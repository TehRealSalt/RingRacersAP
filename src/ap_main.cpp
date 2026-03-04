// DR. ROBOTNIK'S RING RACERS
//-----------------------------------------------------------------------------
// Copyright (C) 2026 by Sally "TehRealSalt" Cochenour.
// Copyright (C) 2026 by Kart Krew.
// Copyright (C) 2020 by Sonic Team Junior.
// Copyright (C) 2000 by DooM Legacy Team.
// Copyright (C) 1996 by id Software, Inc.
//
// This program is free software distributed under the
// terms of the GNU General Public License, version 2.
// See the 'LICENSE' file for more details.
//-----------------------------------------------------------------------------
/// \file  ap_main.cpp
/// \brief Archipelago connectivity

#include <Archipelago.h>
#include "ap_main.h"

#include <algorithm>
#include <cctype>
#include <string>

#include "core/string.h"
#include "core/hash_map.hpp"
#include "core/json.hpp"

#include "m_cond.h"
#include "m_misc.h" // strcatbf
#include "d_main.h" // srb2home
#include "filesrch.h" // refreshdirmenu
#include "s_sound.h" // struct soundtest
#include "i_system.h" // I_UpdateMouseGrab
#include "hu_stuff.h" // HU_AddChatText
#include "r_skins.h"
#include "w_wad.h"
#include "z_zone.h"
#include "k_menu.h"

boolean g_ap_started;

static const std::string g_ap_file_legal_chars = "abcdefghijklmnopqrstuvwxyz0123456789-_";
static const std::string g_ap_file_ext = ".apdat";

static srb2::String g_ap_address = "";
static srb2::String g_ap_slot = "";
static srb2::String g_ap_password = "";

extern consvar_t cv_dummy_ap_address;
extern consvar_t cv_dummy_ap_slot;
extern consvar_t cv_dummy_ap_password;

static srb2::HashMap<INT64, rrap_location_t> g_ap_location_info;
static srb2::HashMap<INT64, rrap_item_t> g_ap_item_info;

rrap_location_t::rrap_location_t(INT64 index, srb2::JsonValue json)
{
	_label = json.at("label").get<srb2::String>();
	_condition_set_id = json.value("condition_set", -1);
	_big_tile = json.value("big_tile", false);
}

rrap_item_t::rrap_item_t(INT64 index, srb2::JsonValue json)
{
	_label = json.at("label").get<srb2::String>();

	int work_unlock_id = json.value("unlockable", 0);
	if (work_unlock_id > 0 && work_unlock_id <= MAXUNLOCKABLES)
	{
		// We need to establish this awkward two-way connection
		// purely to maintain compatibility w/ non-Archipelago
		// clients. Multiplayer!!
		_unlockable_id = work_unlock_id - 1;
		unlockables[_unlockable_id].ap_item_id = index;
	}
	else if (work_unlock_id == 0)
	{
		_unlockable_id = MAXUNLOCKABLES;
	}
	else
	{
		throw std::runtime_error(srb2::format("invalid unlock id '{}'", work_unlock_id));
	}

	srb2::String work_skin = json.value("skin", srb2::String(""));
	if (work_skin.empty() == false)
	{
		int skin_id = R_SkinAvailableEx(work_skin.c_str(), false);
		if (skin_id != -1)
		{
			skins[skin_id]->ap_item_id = index;
		}
		else
		{
			throw std::runtime_error(srb2::format("invalid skin '{}'", work_skin));
		}
	}
}

static void RRAP_LoadArchipelagoJSONLump(uint16_t wad_id, lumpnum_t lump_id)
{
	size_t lump_len = W_LumpLengthPwad(wad_id, lump_id);
	const char *lump = static_cast<const char *>( W_CacheLumpNumPwad(wad_id, lump_id, PU_CACHE) );

	srb2::String json_string { lump, lump_len };
	srb2::JsonObject parsed_obj = srb2::JsonValue::from_json_string(json_string).as_object();
	try
	{
		if (parsed_obj.find("locations") != parsed_obj.end())
		{
			srb2::JsonObject locations = parsed_obj.at("locations").as_object();
			for (auto& [key_string, location_obj] : locations)
			{
				INT64 key_index = std::stol(key_string);
				SRB2_ASSERT(key_index > 0);
				SRB2_ASSERT(g_ap_location_info.find(key_index) == g_ap_location_info.end());

				rrap_location_t location(key_index, location_obj);
				g_ap_location_info.try_emplace(key_index, location);
			}
		}
		
		if (parsed_obj.find("items") != parsed_obj.end())
		{
			srb2::JsonObject items = parsed_obj.at("items").as_object();
			for (auto& [key_string, item_obj] : items)
			{
				INT64 key_index = std::stol(key_string);
				SRB2_ASSERT(key_index > 0);
				SRB2_ASSERT(g_ap_item_info.find(key_index) == g_ap_item_info.end());

				rrap_item_t item(key_index, item_obj);
				g_ap_item_info.try_emplace(key_index, item);
			}
		}
	}
	catch (const std::exception& ex)
	{
		I_Error("Archipelago JSON parse error: %s", ex.what());
	}
}

