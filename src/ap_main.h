// DR. ROBOTNIK'S RING RACERS
//-----------------------------------------------------------------------------
// Copyright (C) 2025 by Kart Krew.
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

#define AP_BASE_ID (44330000)

#include "doomtype.h"

#ifdef __cplusplus
extern "C" {
#endif

extern boolean g_ap_started;

void RRAP_SetUnlocked(int64_t unlock_id);

void D_RegisterArchipelagoCommands(void);

#ifdef __cplusplus
} // extern "C"
#endif

#endif
