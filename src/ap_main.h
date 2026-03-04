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

#include "core/string.h"
#ifdef __cplusplus
#include "core/hash_map.hpp"
#include "core/json.hpp"
#endif

#ifdef __cplusplus
extern "C" {
#endif

typedef enum
{
	CHECK_FALSE = 0,
	CHECK_PENDING,
	CHECK_TRUE
} rrap_location_checked_e;

#ifdef __cplusplus
} // extern "C"
#endif

#ifdef __cplusplus

class rrap_location_t
{
private:
	srb2::String _label;
	INT32 _condition_set_id;
	boolean _big_tile;
	rrap_location_checked_e _checked;

public:
	rrap_location_t() = default;
	rrap_location_t(INT64 index, srb2::JsonValue json);

	srb2::String label() const { return _label; }
	INT32 condition_set_id() const { return _condition_set_id; }
	boolean is_big_tile() const { return _big_tile; }
	rrap_location_checked_e checked() const { return _checked; }

	void set_checked(rrap_location_checked_e x)
	{
		_checked = x;
	}
};

class rrap_item_t
{
private:
	srb2::String _label;
	UINT16 _unlockable_id;
	boolean _received;

public:
	rrap_item_t() = default;
	rrap_item_t(INT64 index, srb2::JsonValue json);

	srb2::String label() const { return _label; }
	UINT16 unlockable_id() const { return _unlockable_id; }
	boolean recieved() const { return _received; }

	void set_recieved(boolean x)
	{
		_received = x;
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

boolean RRAP_ItemRecieved(rrap_item_t *item);
UINT16 RRAP_ItemToUnlockableId(rrap_item_t *item);

void RRAP_LoadArchipelagoJSON(void);
void RRAP_TickMessages(void);
void RRAP_ConnectFromMenu(int32_t choice);

void D_RegisterArchipelagoCommands();

#ifdef __cplusplus
} // extern "C"
#endif

#endif
