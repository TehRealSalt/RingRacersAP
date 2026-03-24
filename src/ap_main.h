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
/// \file  ap_main.h
/// \brief Archipelago connectivity

#ifndef __AP_MAIN__
#define __AP_MAIN__

#include "typedef.h"
#include "doomtype.h"
#include "doomdef.h"
#include "doomstat.h"
#include "m_cond.h"

#include "core/string.h"
#ifdef __cplusplus
#include "core/hash_map.hpp"
#include "core/json.hpp"
#endif

#define AP_CLASSIFICATION_FILLER 0b000
#define AP_CLASSIFICATION_PROGRESSION 0b001
#define AP_CLASSIFICATION_USEFUL 0b010
#define AP_CLASSIFICATION_TRAP 0b100

#ifdef __cplusplus

class rrap_location_t
{
private:
	INT64 _id;
	srb2::String _name;
	srb2::Vector<srb2::String> _tags;
	boolean _available;
	boolean _checked;
	boolean _check_pending;

	UINT16 _condition_set_id;
	UINT8 _prison_cd_count;
	INT32 _spray_can_map_id;
	boolean _big_tile;

	srb2::String _label;
	srb2::String _display_item_label;
	srb2::String _display_item_player;
	UINT8 _display_item_class;
	boolean _display_item_offworld;
	INT64 _display_item_id;

public:
	rrap_location_t() = default;
	rrap_location_t(srb2::JsonValue json);

	INT64 id() const { return _id; }
	srb2::String name() const { return _name; }
	boolean available() const { return _available; }
	boolean checked() const { return _checked; }
	boolean check_pending() const { return _check_pending; }

	UINT16 condition_set_id() const { return _condition_set_id; }
	UINT8 prison_cd_count() const { return _prison_cd_count; }
	INT32 spray_can_map_id() const { return _spray_can_map_id; }
	boolean is_big_tile() const { return _big_tile; }

	srb2::String label() const { return _label; }
	srb2::String display_item_label() const { return _display_item_label; }
	srb2::String display_item_player() const { return _display_item_player; }
	UINT8 display_item_class() const { return _display_item_class; }
	boolean display_item_offworld() const { return _display_item_offworld; }
	INT64 display_item_id() const { return _display_item_id; }

	void update_available();

	void immediate_check(bool skip_pending = false);
	void queue_check();

	void update_displayed_item(srb2::String label, INT64 item_id, srb2::String player, UINT8 flags);

	void unqueue_check()
	{
		_check_pending = false;
	}

	void on_clear()
	{
		_checked = false;
		_check_pending = false;
	}

	boolean achieved() const
	{
		UINT8 prison_cds = prison_cd_count();
		if (prison_cds > 0)
		{
			return (gamedata->numprisoneggpickups >= prison_cds);
		}

		INT32 spray_can_map = spray_can_map_id();
		if (spray_can_map > 0)
		{
			return mapheaderinfo[spray_can_map - 1]->records.spraycan;
		}

		UINT16 condition_set = condition_set_id();
		if (condition_set > 0)
		{
			return M_Achieved(condition_set - 1);
		}

		return false;
	}
};

class rrap_item_t
{
private:
	INT64 _id;
	srb2::String _name;
	INT32 _received;

	UINT16 _unlockable_id;
	INT32 _skin_id;
	INT32 _follower_id;
	INT32 _color_id;

	srb2::String _label;
	INT32 _display_type;
	srb2::String _display_icon;
	UINT16 _display_color;

public:
	rrap_item_t() = default;
	rrap_item_t(srb2::JsonValue json);

	INT64 id() const { return _id; }
	srb2::String name() const { return _name; }
	boolean recieved() const { return (_received > 0); }
	INT32 recieved_count() const { return _received; }

	UINT16 unlockable_id() const { return _unlockable_id; }
	INT32 skin_id() const { return _skin_id; }
	INT32 follower_id() const { return _follower_id; }
	INT32 color_id() const { return _color_id; }

