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
#include "m_random.h"
#include "v_video.h"
#include "i_time.h"
#include "r_main.h"
#include "i_video.h"
#include "k_hud.h"
#include "k_battle.h"
#include "k_grandprix.h"

boolean g_ap_started;

static const std::string g_ap_file_legal_chars = "abcdefghijklmnopqrstuvwxyz0123456789-_";
static const std::string g_ap_file_ext = ".apdat";

static srb2::String g_ap_address = "";
static srb2::String g_ap_slot = "";
static srb2::String g_ap_password = "";

extern consvar_t cv_dummy_ap_address;
extern consvar_t cv_dummy_ap_slot;
extern consvar_t cv_dummy_ap_password;

static srb2::String g_ap_seed = "";
static UINT32 g_ap_seed_hash = 0;

static srb2::HashMap<INT64, rrap_location_t> g_ap_location_info;
static srb2::HashMap<INT64, rrap_item_t> g_ap_item_info;

static UINT32 g_character_wins_count = 0;
static boolean g_simple_map_access = false;
static UINT16 g_keygen_rate = GDCONVERT_ROUNDSTOKEY;
static UINT8 g_goal_num_trophies = UINT8_MAX;
static UINT8 g_goal_trophy_level = 0;

static boolean g_goal_queued = false;
static boolean g_goal_sent = false;

static boolean g_cd_missed_this_map = false;

static srb2::Vector<srb2::String> g_group_blacklist;
static srb2::Vector<srb2::String> g_group_whitelist;
static srb2::Vector<srb2::String> g_name_blacklist;
static srb2::Vector<srb2::String> g_name_whitelist;

rrap_location_t::rrap_location_t(srb2::JsonValue json)
{
	_id = json.at("id").get<INT64>();
	SRB2_ASSERT(_id > 0);

	_name = json.at("name").get<srb2::String>();
	_label = json.value("label", srb2::String(""));
	_big_tile = json.value("big_tile", false);

	_condition_set_id = json.value("condition_set", 0);
	_prison_cd_count = json.value("cd_count", 0);
	_spray_can_map_id = 0;

	srb2::String spray_can_map_name = json.value("spray_can_map", srb2::String(""));
	if (!spray_can_map_name.empty())
	{
		INT32 map_id = G_FindMapByNameOrCode(spray_can_map_name.c_str(), 0);
		if (map_id > 0)
		{
			_spray_can_map_id = map_id;
			mapheaderinfo[_spray_can_map_id - 1]->ap_spraycan_location_id = _id;
		}
		else
		{
			throw std::runtime_error(srb2::format("invalid spray can location map '{}'", spray_can_map_name));
		}
	}

	srb2::JsonArray tags_array = json.at("tags").get<srb2::JsonArray>();
	for (auto &tag_value : tags_array)
	{
		srb2::String tag = tag_value.get<srb2::String>();
		_tags.emplace_back(tag);
	}
}

void rrap_location_t::update_available()
{
	if (std::find(g_name_whitelist.begin(), g_name_whitelist.end(), _name) != g_name_whitelist.end())
	{
		_available = true;
		return;
	}

	if (std::find(g_name_blacklist.begin(), g_name_blacklist.end(), _name) != g_name_blacklist.end())
	{
		_available = false;
		return;
	}

	for (auto &tag : _tags)
	{
		if (std::find(g_group_whitelist.begin(), g_group_whitelist.end(), tag) != g_group_whitelist.end())
		{
			_available = true;
			return;
		}

		if (std::find(g_group_blacklist.begin(), g_group_blacklist.end(), tag) != g_group_blacklist.end())
		{
			_available = false;
			return;
		}
	}

	_available = true;
}

void rrap_location_t::immediate_check(bool skip_pending)
{
	SRB2_ASSERT(_id > 0);

	if (!skip_pending && !_checked)
	{
		// TODO: instead of skip pending,
		// save which locations were checked / pending
		// into gamedata so that we can keep the pending
		// highlight on everything that wasn't inspected
		_check_pending = true;
	}

	_checked = true;
	AP_SendItem(_id);

	std::set<INT64> scout_ids = {_id};
	AP_SendLocationScouts(scout_ids, 0);
}

void rrap_location_t::queue_check()
{
	SRB2_ASSERT(_id > 0);

	_check_pending = true;

	std::set<INT64> scout_ids = {_id};
	AP_SendLocationScouts(scout_ids, 0);
}

