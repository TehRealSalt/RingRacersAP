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
#include "core/vector.hpp"

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
#include "m_random.h" // TODO remove this

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
	_id = index;
	_name = json.at("name").get<srb2::String>();
	_condition_set_id = json.value("condition_set", -1);
	_big_tile = json.value("big_tile", false);
	_label = json.value("label", srb2::String(""));
}

void rrap_location_t::immediate_check()
{
	if (!_checked)
	{
		// TODO: don't set this on reconnect
		_check_pending = true;
	}

	_checked = true;

	AP_SendItem(_id);

	std::set<INT64> scout_ids = {_id};
	AP_SendLocationScouts(scout_ids, 0);
}

void rrap_location_t::queue_check()
{
	_check_pending = true;

	std::set<INT64> scout_ids = {_id};
	AP_SendLocationScouts(scout_ids, 0);
}

void rrap_location_t::update_displayed_item(srb2::String label, INT64 item_id)
{
	CONS_Printf(
		"[AP] Updating location %li display item (label: %s, id: %li)\n",
		_id, label.c_str(), item_id
	);

	if (g_ap_item_info.find(item_id) != g_ap_item_info.end())
	{
		_display_item_id = item_id;
		_display_item_label = g_ap_item_info[item_id].label();
	}
	else
	{
		_display_item_id = 0;
		_display_item_label = label;
	}
}

