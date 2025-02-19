// DR. ROBOTNIK'S RING RACERS
//-----------------------------------------------------------------------------
// Copyright (C) 2025 by Sally "TehRealSalt" Cochenour.
// Copyright (C) 2025 by Kart Krew.
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

#include <algorithm>
#include <cctype>
#include <string>

#include <Archipelago.h>
#include "ap_main.h"

#include "m_cond.h"
#include "m_misc.h" // strcatbf
#include "d_main.h" // srb2home
#include "filesrch.h" // refreshdirmenu
#include "s_sound.h" // struct soundtest
#include "i_system.h" // I_UpdateMouseGrab

boolean g_ap_started;

static const std::string g_ap_file_legal_chars = "abcdefghijklmnopqrstuvwxyz0123456789-_";
static const std::string g_ap_file_ext = ".apdat";

static std::string g_ap_address = "";
static std::string g_ap_slot = "";
static std::string g_ap_password = "";

void RRAP_SetUnlocked(int64_t unlock_id)
{
	if (unlock_id < 0 || unlock_id >= MAXUNLOCKABLES)
	{
		return;
	}

	AP_SendItem(AP_BASE_ID + unlock_id);
}

static void RRAP_GotClearItems(void)
{
	size_t i;

	for (i = 0; i < MAXUNLOCKABLES; i++)
	{
		gamedata->unlocked[i] = 0;
	}
}

static void RRAP_GotItemReceived(int64_t item_id, bool should_notify)
{
	item_id -= AP_BASE_ID;

	if (item_id >= 0 && item_id < MAXUNLOCKABLES)
	{
		// Item ID is an unlockable.
		gamedata->unlocked[item_id] |= UNLOCKED_ITEM;
	}
}

static void RRAP_GotLocationChecked(int64_t location_id)
{
	location_id -= AP_BASE_ID;

	if (location_id >= 0 && location_id < MAXUNLOCKABLES)
	{
		// Location ID is an unlockable.
		gamedata->unlocked[location_id] |= UNLOCKED_LOCATION;
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

	AP_Init(
		g_ap_address.c_str(),
		"Ring Racers",
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

void D_RegisterArchipelagoCommands(void)
{
	COM_AddCommand("ap_connect", Command_AP_Connect);
}