void RRAP_LoadArchipelagoJSON(void)
{
	for (UINT16 wad_num = 0; wad_num < mainwads; wad_num++)
	{
		if (wadfiles[wad_num]->type != RET_PK3)
		{
			continue;
		}

		UINT16 lump_start = W_CheckNumForFolderStartPK3("archipelago/", wad_num, 0);
		if (lump_start == INT16_MAX)
		{
			return;
		}

		UINT16 lump_end = W_CheckNumForFolderEndPK3("archipelago/", wad_num, lump_start);
		for (UINT16 lump_num = lump_start; lump_num < lump_end; lump_num++)
		{
			lumpinfo_t *lump_p = &wadfiles[wad_num]->lumpinfo[lump_num];
			srb2::String file_name = srb2::format("{}|{}", wadfiles[wad_num]->filename, lump_p->fullname);
			CONS_Printf(M_GetText("Loading Archipelago JSON from %s\n"), file_name.c_str());
			RRAP_LoadArchipelagoJSONLump(wad_num, lump_num);
		}
	}
}

rrap_location_t *RRAP_GetLocation(INT64 location_id)
{
	if (!location_id || g_ap_location_info.find(location_id) == g_ap_location_info.end())
	{
		return nullptr;
	}

	return &g_ap_location_info[location_id];
}

rrap_item_t *RRAP_GetItem(INT64 item_id)
{
	if (!item_id || g_ap_item_info.find(item_id) == g_ap_item_info.end())
	{
		return nullptr;
	}

	return &g_ap_item_info[item_id];
}

boolean RRAP_ItemRecieved(rrap_item_t *item)
{
	if (!item)
	{
		return true;
	}

	return item->recieved();
}

UINT16 RRAP_ItemToUnlockableId(rrap_item_t *item)
{
	if (!item)
	{
		return MAXUNLOCKABLES;
	}

	return item->unlockable_id();
}

static void RRAP_GotClearItems(void)
{
	for (auto& [key, value] : g_ap_item_info)
	{
		value.set_recieved(false);
	}

	for (auto& [key, value] : g_ap_location_info)
	{
		value.set_checked(CHECK_FALSE);
	}
}

static void RRAP_GotItemReceived(int64_t item_id, bool should_notify)
{
	if (!item_id || g_ap_item_info.find(item_id) == g_ap_item_info.end())
	{
		CONS_Printf(
			" == AP == could not receive invalid item ID [%li]\n",
			item_id
		);
		return;
	}

	g_ap_item_info[item_id].set_recieved(true);

	if (true) //(should_notify)
	{
		// TEMP?
		CONS_Printf(
			" == AP == GOT ITEM ID [%li]: %s\n",
			item_id,
			g_ap_item_info[item_id].label().c_str()
		);
	}
}

static void RRAP_GotLocationChecked(int64_t location_id)
{
	if (g_ap_location_info.find(location_id) == g_ap_location_info.end())
	{
		CONS_Printf(
			" == AP == could not check invalid location ID [%li]\n",
			location_id
		);
		return;
	}

	g_ap_location_info[location_id].set_checked(CHECK_TRUE);
}

void RRAP_TickMessages(void)
{
	if (AP_IsMessagePending())
	{
		AP_Message *msg = AP_GetLatestMessage();
		HU_AddChatText(va("\x82[AP] \x80%s", msg->text.c_str()), false);
		AP_ClearLatestMessage();
	}
}