void rrap_location_t::update_displayed_item(srb2::String label, INT64 item_id, srb2::String player, UINT8 item_class)
{
	/*
	CONS_Printf(
		"Updating AP location [%li]'s display item (label: %s, id: %li)\n",
		_id, label.c_str(), item_id
	);
	*/

	bool is_ours = false;
	if (g_ap_item_info.find(item_id) != g_ap_item_info.end())
	{
		// Item ID exists, but IDs can overlap between games.
		// So double check the name matches, too.
		is_ours = (label == g_ap_item_info[item_id].name());
	}

	if (is_ours)
	{
		// Item is from our world, display it directly
		_display_item_id = item_id;
		_display_item_label = g_ap_item_info[item_id].label();
	}
	else
	{
		// Item is not ours, we can only display the name
		_display_item_id = 0;
		_display_item_label = label;
	}

	if (player == g_ap_slot)
	{
		_display_item_player = "";
		_display_item_offworld = !is_ours; // super double-check
	}
	else
	{
		_display_item_player = player;
		_display_item_offworld = true;
	}

	_display_item_class = item_class;
}

rrap_item_t::rrap_item_t(srb2::JsonValue json)
{
	_id = json.at("id").get<INT64>();
	SRB2_ASSERT(_id > 0);

	_name = json.at("name").get<srb2::String>();

	_unlockable_id = MAXUNLOCKABLES;
	_skin_id = -1;
	_follower_id = -1;
	_color_id = SKINCOLOR_NONE;

	_progressive_parent = 0;
	_progressive_count = 0;

	_label = json.value("label", srb2::String(""));
	_display_type = SECRET_NONE;
	_display_icon = json.value("icon", srb2::String(""));
	_display_color = SKINCOLOR_NONE;

	int work_unlock_id = json.value("unlockable", 0);
	if (work_unlock_id > 0 && work_unlock_id <= MAXUNLOCKABLES)
	{
		// We need to establish this awkward two-way connection
		// purely to maintain compatibility w/ non-Archipelago
		// clients. Multiplayer!!
		_unlockable_id = work_unlock_id - 1;
		unlockables[_unlockable_id].ap_item_id = _id;
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
			skins[_skin_id]->ap_item_id = _id;

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
			followers[_follower_id].ap_item_id = _id;

			SRB2_ASSERT(_display_type == SECRET_NONE);
			_display_type = SECRET_FOLLOWER;
		}
		else
		{
			throw std::runtime_error(srb2::format("invalid follower '{}'", work_follower));
		}
	}

	srb2::String work_color = json.value("color", srb2::String(""));
	if (work_color.empty() == false)
	{
		int color_id = SKINCOLOR_NONE;
		for (int i = SKINCOLOR_NONE+1; i < numskincolors; ++i)
		{
			if (!strcasecmp(skincolors[i].name, work_color.c_str()))
			{
				color_id = i;
				break;
			}
		}

		if (color_id != SKINCOLOR_NONE)
		{
			_color_id = color_id;
			skincolors[_color_id].ap_item_id = _id;

			SRB2_ASSERT(_display_type == SECRET_NONE);
			_display_type = SECRET_COLOR;
		}
		else
		{
			throw std::runtime_error(srb2::format("invalid color '{}'", work_color));
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

	srb2::String work_song_map = json.value("song_map", srb2::String(""));
	if (work_song_map.empty() == false)
	{
		// The ID isn't used, so just update display type
		SRB2_ASSERT(_display_type == SECRET_NONE);
		_display_type = SECRET_ALTMUSIC;
	}

	srb2::String work_type = json.value("item_type", srb2::String(""));
	if (work_type.empty() == false)
	{
		SRB2_ASSERT(_display_type == SECRET_NONE);

		static srb2::HashMap<srb2::String, INT32> name_to_type = {
			{"hardspeed", SECRET_HARDSPEED},
			{"mastermode", SECRET_MASTERMODE},
			{"encore", SECRET_ENCORE},
			{"timeattack", SECRET_TIMEATTACK},
			{"prisonbreak", SECRET_PRISONBREAK},
			{"specialattack", SECRET_SPECIALATTACK},
			{"spbattack", SECRET_SPBATTACK},
			{"online", SECRET_ONLINE},
			{"addons", SECRET_ADDONS},
			{"eggtv", SECRET_EGGTV},
			{"soundtest", SECRET_SOUNDTEST},
			{"alttitle", SECRET_ALTTITLE},
			{"kkd", SECRET_AP_KKD},
			{"chaokey", SECRET_AP_CHAOKEY}
		};

		if (name_to_type.find(work_type) != name_to_type.end())
		{
			_display_type = name_to_type[work_type];
		}
		else
		{
			throw std::runtime_error(srb2::format("invalid special item type '{}'", work_type));
		}
	}

	if (json.contains("progressive_mapping"))
	{
		srb2::JsonArray progressive_array = json.at("progressive_mapping").as_array();
		for (auto &progressive_value : progressive_array)
		{
			INT64 progressive_id = progressive_value.get<INT64>();
			SRB2_ASSERT(progressive_id > 0);
			// we will confirm more things about the ID when we update children
			_progressive_children.emplace_back(progressive_id);
		}
	}
}

UINT32 rrap_item_t::received(bool recurse) const
{
	UINT32 count = _received;

	if (recurse && _progressive_parent != 0)
	{
		SRB2_ASSERT(_progressive_parent > 0);
		SRB2_ASSERT(g_ap_item_info.find(_progressive_parent) != g_ap_item_info.end());

		rrap_item_t &parent = g_ap_item_info[_progressive_parent];
		if (parent.received(false) >= _progressive_count)
		{
			count += 1;
		}
	}

	return count;
}

INT32 rrap_item_t::display_type(bool recurse) const
{
	if (recurse && !_progressive_children.empty())
	{
		UINT32 index = std::clamp<UINT32>(_received - 1, 0, _progressive_children.size() - 1);

		INT64 child_id = _progressive_children[index];
		SRB2_ASSERT(child_id > 0);
		SRB2_ASSERT(g_ap_item_info.find(child_id) != g_ap_item_info.end());

		rrap_item_t child = g_ap_item_info[child_id];
		return child.display_type(false);
	}

	return _display_type;
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
			srb2::JsonArray locations = parsed_obj.at("locations").as_array();
			for (auto& location_obj : locations)
			{
				rrap_location_t location(location_obj);

				INT64 index = location.id();
				SRB2_ASSERT(index > 0);
				SRB2_ASSERT(g_ap_location_info.find(index) == g_ap_location_info.end());
				g_ap_location_info.try_emplace(index, location);
			}
		}
		
		if (parsed_obj.find("items") != parsed_obj.end())
		{
			srb2::JsonArray items = parsed_obj.at("items").as_array();
			for (auto& item_obj : items)
			{
				rrap_item_t item(item_obj);

				INT64 index = item.id();
				SRB2_ASSERT(index > 0);
				SRB2_ASSERT(g_ap_item_info.find(index) == g_ap_item_info.end());
				g_ap_item_info.try_emplace(index, item);
			}
		}
	}
	catch (const std::exception& ex)
	{
		I_Error("Archipelago JSON parse error: %s", ex.what());
	}
}

