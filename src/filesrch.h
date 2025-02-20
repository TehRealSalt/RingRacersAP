// DR. ROBOTNIK'S RING RACERS
//-----------------------------------------------------------------------------
// Copyright (C) 2025 by Vivian "toastergrl" Grannell.
// Copyright (C) 2025 by Kart Krew.
// Copyright (C) 2020 by Sonic Team Junior.
// Copyright (C) 2000 by DooM Legacy Team.
//
// This program is free software distributed under the
// terms of the GNU General Public License, version 2.
// See the 'LICENSE' file for more details.
//-----------------------------------------------------------------------------
/// \file  filesrch.h
/// \brief Support to find files

#ifndef __FILESRCH_H__
#define __FILESRCH_H__

#include "doomdef.h"
#include "d_netfil.h"
#include "k_menu.h" // MAXSTRINGLENGTH

#ifdef __cplusplus
extern "C" {
#endif

extern consvar_t cv_addons_md5, cv_addons_showall, cv_addons_search_case, cv_addons_search_type;

/**	\brief	The filesearch function

	This function search files, manly WADs and return back the status of the file

	\param	filename	the file to look for
	\param	startpath	where to start look from
	\param	wantedmd5sum	want to check with MD5
	\param	completepath	want to return the complete path of the file?
	\param	maxsearchdepth	the max depth to search for the file

	\return	filestatus_t


*/

filestatus_t filesearch(char *filename, const char *startpath, const UINT8 *wantedmd5sum,
	boolean completepath, int maxsearchdepth);

#define menudepth 20

extern char menupath[1024];
extern size_t menupathindex[menudepth];
extern size_t menudepthleft;

extern char menusearch[MAXSTRINGLENGTH+1];

extern char **dirmenu;
extern size_t sizedirmenu;
extern size_t dir_on[menudepth];
extern UINT8 refreshdirmenu;
extern char *refreshdirname;

typedef enum
{
	EXT_FOLDER = 0,
	EXT_UP,
	EXT_NORESULTS,
	EXT_START,
	EXT_TXT = EXT_START,
	EXT_CFG,
	EXT_LOADSTART,
	EXT_WAD = EXT_LOADSTART,
#ifdef USE_KART
	EXT_KART,
#endif
	EXT_PK3,
	EXT_SOC,
	EXT_LUA,
	NUM_EXT,
	NUM_EXT_TABLE = NUM_EXT-EXT_START,
	EXT_LOADED = 0x80
	/*
	obviously there can only be 0x7F supported extensions in
	addons menu because we're cramming this into a char out of
	laziness/easy memory allocation (what's the difference?)
	and have stolen a bit to show whether it's loaded or not
	in practice the size of the data type is probably overkill
	toast 02/05/17
	*/
} ext_enum;

typedef enum
{
	DIR_TYPE = 0,
	DIR_LEN,
	DIR_STRING
} dirname_enum;

typedef enum
{
	REFRESHDIR_NORMAL = 1,
	REFRESHDIR_ADDFILE = 2,
	REFRESHDIR_WARNING = 4,
	REFRESHDIR_ERROR = 8,
	REFRESHDIR_NOTLOADED = 16,
	REFRESHDIR_MAX = 32,
	REFRESHDIR_GAMEDATA = 64
} refreshdir_enum;

void closefilemenu(boolean validsize);
void searchfilemenu(char *tempname);
boolean preparefilemenu(boolean samedepth, boolean replayhut);

#ifdef __cplusplus
} // extern "C"
#endif

#endif // __FILESRCH_H__