rrap_item_t::rrap_item_t(INT64 index, srb2::JsonValue json)
{
	_id = index;
	_name = json.at("name").get<srb2::String>();

	_unlockable_id = MAXUNLOCKABLES;
	_skin_id = -1;
	_follower_id = -1;

	_label = json.value("label", srb2::String(""));
	_display_type = SECRET_NONE;
	_display_icon = "";
	_display_color = SKINCOLOR_NONE;

	int work_unlock_id = json.value("unlockable", 0);
	if (work_unlock_id > 0 && work_unlock_id <= MAXUNLOCKABLES)
	{
		// We need to establish this awkward two-way connection
		// purely to maintain compatibility w/ non-Archipelago
		// clients. Multiplayer!!
		_unlockable_id = work_unlock_id - 1;
		unlockables[_unlockable_id].ap_item_id = index;
	}
	else if (work_unlock_id != 0)
	{
		throw std::runtime_error(srb2::format("invalid unlock id '{}'", work_unlock_id));
	}

	srb2::String work_skin = json.value("skin", srb2::String(""));
	if (work_skin.empty() == false)
	{
		int skin_id = R_SkinAvailableEx(work_skin.c_str(), false);
		if (skin_id != -1)
		{
			_skin_id = skin_id;
			skins[_skin_id]->ap_item_id = index;

			SRB2_ASSERT(_display_type == SECRET_NONE);
			_display_type = SECRET_SKIN;
		}
		else
		{
			throw std::runtime_error(srb2::format("invalid skin '{}'", work_skin));
		}
	}

	srb2::String work_follower = json.value("follower", srb2::String(""));
	if (work_follower.empty() == false)
	{
		int follower_id = K_FollowerAvailable(work_follower.c_str());
		if (follower_id != -1)
		{
			_follower_id = follower_id;
			followers[_follower_id].ap_item_id = index;

			SRB2_ASSERT(_display_type == SECRET_NONE);
			_display_type = SECRET_FOLLOWER;
		}
		else
		{
			throw std::runtime_error(srb2::format("invalid follower '{}'", work_follower));
		}
	}

	srb2::String work_cup = json.value("cup", srb2::String(""));
	if (work_cup.empty() == false)
	{
		// The ID isn't used, so just update display type
		SRB2_ASSERT(_display_type == SECRET_NONE);
		_display_type = SECRET_CUP;
	}

	srb2::String work_map = json.value("map", srb2::String(""));
	if (work_map.empty() == false)
	{
		// The ID isn't used, so just update display type
		SRB2_ASSERT(_display_type == SECRET_NONE);
		_display_type = SECRET_MAP;
	}

	srb2::String work_type = json.value("item_type", srb2::String(""));
	if (work_type.empty() == false)
	{
		SRB2_ASSERT(_display_type == SECRET_NONE);

		if (work_type == "hardspeed")
		{
			_display_type = SECRET_HARDSPEED;
		}
		else if (work_type == "mastermode")
		{
			_display_type = SECRET_MASTERMODE;
		}
		else if (work_type == "encore")
		{
			_display_type = SECRET_ENCORE;
		}
		else if (work_type == "timeattack")
		{
			_display_type = SECRET_TIMEATTACK;
		}
		else if (work_type == "prisonbreak")
		{
			_display_type = SECRET_PRISONBREAK;
		}
		else if (work_type == "specialattack")
		{
			_display_type = SECRET_SPECIALATTACK;
		}
		else if (work_type == "spbattack")
		{
			_display_type = SECRET_SPBATTACK;
		}
		else if (work_type == "online")
		{
			_display_type = SECRET_ONLINE;
		}
		else if (work_type == "addons")
		{
			_display_type = SECRET_ADDONS;
		}
		else if (work_type == "eggtv")
		{
			_display_type = SECRET_EGGTV;
		}
		else if (work_type == "soundtest")
		{
			_display_type = SECRET_SOUNDTEST;
		}
		else if (work_type == "alttitle")
		{
			_display_type = SECRET_ALTTITLE;
		}
		else
		{
			throw std::runtime_error(srb2::format("invalid special item type '{}'", work_type));
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

char *RRAP_LocationLabel(rrap_location_t *location)
{
	if (!location)
	{
		return nullptr;
	}

	return Z_StrDup( location->label().c_str() );
}

UINT16 RRAP_LocationConditionSet(rrap_location_t *location)
{
	if (!location)
	{
		return 0;
	}

	return location->condition_set_id();
}

boolean RRAP_LocationIsBigTile(rrap_location_t *location)
{
	if (!location)
	{
		return false;
	}

	return location->is_big_tile();
}

boolean RRAP_LocationChecked(rrap_location_t *location)
{
	if (!location)
	{
		return true;
	}

	return location->checked();
}

boolean RRAP_LocationCheckPending(rrap_location_t *location)
{
	if (!location)
	{
		return false;
	}

	return location->check_pending();
}

char *RRAP_LocationDisplayItemLabel(rrap_location_t *location)
{
	if (!location)
	{
		return nullptr;
	}

	return Z_StrDup( location->display_item_label().c_str() );
}

rrap_item_t *RRAP_LocationDisplayItem(rrap_location_t *location)
{
	if (!location)
	{
		return nullptr;
	}

	INT64 item_id = location->display_item_id();
	if (!item_id || g_ap_item_info.find(item_id) == g_ap_item_info.end())
	{
		return nullptr;
	}

	return &g_ap_item_info[item_id];
}

void RRAP_LocationImmediateCheck(rrap_location_t *location)
{
	if (!location)
	{
		return;
	}

	location->immediate_check();
}

void RRAP_LocationQueueCheck(rrap_location_t *location)
{
	if (!location)
	{
		return;
	}

	location->queue_check();
}

void RRAP_LocationUnqueueCheck(rrap_location_t *location)
{
	if (!location)
	{
		return;
	}

	location->unqueue_check();
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

INT32 RRAP_ItemToSkinId(rrap_item_t *item)
{
	if (!item)
	{
		return -1;
	}

	return item->skin_id();
}

INT32 RRAP_ItemToFollowerId(rrap_item_t *item)
{
	if (!item)
	{
		return -1;
	}

	return item->follower_id();
}

INT32 RRAP_ItemDisplayType(rrap_item_t *item)
{
	if (!item)
	{
		return SECRET_NONE;
	}

	return item->display_type();
}

char *RRAP_ItemDisplayIcon(rrap_item_t *item)
{
	if (!item)
	{
		return nullptr;
	}

	return Z_StrDup( item->display_icon().c_str() );
}

UINT16 RRAP_ItemDisplayColor(rrap_item_t *item)
{
	if (!item)
	{
		return SKINCOLOR_NONE;
	}

	return item->display_color();
}

void RRAP_PopulateChallengeGrid(void)
{
	INT64 i, j;
	srb2::Vector<INT64> selection_small;
	srb2::Vector<INT64> selection_big;
	UINT64 num_empty = 0;
	int big_compact = 2;

	if (gamedata->ap_challengegrid != nullptr)
	{
		// todo tweak your grid if unlocks are changed
		return;
	}

	// Go through unlockables
	for (auto& [id, location] : g_ap_location_info)
	{
		UINT16 condition_set = location.condition_set_id();
		if (!condition_set)
		{
			continue;
		}

		if (location.is_big_tile())
		{
			selection_big.emplace_back(id);
			CONS_Printf(" found %li (LARGE)\n", id);
		}
		else
		{
			selection_small.emplace_back(id);
			CONS_Printf(" found %li\n", id);
		}
	}

	gamedata->ap_challengegridwidth = 0;

	if (selection_small.size() + selection_big.size() == 0)
	{
		return;
	}

	if (selection_big.size())
	{
		// Getting the number of 2-highs you can fit into two adjacent columns.
		size_t big_pad = (CHALLENGEGRIDHEIGHT / 2);
		num_empty = selection_big.size() % big_pad;
		big_pad = (selection_big.size() + (big_pad - 1)) / big_pad;

		gamedata->ap_challengegridwidth = big_pad * 2;
		num_empty *= 4;

#if (CHALLENGEGRIDHEIGHT % 2)
		// One extra empty per column.
		num_empty += gamedata->ap_challengegridwidth;
#endif

		CONS_Printf(
			"%lu major unlocks means width of %lu, numempty of %lu\n",
			selection_big.size(),
			gamedata->ap_challengegridwidth,
			num_empty
		);
	}

	if (selection_small.size() > num_empty)
	{
		// Getting the number of extra columns to store normal unlocks
		UINT64 temp = ((selection_small.size() - num_empty) + (CHALLENGEGRIDHEIGHT - 1)) / CHALLENGEGRIDHEIGHT;
		gamedata->ap_challengegridwidth += temp;
		big_compact = 1;

		CONS_Printf(
			"%lu normal unlocks means %lu extra entries, additional width of %lu\n",
			selection_small.size(),
			(selection_small.size() - num_empty),
			temp
		);
	}
	else if (challengegridloops)
	{
		// Another case where offset large tiles are permitted.
		big_compact = 1;
	}

#if 0
	// [RRAP] The placing algorithm fails HARD with too many big tiles.
	// Try to just salvage it for now, look into a better way of placing
	// these down later.
	INT64 big_tile_area = selection_big.size() * 4;
	INT64 min_width = (big_tile_area * 3 / 2) / CHALLENGEGRIDHEIGHT;
	if (gamedata->ap_challengegridwidth < min_width)
	{
		gamedata->ap_challengegridwidth = min_width;

		CONS_Printf(
			" FORCING WIDTH HACK: %lu\n",
			min_width
		);
	}
#endif

	gamedata->ap_challengegrid = static_cast<int64_t *>(Z_Calloc(
		(gamedata->ap_challengegridwidth * CHALLENGEGRIDHEIGHT * sizeof(INT64)),
		PU_STATIC, nullptr
	));

	if (!gamedata->ap_challengegrid)
	{
		I_Error("RRAP_PopulateChallengeGrid: was not able to allocate grid");
	}

	// Attempt to place all large tiles first.
	if (selection_big.size())
	{
		// You lose one from CHALLENGEGRIDHEIGHT because it is impossible to place a 2-high tile on the bottom row.
		// You lose one from the width if it doesn't loop.
		// You divide by two if the grid is so compacted that large tiles can't be in offset columns.
		INT64 num_spots = (gamedata->ap_challengegridwidth - (challengegridloops ? 0 : big_compact))
				* ((CHALLENGEGRIDHEIGHT - 1) / big_compact);

		// 0 is row, 1 is column
		srb2::Vector<INT64> quick_check;
		quick_check.resize(2 * num_spots, 0);

		// Prepare the easy-grab spots.
		for (i = 0; i < num_spots; i++)
		{
			quick_check[i * 2 + 0] = i % (CHALLENGEGRIDHEIGHT - 1);
			quick_check[i * 2 + 1] = big_compact * i / (CHALLENGEGRIDHEIGHT - 1);
		}

		// Place in random valid locations.
		while (selection_big.size() && num_spots > 0)
		{
			INT64 row, col;

			// RRAP TODO - this needs to be seeded with the room,
			// so that races between 2 worlds are fair
			j = M_RandomKey(num_spots);

			row = quick_check[j * 2 + 0];
			col = quick_check[j * 2 + 1];

			// We always take from selection_big in order, but the PLACEMENT is still random.
			INT64 placed = selection_big.back();
			selection_big.pop_back();

			CONS_Printf("--- %li (LARGE) placed at (%li, %li)\n", placed, row, col);

			i = row + (col * CHALLENGEGRIDHEIGHT);
			gamedata->ap_challengegrid[i] = gamedata->ap_challengegrid[i+1] = placed;

			if (col == gamedata->ap_challengegridwidth - 1)
			{
				i = row;
			}
			else
			{
				i += CHALLENGEGRIDHEIGHT;
			}

			gamedata->ap_challengegrid[i] = gamedata->ap_challengegrid[i+1] = placed;

			if (selection_big.empty())
			{
				break;
			}

			for (i = 0; i < num_spots; i++)
			{
quickcheckagain:
				if (abs((quick_check[i * 2 + 0]) - (row)) <= 1 // Row distance
					&& (abs((quick_check[i * 2 + 1]) - (col)) <= 1 // Column distance
					|| (quick_check[i * 2 + 1] == 0 && col == gamedata->ap_challengegridwidth-1) // Wraparounds l->r
					|| (quick_check[i * 2 + 1] == gamedata->ap_challengegridwidth-1 && col == 0))) // Wraparounds r->l
				{
					// Remove from possible indicies
					num_spots--;

					if (i == num_spots)
						break;

					// Shuffle remaining so we can keep on using M_RandomKey
					quick_check[i * 2 + 0] = quick_check[num_spots * 2 + 0];
					quick_check[i * 2 + 1] = quick_check[num_spots * 2 + 1];

					// Woah there - we've gotta check the one that just got put in our place.
					goto quickcheckagain;
				}

				continue;
			}
		}

#if (CHALLENGEGRIDHEIGHT == 4)
		while (selection_big.size())
		{
			INT64 location_to_move = 0;

			j = gamedata->ap_challengegridwidth - 1;

			// Attempt to fix our whoopsie.
			for (i = 0; i < j; i++)
			{
				if (gamedata->ap_challengegrid[1 + (i * CHALLENGEGRIDHEIGHT)] != 0
					&& gamedata->ap_challengegrid[(i * CHALLENGEGRIDHEIGHT)] == 0)
					break;
			}

			if (i == j)
			{
				break;
			}

			location_to_move = gamedata->ap_challengegrid[1 + (i*CHALLENGEGRIDHEIGHT)];

			if (i == 0
				&& challengegridloops
				&& (gamedata->ap_challengegrid [1 + (j * CHALLENGEGRIDHEIGHT)]
					== gamedata->ap_challengegrid[1]))
				;
			else
			{
				j = i + 1;
			}

			INT64 placed = selection_big.back();
			selection_big.pop_back();

			// Push one pair up.
			gamedata->ap_challengegrid[(i*CHALLENGEGRIDHEIGHT)] = gamedata->ap_challengegrid[(j*CHALLENGEGRIDHEIGHT)] = location_to_move;

			// Wedge the remaining four underneath.
			gamedata->ap_challengegrid[2 + (i*CHALLENGEGRIDHEIGHT)] = gamedata->ap_challengegrid[2 + (j*CHALLENGEGRIDHEIGHT)] = placed;
			gamedata->ap_challengegrid[3 + (i*CHALLENGEGRIDHEIGHT)] = gamedata->ap_challengegrid[3 + (j*CHALLENGEGRIDHEIGHT)] = placed;
		}
#endif

		if (selection_big.size())
		{
			UINT64 width_to_print = gamedata->ap_challengegridwidth;

			Z_Free(gamedata->ap_challengegrid);
			gamedata->ap_challengegrid = nullptr;

			I_Error(
				"RRAP_PopulateChallengeGrid: was not able to populate %lu large tiles (width %lu)",
				selection_big.size(),
				width_to_print
			);
		}
	}

	num_empty = 0;

	// Space out empty entries to pepper into unlock list
	for (i = 0; i < gamedata->ap_challengegridwidth * CHALLENGEGRIDHEIGHT; i++)
	{
		if (gamedata->ap_challengegrid[i] != 0)
		{
			continue;
		}

		num_empty++;
	}

	if (selection_small.size() > num_empty)
	{
		gamedata->ap_challengegridwidth = 0;

		Z_Free(gamedata->ap_challengegrid);
		gamedata->ap_challengegrid = nullptr;

		I_Error(
			"M_PopulateChallengeGrid: %lu small unlocks vs %lu empty spaces (%lu gap)",
			selection_small.size(),
			num_empty,
			(selection_small.size() - num_empty)
		);
	}

	CONS_Printf(" %lu unlocks vs %lu empty spaces\n", selection_small.size(), num_empty);

	while (selection_small.size() < num_empty)
	{
		CONS_Printf(" adding empty)\n");
		selection_small.emplace_back(0);
	}

	// Fill the remaining spots with random ordinary unlocks (and empties).
	for (i = 0; i < gamedata->ap_challengegridwidth * CHALLENGEGRIDHEIGHT; i++)
	{
		if (gamedata->ap_challengegrid[i] != 0)
		{
			continue;
		}

		// RRAP TODO - this needs to be seeded with the room,
		// so that races between 2 worlds are fair
		j = M_RandomKey(selection_small.size()); // Get an entry

		INT64 placed = selection_small[j];
		selection_small.erase(selection_small.begin() + j);

		gamedata->ap_challengegrid[i] = placed; // Set that entry

		CONS_Printf(" %li placed at (%li, %li)\n", placed, i / CHALLENGEGRIDHEIGHT, i % CHALLENGEGRIDHEIGHT);

		if (selection_small.empty())
		{
			break;
		}
	}
}

void RRAP_SanitiseChallengeGrid(void)
{
	srb2::HashMap<INT64, int> seen;
	srb2::Vector<INT64> empty;
	INT64 i, j;

	if (gamedata->ap_challengegrid == nullptr)
		return;

	// Go through all spots to identify duplicates and absences.
	for (j = 0; j < gamedata->ap_challengegridwidth * CHALLENGEGRIDHEIGHT; j++)
	{
		i = gamedata->ap_challengegrid[j];

		rrap_location_t &ref = g_ap_location_info[i];
		if (i <= 0 || !ref.condition_set_id())
		{
			empty.emplace_back(j);
			continue;
		}

		if (seen.find(i) == seen.end())
		{
			seen[i] = 0;
		}

		if (seen[i] != 5) // Arbitrary cap greater than 4
		{
			seen[i]++;

			if (seen[i] == 1 || ref.is_big_tile())
			{
				continue;
			}
		}

		empty.emplace_back(j);
	}

	// Go through unlockables to identify if any haven't been seen.
	for (auto& [id, location] : g_ap_location_info)
	{
		if (!location.condition_set_id())
		{
			continue;
		}
	
		if (location.is_big_tile() && seen[id] != 4)
		{
			// Probably not enough spots to retrofit.
			goto badgrid;
		}

		if (seen[id] != 0)
		{
			// Present on the challenge grid.
			continue;
		}

		if (empty.size() != 0)
		{
			// Small ones can be slotted in easy.
			j = empty.back();
			empty.pop_back();

			gamedata->ap_challengegrid[j] = id;
		}

		// Nothing we can do to recover.
		goto badgrid;
	}

	// Fill the remaining spots with empties.
	while (empty.size() != 0)
	{
		j = empty.back();
		empty.pop_back();

		gamedata->ap_challengegrid[j] = 0;
	}

	return;

badgrid:
	// Just remove everything and let it get regenerated.
	Z_Free(gamedata->ap_challengegrid);
	gamedata->ap_challengegrid = nullptr;
	gamedata->ap_challengegridwidth = 0;
}

int RRAP_TestLocations(void)
{
	int response = 0;

	for (auto& [index, location] : g_ap_location_info)
	{
		UINT16 condition_set = location.condition_set_id();
		if (!condition_set)
		{
			continue;
		}

		if (location.checked() == true
			|| location.check_pending() == true)
		{
			continue;
		}

		if (M_Achieved(condition_set - 1) == false)
		{
			continue;
		}

		location.queue_check();
		response++;
	}

	return response;
}

INT64 RRAP_GetNextCheckedLocation(boolean canskipchaokeys)
{
	// Go through unlockables
	for (auto& [id, location] : g_ap_location_info)
	{
		UINT16 condition_set = location.condition_set_id();
		if (!condition_set)
		{
			// Not worthy of consideration
			continue;
		}

		if (location.checked() == true)
		{
			// Already unlocked, no need to engage
			continue;
		}

		if (location.check_pending() == false)
		{
			// Not unlocked AND not pending, which means chao keys can be used on something
			canskipchaokeys = false;
			continue;
		}

		return id;
	}

	if (canskipchaokeys == true)
	{
		// Okay, we're skipping chao keys - let's just insta-digest them.

		if (gamedata->chaokeys + gamedata->keyspending < GDMAX_CHAOKEYS)
		{
			gamedata->chaokeys += gamedata->keyspending;
			gamedata->pendingkeyroundoffset =
				(gamedata->pendingkeyroundoffset + gamedata->pendingkeyrounds)
				% GDCONVERT_ROUNDSTOKEY;

		}
		else
		{
			gamedata->chaokeys = GDMAX_CHAOKEYS;
			gamedata->pendingkeyroundoffset = 0;
		}

		gamedata->keyspending = 0;
		gamedata->pendingkeyrounds = 0;
	}
	else if (gamedata->keyspending != 0)
	{
		// Sentinel value to queue the animation
		return -1;
	}

	return 0;
}

void RRAP_ChallengesMenuCountPercent(void)
{
	challengesmenu.unlockcount[CMC_UNLOCKED] = 0;
	challengesmenu.unlockcount[CMC_TOTAL] = 0;
	challengesmenu.unlockcount[CMC_KEYED] = 0;
	challengesmenu.unlockcount[CMC_MAJORSKIPPED] = 0;

// The "basic" medal is basically never seen because Major challenges
// are usually completed last before 101%. Correct that with this
//#define MAJORDISTINCTION

	for (auto& [id, location] : g_ap_location_info)
	{
		UINT16 condition_set = location.condition_set_id();
		if (!condition_set)
		{
			continue;
		}

		challengesmenu.unlockcount[CMC_TOTAL]++;

		if (!location.checked())
		{
			continue;
		}

		challengesmenu.unlockcount[CMC_UNLOCKED]++;

		if (M_Achieved(condition_set - 1) == true)
		{
			continue;
		}

		challengesmenu.unlockcount[CMC_KEYED]++;

#ifdef MAJORDISTINCTION
		if (unlockables[i].majorunlock == false)
		{
			continue;
		}

		challengesmenu.unlockcount[CMC_MAJORSKIPPED]++;
#endif
	}

	challengesmenu.unlockcount[CMC_PERCENT] =
		(100 * challengesmenu.unlockcount[CMC_UNLOCKED])
			/ challengesmenu.unlockcount[CMC_TOTAL];
}

INT64 RRAP_ChallengesMenuRandomFocus(INT32 level)
{
	srb2::Vector<INT64> selection;

	// Get a random available location.
	for (auto& [id, location] : g_ap_location_info)
	{
		UINT16 condition_set = location.condition_set_id();
		if (!condition_set)
		{
			continue;
		}

		// Otherwise we don't care, just pick any non-blank tile
		if (level < 2)
		{
			// We try for any unlock second
			if (!location.checked())
			{
				continue;
			}

			if (level == 0)
			{
				// We try for a pending unlock first
				if (!location.check_pending())
				{
					continue;
				}
			}
		}

		selection.emplace_back(id);
	}

	if (selection.empty())
	{
		return 0;
	}

	INT32 index = M_RandomKey(selection.size());
	return selection[index];
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

static void RRAP_GotClearItems(void)
{
	for (auto& [id, item] : g_ap_item_info)
	{
		item.on_clear();
	}

	for (auto& [id, location] : g_ap_location_info)
	{
		location.on_clear();
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

	g_ap_item_info[item_id].recieve();

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

	g_ap_location_info[location_id].immediate_check();
}

static void RRAP_GotLocationInfo(std::vector<AP_NetworkItem> network_items)
{
	CONS_Printf(" == AP == got location info packet...\n");

	for (auto& net_item : network_items)
	{
		CONS_Printf(
			" == AP == got location info ID [%li]\n",
			net_item.location
		);

		if (g_ap_location_info.find(net_item.location) == g_ap_location_info.end())
		{
			CONS_Printf(
				" == AP == could not set location info for invalid location ID [%li]\n",
				net_item.location
			);
			return;
		}

		g_ap_location_info[net_item.location].update_displayed_item(
			net_item.itemName, net_item.item
		);
	}
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
	AP_SetLocationInfoCallback(RRAP_GotLocationInfo);

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