void rrap_item_t::update_children()
{
	if (_progressive_children.empty())
	{
		return;
	}

	for (UINT32 i = 0; i < _progressive_children.size(); i++)
	{
		INT64 child_id = _progressive_children[i];

		SRB2_ASSERT(child_id > 0);
		SRB2_ASSERT(g_ap_item_info.find(child_id) != g_ap_item_info.end());
		rrap_item_t &child = g_ap_item_info[child_id];

		child.update_from_parent(_id, i + 1);
	}
}

void rrap_item_t::update_from_parent(INT64 parent_id, UINT32 count)
{
	SRB2_ASSERT(parent_id > 0);
	SRB2_ASSERT(g_ap_item_info.find(parent_id) != g_ap_item_info.end());

	_progressive_parent = parent_id;
	_progressive_count = count;
}

void RRAP_LoadArchipelagoJSON(void)
{
	// This function already just runs once during startup,
	// so this should be a good nuff place to set data path.
	AP_SetDataPath(srb2home);

	bool found_any_manifest = false;

	for (UINT16 wad_id = 0; wad_id < mainwads; wad_id++)
	{
		if (wadfiles[wad_id]->type != RET_PK3)
		{
			continue;
		}

		UINT16 manifest_lump_id = W_CheckNumForFullNamePK3("archipelago/!manifest.json", wad_id, 0);
		if (manifest_lump_id == INT16_MAX)
		{
			continue;
		}

		CONS_Printf("Reading Archipelago manifest...\n");

		size_t manifest_lump_len = W_LumpLengthPwad(wad_id, manifest_lump_id);
		const char *manifest_lump = static_cast<const char *>( W_CacheLumpNumPwad(wad_id, manifest_lump_id, PU_CACHE) );

		srb2::String manifest_str { manifest_lump, manifest_lump_len };
		srb2::JsonObject manifest_obj = srb2::JsonValue::from_json_string(manifest_str).as_object();

		try
		{
			srb2::JsonArray file_list = manifest_obj.at("files").as_array();

			for (size_t i = 0; i < file_list.size(); i++)
			{
				srb2::String file_name = file_list.at(i).get<srb2::String>();
				srb2::String file_path = srb2::format("archipelago/{}", file_name);
				UINT16 json_lump_id = W_CheckNumForFullNamePK3(file_path.c_str(), wad_id, 0);

				if (json_lump_id == INT16_MAX)
				{
					throw std::runtime_error(srb2::format("could not find file in '{}'", file_path));
				}

				CONS_Printf("  Reading AP JSON @ %s...\n", file_name.c_str());
				RRAP_LoadArchipelagoJSONLump(wad_id, json_lump_id);
			}
		}
		catch (const std::exception& ex)
		{
			I_Error("Archipelago manifest parse error: %s", ex.what());
		}

		found_any_manifest = true;
	}

	if (!found_any_manifest)
	{
		I_Error("Could not find Archipelago manifest file");
	}

	// Afterwards pass
	for (auto& [_, item] : g_ap_item_info)
	{
		item.update_children();
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

UINT16 RRAP_ItemClassToSkinColor(UINT8 item_class)
{
	if (item_class & AP_CLASSIFICATION_PROGRESSION)
	{
		return SKINCOLOR_PURPLE;
	}
	else if (item_class & AP_CLASSIFICATION_USEFUL)
	{
		return SKINCOLOR_BLUE;
	}
	else if (item_class & AP_CLASSIFICATION_TRAP)
	{
		return SKINCOLOR_RED;
	}
	else
	{
		return SKINCOLOR_CERULEAN;
	}
}

UINT8 RRAP_ItemClassToTextColor(UINT8 item_class)
{
	if (item_class & AP_CLASSIFICATION_PROGRESSION)
	{
		return 0x81; // purplemap
	}
	else if (item_class & AP_CLASSIFICATION_USEFUL)
	{
		return 0x84; // bluemap 
	}
	else if (item_class & AP_CLASSIFICATION_TRAP)
	{
		return 0x85; // redmap
	}
	else
	{
		return 0x88; // skymap
	}
}

UINT8 RRAP_ItemClassToStars(UINT8 item_class)
{
	// Color-blind friendly iconography

	if (item_class & AP_CLASSIFICATION_PROGRESSION)
	{
		return 2;
	}
	else if (item_class & AP_CLASSIFICATION_USEFUL)
	{
		return 1; 
	}
	else
	{
		return 0;
	}
}

boolean RRAP_LocationAvailable(rrap_location_t *location)
{
	if (!location)
	{
		return false;
	}

	return location->available();
}

boolean RRAP_LocationAchieved(rrap_location_t *location)
{
	if (!location)
	{
		return false;
	}

	return location->achieved();
}

char *RRAP_LocationLabel(rrap_location_t *location)
{
	if (!location)
	{
		return nullptr;
	}

	return Z_StrDup( location->label().c_str() );
}

UINT8 RRAP_LocationPrisonCDCount(rrap_location_t *location)
{
	if (!location)
	{
		return 0;
	}

	return location->prison_cd_count();
}

INT32 RRAP_LocationSprayCanMapID(rrap_location_t *location)
{
	if (!location)
	{
		return 0;
	}

	return location->spray_can_map_id();
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

char *RRAP_LocationDisplayItemPlayer(rrap_location_t *location)
{
	if (!location)
	{
		return nullptr;
	}

	if (location->display_item_player().empty())
	{
		return nullptr;
	}

	return Z_StrDup( location->display_item_player().c_str() );
}

UINT8 RRAP_LocationDisplayItemClass(rrap_location_t *location)
{
	if (!location)
	{
		return AP_CLASSIFICATION_FILLER;
	}

	return location->display_item_class();
}

boolean RRAP_LocationDisplayItemIsOffWorld(rrap_location_t *location)
{
	if (!location)
	{
		return true;
	}

	return location->display_item_offworld();
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

UINT32 RRAP_ItemReceived(rrap_item_t *item)
{
	if (!item)
	{
		// If the item is not valid, then
		// just assume that we have it.
		return 1;
	}

	return item->received(true);
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

INT32 RRAP_ItemToColorId(rrap_item_t *item)
{
	if (!item)
	{
		return SKINCOLOR_NONE;
	}

	return item->color_id();
}

INT32 RRAP_ItemDisplayType(rrap_item_t *item)
{
	if (!item)
	{
		return SECRET_NONE;
	}

	return item->display_type(true);
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

UINT32 RRAP_CapCharacterWins(UINT32 input)
{
	if (g_character_wins_count <= 0 || input < g_character_wins_count)
	{
		return input;
	}

	return g_character_wins_count;
}

boolean RRAP_SimplifyMapAccess(void)
{
	return g_simple_map_access;
}

UINT16 RRAP_ChaoKeyCount(void)
{
	constexpr INT64 key_id = 10000; // TODO: don't hardcode
	rrap_item_t key_item = g_ap_item_info[key_id];
	INT32 num_keys = (key_item.received() + gamedata->chaokeys) - gamedata->keysused;
	return std::clamp<UINT16>(num_keys, 0, GDMAX_CHAOKEYS);
}

UINT16 RRAP_ChaoKeygenRate(void)
{
	return g_keygen_rate;
}

void RRAP_PopulateChallengeGrid(void)
{
	INT64 i, j;
	srb2::Vector<INT64> selection_small;
	srb2::Vector<INT64> selection_big;
	UINT64 num_empty = 0;
	int big_compact = 2;

	P_SetRandSeed(PR_AP_CHALLENGES, g_ap_seed_hash);

	if (gamedata->ap_challengegrid != nullptr)
	{
		// todo tweak your grid if unlocks are changed
		return;
	}

	// Go through unlockables
	for (auto& [id, location] : g_ap_location_info)
	{
		if (!location.available())
		{
			continue;
		}

		if (location.is_big_tile())
		{
			selection_big.emplace_back(id);
			//CONS_Printf(" found %li (LARGE)\n", id);
		}
		else
		{
			selection_small.emplace_back(id);
			//CONS_Printf(" found %li\n", id);
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

		/*
		CONS_Printf(
			"%lu major unlocks means width of %lu, numempty of %lu\n",
			selection_big.size(),
			gamedata->ap_challengegridwidth,
			num_empty
		);
		*/
	}

	if (selection_small.size() > num_empty)
	{
		// Getting the number of extra columns to store normal unlocks
		UINT64 temp = ((selection_small.size() - num_empty) + (CHALLENGEGRIDHEIGHT - 1)) / CHALLENGEGRIDHEIGHT;
		gamedata->ap_challengegridwidth += temp;
		big_compact = 1;

		/*
		CONS_Printf(
			"%lu normal unlocks means %lu extra entries, additional width of %lu\n",
			selection_small.size(),
			(selection_small.size() - num_empty),
			temp
		);
		*/
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

		/*
		CONS_Printf(
			" FORCING WIDTH HACK: %lu\n",
			min_width
		);
		*/
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

			j = P_RandomKey(PR_AP_CHALLENGES, num_spots);

			row = quick_check[j * 2 + 0];
			col = quick_check[j * 2 + 1];

			// We always take from selection_big in order, but the PLACEMENT is still random.
			INT64 placed = selection_big.back();
			selection_big.pop_back();

			//CONS_Printf("--- %li (LARGE) placed at (%li, %li)\n", placed, row, col);

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

					// Shuffle remaining so we can keep on using P_RandomKey
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

	//CONS_Printf(" %lu unlocks vs %lu empty spaces\n", selection_small.size(), num_empty);

	while (selection_small.size() < num_empty)
	{
		//CONS_Printf(" adding empty)\n");
		selection_small.emplace_back(0);
	}

	// Fill the remaining spots with random ordinary unlocks (and empties).
	for (i = 0; i < gamedata->ap_challengegridwidth * CHALLENGEGRIDHEIGHT; i++)
	{
		if (gamedata->ap_challengegrid[i] != 0)
		{
			continue;
		}

		j = P_RandomKey(PR_AP_CHALLENGES, selection_small.size()); // Get an entry

		INT64 placed = selection_small[j];
		selection_small.erase(selection_small.begin() + j);

		gamedata->ap_challengegrid[i] = placed; // Set that entry

		//CONS_Printf(" %li placed at (%li, %li)\n", placed, i / CHALLENGEGRIDHEIGHT, i % CHALLENGEGRIDHEIGHT);

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
		if (i <= 0 || !ref.available())
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
		if (!location.available())
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

boolean RRAP_TestGoal(void)
{
	if (g_goal_sent || g_goal_queued)
	{
		return false;
	}

	// Check goal condition
	UINT8 num_trophies = 0;
	cupheader_t *cup = kartcupheaders;
	while (cup)
	{
		if (cup->id >= basenumkartcupheaders)
		{
			cup = NULL;
			break;
		}

		boolean any_trophy = false;
		for (size_t i = 0; i < 4; i++)
		{
			cupwindata_t *windata = &cup->windata[i];

			if (windata->best_placement == 0)
			{
				// No trophy
				continue;
			}

			if (g_goal_trophy_level != 0
				&& g_goal_trophy_level < windata->best_placement)
			{
				// A trophy, but it's not good enough
				continue;
			}

			any_trophy = true;
			break;
		}

		if (any_trophy)
		{
			num_trophies++;
			if (num_trophies >= g_goal_num_trophies)
			{
				break;
			}
		}

		cup = cup->next;
	}

	return (num_trophies >= g_goal_num_trophies);
}

int RRAP_TestLocations(void)
{
	int response = 0;

	for (auto& [index, location] : g_ap_location_info)
	{
		if (!location.available())
		{
			continue;
		}

		if (location.checked() || location.check_pending())
		{
			continue;
		}

		if (!location.achieved())
		{
			continue;
		}

		location.queue_check();
		response++;
	}

	if (RRAP_TestGoal())
	{
		g_goal_queued = true;
		response++;
	}

	return response;
}

INT64 RRAP_GetNextCheckedLocation(boolean canskipchaokeys)
{
	// Go through unlockables
	for (auto& [id, location] : g_ap_location_info)
	{
		if (!location.available())
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
		UINT16 keygen_rate = RRAP_ChaoKeygenRate();

		if (keygen_rate > 0)
		{
			if (gamedata->chaokeys + gamedata->keyspending < GDMAX_CHAOKEYS)
			{
				gamedata->chaokeys += gamedata->keyspending;
				gamedata->pendingkeyroundoffset =
					(gamedata->pendingkeyroundoffset + gamedata->pendingkeyrounds)
					% keygen_rate;
			}
			else
			{
				gamedata->chaokeys = GDMAX_CHAOKEYS;
				gamedata->pendingkeyroundoffset = 0;
			}
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
		if (!location.available())
		{
			continue;
		}

		challengesmenu.unlockcount[CMC_TOTAL]++;

		if (!location.checked())
		{
			continue;
		}

		challengesmenu.unlockcount[CMC_UNLOCKED]++;

		if (location.achieved())
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
		if (!location.available())
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

void RRAP_CountItems(INT32 filter, INT64 *total, INT64 *count)
{
	for (auto& [id, item] : g_ap_item_info)
	{
		INT32 type = item.display_type();
		if (type == SECRET_NONE)
		{
			continue;
		}

		if (filter != SECRET_NONE && type != filter)
		{
			continue;
		}

		*total += 1;

		if (item.received(true) > 0)
		{
			*count += 1;
		}
	}
}

boolean RRAP_TryGoalSend(void)
{
	if (!g_goal_queued)
	{
		return false;
	}

	g_goal_queued = false;

	if (g_goal_sent)
	{
		return false;
	}

	AP_StoryComplete();
	g_goal_sent = true;

	return true;
}

void RRAP_LevelChanged(void)
{
	if (battleprisons && grandprixinfo.gp)
	{
		RRAP_PrisonEggCDMissed();
	}

	g_cd_missed_this_map = false;
}

void RRAP_PrisonEggCDMissed(void)
{
	if (g_cd_missed_this_map)
	{
		return;
	}

	gamedata->missed_prison_egg_pickups++;
	g_cd_missed_this_map = true;

	UINT64 hint_cd = gamedata->numprisoneggpickups + gamedata->missed_prison_egg_pickups;
	if (hint_cd == 0)
	{
		return;
	}

	for (auto& [index, location] : g_ap_location_info)
	{
		if (!location.available())
		{
			continue;
		}

		UINT8 requirement = location.prison_cd_count();
		if (requirement != hint_cd)
		{
			continue;
		}

		std::set<INT64> scout_ids = {index};
		AP_SendLocationScouts(scout_ids, 2);
	}
}

void RRAP_TickMessages(void)
{
	if (AP_IsMessagePending())
	{
		AP_Message *msg = AP_GetLatestMessage();
		HU_AddChatText(va("\x89[AP] \x80%s", msg->text.c_str()), Playing());
		AP_ClearLatestMessage();
	}
}

void RRAP_Say(const char *msg)
{
	AP_Say(msg);
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
	std::string gamedata_name = g_ap_slot + "_" + g_ap_seed;

	// Convert to lowercase & discard illegal chars
	std::transform(
		gamedata_name.begin(), gamedata_name.end(), gamedata_name.begin(),
		[](unsigned char c)
		{
			unsigned char lwr = std::tolower(c);
			return ((g_ap_file_legal_chars.find(lwr) == std::string::npos) ? '-' : lwr);
		}
	);

	const size_t file_name_max = sizeof(gamedatafilename) - g_ap_file_ext.size();
	if (gamedata_name.size() >= file_name_max)
	{
		// Will overflow our C-friendly array?
		// Clamp it, I guess...
		gamedata_name.resize(file_name_max - 1);
	}

	// add extension
	std::string gamedata_file = gamedata_name + g_ap_file_ext;

	// Copy to the C code...
	strlcpy(gamedatafilename, gamedata_file.c_str(), sizeof(gamedatafilename));
	gamedatafilename[std::min(gamedata_file.size(), sizeof(gamedatafilename) - 1)] = '\0';

	strlcpy(timeattackfolder, gamedata_name.c_str(), sizeof(timeattackfolder));
	timeattackfolder[std::min(gamedata_name.size(), sizeof(timeattackfolder) - 1)] = '\0';

	strcpy(savegamename, gamedata_name.c_str());
	strlcat(savegamename, "%u.ssg", sizeof(savegamename));
	// can't use sprintf since there is %u in savegamename
	strcatbf(savegamename, srb2home, PATHSEP);

	strcpy(gpbackup, va("gp%s.bkp", gamedata_name.c_str()));
	strcatbf(gpbackup, srb2home, PATHSEP);

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
		CONS_Alert(
			CONS_WARNING,
			"Could not receive invalid AP item ID [%li]\n",
			item_id
		);
		return;
	}

	g_ap_item_info[item_id].receive();

	if (should_notify && Playing())
	{
		srb2::String msg = srb2::format("Got '{}'!", g_ap_item_info[item_id].name());
		K_AddMessage(msg.c_str(), false, false);
	}
}

static void RRAP_GotLocationChecked(int64_t location_id)
{
	if (g_ap_location_info.find(location_id) == g_ap_location_info.end())
	{
		CONS_Alert(
			CONS_WARNING,
			"Could not check invalid AP location ID [%li]\n",
			location_id
		);
		return;
	}

	g_ap_location_info[location_id].immediate_check(true);
}

static void RRAP_GotLocationInfo(std::vector<AP_NetworkItem> network_items)
{
	for (auto& net_item : network_items)
	{
		if (g_ap_location_info.find(net_item.location) == g_ap_location_info.end())
		{
			CONS_Alert(
				CONS_WARNING,
				"Could not set location info for invalid AP location ID [%li]\n",
				net_item.location
			);
			return;
		}

		g_ap_location_info[net_item.location].update_displayed_item(
			net_item.itemName,
			net_item.item,
			net_item.playerName,
			net_item.flags
		);
	}
}

static void RRAP_SlotData_APWorldVersion(std::string raw_string)
{
	srb2::String room_version = srb2::JsonValue::from_json_string(raw_string).get<srb2::String>();
	srb2::String our_version = comptag;

	// TODO: actually comply with semver instead of doing direct comparison
	if (our_version != room_version)
	{
		CONS_Alert(
			CONS_WARNING,
			"Our game's version is '%s', while the AP room's version is '%s'. Issues may occur!\n",
			our_version.c_str(),
			room_version.c_str()
		);
	}
}

static void RRAP_SlotData_CharWinsCount(int wins_count)
{
	if (wins_count < 0 || wins_count > 100)
	{
		CONS_Alert(
			CONS_WARNING,
			"Recieved invalid character_wins_count setting (expected 0 to 100, got %d). Resetting to 0, issues may occur!\n",
			wins_count
		);
		wins_count = 0;
	}

	g_character_wins_count = wins_count;
}

static void RRAP_SlotData_SimpleMapAccess(int toggle)
{
	g_simple_map_access = (bool)toggle;
}

static void RRAP_SlotData_KeygenRate(int rate)
{
	if (rate < 0)
	{
		CONS_Alert(
			CONS_WARNING,
			"Recieved invalid keygen_rate setting (expected >= 0, got %d). Resetting to %d, issues may occur!\n",
			rate, GDCONVERT_ROUNDSTOKEY
		);
		rate = GDCONVERT_ROUNDSTOKEY;
	}

	g_keygen_rate = rate;
}

static void RRAP_SlotData_GoalNumTrophies(int trophy_count)
{
	if (trophy_count < 1 || trophy_count > 30)
	{
		CONS_Alert(
			CONS_WARNING,
			"Recieved invalid goal_num_trophies setting (expected 1 to 30, got %d). Resetting to 14, issues may occur!\n",
			trophy_count
		);
		trophy_count = 14;
	}
	g_goal_num_trophies = trophy_count;
}

static void RRAP_SlotData_GoalTrophyLevel(int trophy_level)
{
	if (trophy_level < 0 || trophy_level > 3)
	{
		CONS_Alert(
			CONS_WARNING,
			"Recieved invalid goal_trophy_level setting (expected 0 to 3, got %d). Resetting to 0, issues may occur!\n",
			trophy_level
		);
		trophy_level = 0;
	}
	g_goal_trophy_level = trophy_level;
}

static void RRAP_UpdateList(srb2::Vector<srb2::String> &input, srb2::JsonArray &array)
{
	input.clear();

	for (auto &val : array)
	{ 
		srb2::String str = val.get<srb2::String>();
		input.emplace_back(str);
	}
}

static void RRAP_SlotData_GroupWhitelist(std::string raw_string)
{
	srb2::JsonArray array = srb2::JsonValue::from_json_string(raw_string).get<srb2::JsonArray>();
	RRAP_UpdateList(g_group_whitelist, array);
}

static void RRAP_SlotData_GroupBlacklist(std::string raw_string)
{
	srb2::JsonArray array = srb2::JsonValue::from_json_string(raw_string).get<srb2::JsonArray>();
	RRAP_UpdateList(g_group_blacklist, array);
}

static void RRAP_SlotData_NameWhitelist(std::string raw_string)
{
	srb2::JsonArray array = srb2::JsonValue::from_json_string(raw_string).get<srb2::JsonArray>();
	RRAP_UpdateList(g_name_whitelist, array);
}

static void RRAP_SlotData_NameBlacklist(std::string raw_string)
{
	srb2::JsonArray array = srb2::JsonValue::from_json_string(raw_string).get<srb2::JsonArray>();
	RRAP_UpdateList(g_name_blacklist, array);
}

static void RRAP_DrawConnectionStatus(void)
{
	tic_t tick = I_GetTime();
	int anim_time = ((tick / 4) & 15) + 16;
	constexpr UINT8 pal_start = 32;
 
	M_DrawGonerBack();

	M_DrawTextBox(BASEVIDWIDTH/2-128-8, BASEVIDHEIGHT-24-8, 32, 1);
	K_DrawGameControl(BASEVIDWIDTH/2, BASEVIDHEIGHT-24-24, 0, "Press <b_animated> or <x_animated> to abort", 1, HU_FONT, V_YELLOWMAP);

	for (int i = 0; i < 16; i++)
	{
		V_DrawFill(
			(BASEVIDWIDTH / 2 - 128) + (i * 16), BASEVIDHEIGHT - 24,
			16, 8,
			pal_start + ((anim_time - i) & 15)
		);
	}

	V_DrawCenteredString(BASEVIDWIDTH/2, BASEVIDHEIGHT-16-24, V_YELLOWMAP, "Connecting to Archipelago room...");
}

static int RRAP_StartupTick(void)
{
	AP_RoomInfo room;
	int room_error = AP_GetRoomInfo(&room);
	if (!room_error)
	{
		g_ap_seed = room.seed_name;
		g_ap_seed_hash = quickncasehash(g_ap_seed.c_str(), g_ap_seed.size());
		return 1;
	}

	static tic_t old_tic = 0;
	if (old_tic != I_GetTime())
	{
		I_OsPolling();

		// Needs to be updated here for M_DrawEggaChannelAlignable
		renderdeltatics = FRACUNIT;
		rendertimefrac = FRACUNIT;

		G_ResetAllDeviceResponding();

		for (; eventtail != eventhead; eventtail = (eventtail+1) & (MAXEVENTS-1))
		{
			HandleGamepadDeviceEvents(&events[eventtail]);
			G_MapEventsToControls(&events[eventtail]);
		}

#ifdef HAVE_THREADS
		I_lock_mutex(&k_menu_mutex);
#endif
		M_UpdateMenuCMD(0, true, false);

		constexpr UINT8 pid = 0;
		if (M_MenuBackPressed(pid))
		{
			return -1;
		}

		M_ScreenshotTicker();

#ifdef HAVE_THREADS
		I_unlock_mutex(k_menu_mutex);
#endif

		old_tic = I_GetTime();

		RRAP_DrawConnectionStatus();

		I_UpdateNoVsync(); // page flip or blit buffer

#ifdef HWRENDER
		// Only take screenshots after drawing.
		if (moviemode && rendermode == render_opengl)
			M_LegacySaveFrame();
		if (rendermode == render_opengl && takescreenshot)
			M_DoLegacyGLScreenShot();
#endif

		if ((moviemode || takescreenshot) && rendermode == render_soft)
			I_CaptureVideoFrame();

		S_UpdateSounds();
		S_UpdateClosedCaptions();
	}
	else
	{
		I_Sleep(cv_sleep.value);
		I_UpdateTime();
	}

	return 0;
}

static void RRAP_UpdateLocationsAvailable(void)
{
	for (auto& [_, location] : g_ap_location_info)
	{
		location.update_available();
	}
}

static void RRAP_Connect(void)
{
	if (g_ap_started)
	{
		g_ap_started = false;
		Command_ExitGame_f();
	}

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

	AP_RegisterSlotDataRawCallback("apworld_version", RRAP_SlotData_APWorldVersion);

	AP_RegisterSlotDataRawCallback("location_group_whitelist", RRAP_SlotData_GroupWhitelist);
	AP_RegisterSlotDataRawCallback("location_group_blacklist", RRAP_SlotData_GroupBlacklist);
	AP_RegisterSlotDataRawCallback("location_name_whitelist", RRAP_SlotData_NameWhitelist);
	AP_RegisterSlotDataRawCallback("location_name_blacklist", RRAP_SlotData_NameBlacklist);

	AP_RegisterSlotDataIntCallback("character_wins_count", RRAP_SlotData_CharWinsCount);
	AP_RegisterSlotDataIntCallback("simple_map_access", RRAP_SlotData_SimpleMapAccess);
	AP_RegisterSlotDataIntCallback("keygen_rate", RRAP_SlotData_KeygenRate);
	AP_RegisterSlotDataIntCallback("goal_num_trophies", RRAP_SlotData_GoalNumTrophies);
	AP_RegisterSlotDataIntCallback("goal_trophy_level", RRAP_SlotData_GoalTrophyLevel);

	AP_Start();

	int result = 0;
	while (result == 0)
	{
		result = RRAP_StartupTick();
	}

	if (result == 1)
	{
		g_ap_started = true;
		RRAP_UpdateLocationsAvailable();
		RRAP_InitGamedata();

		if (gamestate == GS_MENU || gamestate == GS_TITLESCREEN)
		{
			menuactive = false;
			I_UpdateMouseGrab();
			COM_BufAddText("playintro");
		}
	}
	else
	{
		// Error / cancel occurred.
		AP_Shutdown();
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

static void Command_AP_Say(void)
{
	if (COM_Argc() < 2 || *COM_Argv(1) == 0)
	{
		CONS_Printf("ap_say <message>: send a message to the Archipelago room\n");
		return;
	}

	RRAP_Say(COM_Argv(1));
}

static void Command_AP_BuildDescriptions(void)
{
	for (auto& [id, _] : g_ap_location_info)
	{
		char *description_c = M_BuildConditionSetString(id);
		srb2::String description = description_c;
		Z_Free(description_c);

		std::replace(description.begin(), description.end(), '\n', ' ');
		CONS_Printf("[%d]: \"%s\"\n", id, description.c_str());
	}
}

void D_RegisterArchipelagoCommands(void)
{
	COM_AddCommand("ap_connect", Command_AP_Connect);
	COM_AddCommand("ap_say", Command_AP_Say);
	COM_AddCommand("ap_builddescriptions", Command_AP_BuildDescriptions);
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