static void RRAP_InitGamedata(void)
{
	if (gamedata != nullptr)
	{
		// Close current gamedata...
		G_SaveGameData();
		gamedata->loaded = false;
	}

	// Determine name of this session's gamedata.
	// TODO: Can we get some other game identifier instead?
	// This has lots of collision risk.
	std::string gamedata_name = g_ap_slot + "_" + g_ap_address;
	CONS_Printf("gamedata_name: %s\n", gamedata_name.c_str());

	// Convert to lowercase & discard illegal chars
	std::transform(
		gamedata_name.begin(), gamedata_name.end(), gamedata_name.begin(),
		[](unsigned char c)
		{
			unsigned char lwr = std::tolower(c);
			return ((g_ap_file_legal_chars.find(lwr) == std::string::npos) ? '-' : lwr);
		}
	);

	CONS_Printf("w/o illegal: %s\n", gamedata_name.c_str());

	const size_t file_name_max = sizeof(gamedatafilename) - g_ap_file_ext.size();
	if (gamedata_name.size() >= file_name_max)
	{
		// Will overflow our C-friendly array?
		// Clamp it, I guess...
		gamedata_name.resize(file_name_max - 1);
	}
	CONS_Printf("resized: %s\n", gamedata_name.c_str());

	// add extension
	std::string gamedata_file = gamedata_name + g_ap_file_ext;
	CONS_Printf("gamedata_file: %s\n", gamedata_file.c_str());

	// Copy to the C code...
	strlcpy(gamedatafilename, gamedata_file.c_str(), sizeof(gamedatafilename));
	gamedatafilename[std::min(gamedata_file.size(), sizeof(gamedatafilename) - 1)] = '\0';
	CONS_Printf("gamedatafilename: %s\n", gamedatafilename);

	strlcpy(timeattackfolder, gamedata_name.c_str(), sizeof(timeattackfolder));
	timeattackfolder[std::min(gamedata_name.size(), sizeof(timeattackfolder) - 1)] = '\0';
	CONS_Printf("timeattackfolder: %s\n", timeattackfolder);

	strcpy(savegamename, gamedata_name.c_str());
	strlcat(savegamename, "%u.ssg", sizeof(savegamename));
	// can't use sprintf since there is %u in savegamename
	strcatbf(savegamename, srb2home, PATHSEP);
	CONS_Printf("savegamename: %s\n", savegamename);

	strcpy(gpbackup, va("gp%s.bkp", gamedata_name.c_str()));
	strcatbf(gpbackup, srb2home, PATHSEP);
	CONS_Printf("gpbackup: %s\n", gpbackup);

	refreshdirmenu |= REFRESHDIR_GAMEDATA;

	// Don't softlock the Stereo on if you won't be able to access it anymore!?
	if (soundtest.playing && M_SecretUnlocked(SECRET_SOUNDTEST, true) == false)
	{
		S_SoundTestStop();
	}

	G_LoadGameData();

	// [RRAP] Set up some gamedata variables
	// to be how we want them.
	gamedata->gonerlevel = GDGONER_DONE;
	gamedata->tutorialdone = true;
}

static void RRAP_Connect(void)
{
	AP_Init(
		g_ap_address.c_str(),
		"Dr. Robotnik's Ring Racers",
		g_ap_slot.c_str(),
		g_ap_password.c_str()
	);

	AP_SetItemClearCallback(RRAP_GotClearItems);
	AP_SetItemRecvCallback(RRAP_GotItemReceived);
	AP_SetLocationCheckedCallback(RRAP_GotLocationChecked);

	RRAP_InitGamedata();

	AP_Start();
	g_ap_started = true;

	if (gamestate == GS_MENU || gamestate == GS_TITLESCREEN)
	{
		menuactive = false;
		I_UpdateMouseGrab();
		COM_BufAddText("playintro");
	}
}

static void Command_AP_Connect(void)
{
	if (COM_Argc() < 3 || *COM_Argv(1) == 0 || *COM_Argv(2) == 0)
	{
		CONS_Printf("ap_connect <address> <slot> [password]: connect to an Archipelago room\n");
		return;
	}

	g_ap_address = COM_Argv(1);
	g_ap_slot = COM_Argv(2);
	g_ap_password = COM_Argv(3);

	RRAP_Connect();
}

void D_RegisterArchipelagoCommands(void)
{
	COM_AddCommand("ap_connect", Command_AP_Connect);
}

void RRAP_ConnectFromMenu(int32_t choice)
{
	if (cv_dummy_ap_address.string[0] == '\0')
	{
		M_StartMessage(
			"Archipelago Connection Failure",
			M_GetText(
				"No room address was specified.\n"
			),
			nullptr, MM_NOTHING, nullptr,
			"Back to Menu"
		);
		return;
	}

	if (cv_dummy_ap_slot.string[0] == '\0')
	{
		M_StartMessage(
			"Archipelago Connection Failure",
			M_GetText(
				"No slot name was specified.\n"
			),
			nullptr, MM_NOTHING, nullptr,
			"Back to Menu"
		);
		return;
	}

	g_ap_address = cv_dummy_ap_address.string;
	g_ap_slot = cv_dummy_ap_slot.string;
	g_ap_password = cv_dummy_ap_password.string;

	RRAP_Connect();
}