	srb2::String label() const { return _label; }
	INT32 display_type() const { return _display_type; }
	srb2::String display_icon() const { return _display_icon; }
	UINT16 display_color() const { return _display_color; }

	void recieve()
	{
		_received += 1;
	}

	void on_clear()
	{
		_received = 0;
	}
};

#else

// C compatibility interface
struct rrap_location_t;
typedef struct rrap_location_t rrap_location_t;

struct rrap_item_t;
typedef struct rrap_item_t rrap_item_t;

#endif

#ifdef __cplusplus
extern "C" {
#endif

extern boolean g_ap_started;

rrap_location_t *RRAP_GetLocation(INT64 location_id);
rrap_item_t *RRAP_GetItem(INT64 item_id);
void RRAP_LoadArchipelagoJSON(void);

UINT16 RRAP_ItemClassToSkinColor(UINT8 item_class);
UINT8 RRAP_ItemClassToTextColor(UINT8 item_class);
UINT8 RRAP_ItemClassToStars(UINT8 item_class);

boolean RRAP_LocationAvailable(rrap_location_t *location);
boolean RRAP_LocationAchieved(rrap_location_t *location);
char *RRAP_LocationLabel(rrap_location_t *location);
UINT16 RRAP_LocationConditionSet(rrap_location_t *location);
UINT8 RRAP_LocationPrisonCDCount(rrap_location_t *location);
INT32 RRAP_LocationSprayCanMapID(rrap_location_t *location);
boolean RRAP_LocationIsBigTile(rrap_location_t *location);
boolean RRAP_LocationChecked(rrap_location_t *location);
boolean RRAP_LocationCheckPending(rrap_location_t *location);

char *RRAP_LocationDisplayItemLabel(rrap_location_t *location);
char *RRAP_LocationDisplayItemPlayer(rrap_location_t *location);
UINT8 RRAP_LocationDisplayItemClass(rrap_location_t *location);
boolean RRAP_LocationDisplayItemIsOffWorld(rrap_location_t *location);
rrap_item_t *RRAP_LocationDisplayItem(rrap_location_t *location);

void RRAP_LocationImmediateCheck(rrap_location_t *location);
void RRAP_LocationQueueCheck(rrap_location_t *location);
void RRAP_LocationUnqueueCheck(rrap_location_t *location);

char *RRAP_ItemLabel(rrap_item_t *item);
boolean RRAP_ItemRecieved(rrap_item_t *item);
UINT16 RRAP_ItemToUnlockableId(rrap_item_t *item);
INT32 RRAP_ItemToSkinId(rrap_item_t *item);
INT32 RRAP_ItemToFollowerId(rrap_item_t *item);
INT32 RRAP_ItemToColorId(rrap_item_t *item);

INT32 RRAP_ItemDisplayType(rrap_item_t *item);
char *RRAP_ItemDisplayIcon(rrap_item_t *item);
UINT16 RRAP_ItemDisplayColor(rrap_item_t *item);

void RRAP_PopulateChallengeGrid(void);
void RRAP_SanitiseChallengeGrid(void);

UINT32 RRAP_CapCharacterWins(UINT32 input);
boolean RRAP_SimplifyMapAccess(void);

int RRAP_TestLocations(void);
boolean RRAP_TryGoalSend(void);
INT64 RRAP_GetNextCheckedLocation(boolean canskipchaokeys);
void RRAP_ChallengesMenuCountPercent(void);
INT64 RRAP_ChallengesMenuRandomFocus(INT32 level);
void RRAP_CountItems(INT32 filter, INT64 *total, INT64 *count);

void RRAP_TickMessages(void);
void RRAP_Say(const char *msg);
void RRAP_ConnectFromMenu(int32_t choice);

void D_RegisterArchipelagoCommands();

#ifdef __cplusplus
} // extern "C"
#endif

#endif
