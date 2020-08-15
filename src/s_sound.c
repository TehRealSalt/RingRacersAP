// SONIC ROBO BLAST 2
//-----------------------------------------------------------------------------
// Copyright (C) 1993-1996 by id Software, Inc.
// Copyright (C) 1998-2000 by DooM Legacy Team.
// Copyright (C) 1999-2020 by Sonic Team Junior.
//
// This program is free software distributed under the
// terms of the GNU General Public License, version 2.
// See the 'LICENSE' file for more details.
//-----------------------------------------------------------------------------
/// \file  s_sound.c
/// \brief System-independent sound and music routines

#include "doomdef.h"
#include "doomstat.h"
#include "command.h"
#include "g_game.h"
#include "m_argv.h"
#include "r_main.h" // R_PointToAngle2() used to calc stereo sep.
#include "r_skins.h" // for skins
#include "i_system.h"
#include "i_sound.h"
#include "s_sound.h"
#include "w_wad.h"
#include "z_zone.h"
#include "d_main.h"
#include "r_sky.h" // skyflatnum
#include "p_local.h" // camera info
#include "fastcmp.h"
#include "m_misc.h" // for tunes command
#include "m_cond.h" // for conditionsets
#include "lua_hook.h" // MusicChange hook

#ifdef HW3SOUND
// 3D Sound Interface
#include "hardware/hw3sound.h"
#else
static INT32 S_AdjustSoundParams(const mobj_t *listener, const mobj_t *source, INT32 *vol, INT32 *sep, INT32 *pitch, sfxinfo_t *sfxinfo);
#endif

CV_PossibleValue_t soundvolume_cons_t[] = {{0, "MIN"}, {31, "MAX"}, {0, NULL}};
static void SetChannelsNum(void);
static void Command_Tunes_f(void);
static void Command_RestartAudio_f(void);

// Sound system toggles
#ifndef NO_MIDI
static void GameMIDIMusic_OnChange(void);
#endif
static void GameSounds_OnChange(void);
static void GameDigiMusic_OnChange(void);
#ifndef NO_MIDI
static void MusicPref_OnChange(void);
#endif

static void PlayMusicIfUnfocused_OnChange(void);
static void PlaySoundIfUnfocused_OnChange(void);

#ifdef HAVE_OPENMPT
static void ModFilter_OnChange(void);
#endif

static lumpnum_t S_GetMusicLumpNum(const char *mname);

static boolean S_CheckQueue(void);

#if defined (_WINDOWS) && !defined (SURROUND) //&& defined (_X86_)
#define SURROUND
#endif

#ifdef _WINDOWS
consvar_t cv_samplerate = {"samplerate", "44100", 0, CV_Unsigned, NULL, 44100, NULL, NULL, 0, 0, NULL}; //Alam: For easy hacking?
#else
consvar_t cv_samplerate = {"samplerate", "22050", 0, CV_Unsigned, NULL, 22050, NULL, NULL, 0, 0, NULL}; //Alam: For easy hacking?
#endif

// stereo reverse
consvar_t stereoreverse = {"stereoreverse", "Off", CV_SAVE, CV_OnOff, NULL, 0, NULL, NULL, 0, 0, NULL};

// if true, all sounds are loaded at game startup
static consvar_t precachesound = {"precachesound", "Off", CV_SAVE, CV_OnOff, NULL, 0, NULL, NULL, 0, 0, NULL};

// actual general (maximum) sound & music volume, saved into the config
consvar_t cv_soundvolume = {"soundvolume", "18", CV_SAVE, soundvolume_cons_t, NULL, 0, NULL, NULL, 0, 0, NULL};
consvar_t cv_digmusicvolume = {"digmusicvolume", "18", CV_SAVE, soundvolume_cons_t, NULL, 0, NULL, NULL, 0, 0, NULL};

#ifndef NO_MIDI
consvar_t cv_midimusicvolume = {"midimusicvolume", "18", CV_SAVE, soundvolume_cons_t, NULL, 0, NULL, NULL, 0, 0, NULL};
#endif

// number of channels available
consvar_t cv_numChannels = {"snd_channels", "64", CV_SAVE|CV_CALL, CV_Unsigned, SetChannelsNum, 0, NULL, NULL, 0, 0, NULL};

consvar_t surround = {"surround", "Off", CV_SAVE, CV_OnOff, NULL, 0, NULL, NULL, 0, 0, NULL};

static void Captioning_OnChange(void)
{
	S_ResetCaptions();
	if (cv_closedcaptioning.value)
		S_StartSound(NULL, sfx_menu1);
}

consvar_t cv_closedcaptioning = {"closedcaptioning", "Off", CV_SAVE|CV_CALL, CV_OnOff, Captioning_OnChange, 0, NULL, NULL, 0, 0, NULL};

// Sound system toggles, saved into the config
consvar_t cv_gamedigimusic = {"digimusic", "On", CV_SAVE|CV_CALL|CV_NOINIT, CV_OnOff, GameDigiMusic_OnChange, 0, NULL, NULL, 0, 0, NULL};
#ifndef NO_MIDI
consvar_t cv_gamemidimusic = {"midimusic", "On", CV_SAVE|CV_CALL|CV_NOINIT, CV_OnOff, GameMIDIMusic_OnChange, 0, NULL, NULL, 0, 0, NULL};
#endif
consvar_t cv_gamesounds = {"sounds", "On", CV_SAVE|CV_CALL|CV_NOINIT, CV_OnOff, GameSounds_OnChange, 0, NULL, NULL, 0, 0, NULL};

#ifndef NO_MIDI
// Music preference
static CV_PossibleValue_t cons_musicpref_t[] = {
	{0, "Digital"},
	{1, "MIDI"},
	{0, NULL}
};
consvar_t cv_musicpref = {"musicpref", "Digital", CV_SAVE|CV_CALL|CV_NOINIT, cons_musicpref_t, MusicPref_OnChange, 0, NULL, NULL, 0, 0, NULL};
#endif

static CV_PossibleValue_t music_resync_threshold_cons_t[] = {
	{0,    "MIN"},
	{1000, "MAX"},
	{0, NULL}
};

consvar_t cv_music_resync_threshold = {"music_resync_threshold", "100", CV_SAVE|CV_CALL, music_resync_threshold_cons_t, I_UpdateSongLagThreshold, 0, NULL, NULL, 0, 0, NULL};
consvar_t cv_music_resync_powerups_only = {"music_resync_powerups_only", "No", CV_SAVE|CV_CALL, CV_YesNo, I_UpdateSongLagConditions, 0, NULL, NULL, 0, 0, NULL};

// Window focus sound sytem toggles
consvar_t cv_playmusicifunfocused = {"playmusicifunfocused",  "No", CV_SAVE|CV_CALL|CV_NOINIT, CV_YesNo, PlayMusicIfUnfocused_OnChange, 0, NULL, NULL, 0, 0, NULL};
consvar_t cv_playsoundifunfocused = {"playsoundsifunfocused", "No", CV_SAVE|CV_CALL|CV_NOINIT, CV_YesNo, PlaySoundIfUnfocused_OnChange, 0, NULL, NULL, 0, 0, NULL};

#ifdef HAVE_OPENMPT
openmpt_module *openmpt_mhandle = NULL;

static CV_PossibleValue_t interpolationfilter_cons_t[] = {{0, "Default"}, {1, "None"}, {2, "Linear"}, {4, "Cubic"}, {8, "Windowed sinc"}, {0, NULL}};
consvar_t cv_modfilter = {"modfilter", "0", CV_SAVE|CV_CALL, interpolationfilter_cons_t, ModFilter_OnChange, 0, NULL, NULL, 0, 0, NULL};

#endif

#define S_MAX_VOLUME 127

// when to clip out sounds
// Does not fit the large outdoor areas.
// added 2-2-98 in 8 bit volume control (before (1200*0x10000))
#define S_CLIPPING_DIST (1536*0x10000)

// Distance to origin when sounds should be maxed out.
// This should relate to movement clipping resolution
// (see BLOCKMAP handling).
// Originally: (200*0x10000).
// added 2-2-98 in 8 bit volume control (before (160*0x10000))
#define S_CLOSE_DIST (160*0x10000)

// added 2-2-98 in 8 bit volume control (before remove the +4)
#define S_ATTENUATOR ((S_CLIPPING_DIST-S_CLOSE_DIST)>>(FRACBITS+4))

// Adjustable by menu.
#define NORM_VOLUME snd_MaxVolume

#define NORM_PITCH 128
#define NORM_PRIORITY 64
#define NORM_SEP 128

#define S_PITCH_PERTURB 1
#define S_STEREO_SWING (96*0x10000)

#ifdef SURROUND
#define SURROUND_SEP -128
#endif

// percent attenuation from front to back
#define S_IFRACVOL 30

// the set of channels available
static channel_t *channels = NULL;
static INT32 numofchannels = 0;

caption_t closedcaptions[NUMCAPTIONS];

void S_ResetCaptions(void)
{
	UINT8 i;
	for (i = 0; i < NUMCAPTIONS; i++)
	{
		closedcaptions[i].c = NULL;
		closedcaptions[i].s = NULL;
		closedcaptions[i].t = 0;
		closedcaptions[i].b = 0;
	}
}

//
// Internals.
//
static void S_StopChannel(INT32 cnum);

//
// S_getChannel
//
// If none available, return -1. Otherwise channel #.
//
static INT32 S_getChannel(const void *origin, sfxinfo_t *sfxinfo)
{
	// channel number to use
	INT32 cnum;

	channel_t *c;

	// Find an open channel
	for (cnum = 0; cnum < numofchannels; cnum++)
	{
		if (!channels[cnum].sfxinfo)
			break;

		// Now checks if same sound is being played, rather
		// than just one sound per mobj
		else if (sfxinfo == channels[cnum].sfxinfo && (sfxinfo->pitch & SF_NOMULTIPLESOUND))
		{
			return -1;
			break;
		}
		else if (sfxinfo == channels[cnum].sfxinfo && sfxinfo->singularity == true)
		{
			S_StopChannel(cnum);
			break;
		}
		else if (origin && channels[cnum].origin == origin && channels[cnum].sfxinfo == sfxinfo)
		{
			if (sfxinfo->pitch & SF_NOINTERRUPT)
				return -1;
			else
				S_StopChannel(cnum);
			break;
		}
		else if (origin && channels[cnum].origin == origin
			&& channels[cnum].sfxinfo->name != sfxinfo->name
			&& (channels[cnum].sfxinfo->pitch & SF_TOTALLYSINGLE) && (sfxinfo->pitch & SF_TOTALLYSINGLE))
		{
			S_StopChannel(cnum);
			break;
		}
	}

	// None available
	if (cnum == numofchannels)
	{
		// Look for lower priority
		for (cnum = 0; cnum < numofchannels; cnum++)
			if (channels[cnum].sfxinfo->priority <= sfxinfo->priority)
				break;

		if (cnum == numofchannels)
		{
			// No lower priority. Sorry, Charlie.
			return -1;
		}
		else
		{
			// Otherwise, kick out lower priority.
			S_StopChannel(cnum);
		}
	}

	c = &channels[cnum];

	// channel is decided to be cnum.
	c->sfxinfo = sfxinfo;
	c->origin = origin;

	return cnum;
}

void S_RegisterSoundStuff(void)
{
	if (dedicated)
	{
		sound_disabled = true;
		return;
	}

	CV_RegisterVar(&stereoreverse);
	CV_RegisterVar(&precachesound);

	CV_RegisterVar(&surround);
	CV_RegisterVar(&cv_samplerate);
	CV_RegisterVar(&cv_playsoundifunfocused);
	CV_RegisterVar(&cv_playmusicifunfocused);
	CV_RegisterVar(&cv_gamesounds);
	CV_RegisterVar(&cv_gamedigimusic);
#ifndef NO_MIDI
	CV_RegisterVar(&cv_gamemidimusic);
	CV_RegisterVar(&cv_musicpref);
#endif

	CV_RegisterVar(&cv_music_resync_threshold);
	CV_RegisterVar(&cv_music_resync_powerups_only);

#ifdef HAVE_OPENMPT
	CV_RegisterVar(&cv_modfilter);
#endif
#ifdef HAVE_MIXERX
	CV_RegisterVar(&cv_midiplayer);
	CV_RegisterVar(&cv_midisoundfontpath);
	CV_RegisterVar(&cv_miditimiditypath);
#endif

	COM_AddCommand("tunes", Command_Tunes_f);
	COM_AddCommand("restartaudio", Command_RestartAudio_f);
}

static void SetChannelsNum(void)
{
	INT32 i;

	// Allocating the internal channels for mixing
	// (the maximum number of sounds rendered
	// simultaneously) within zone memory.
	if (channels)
		S_StopSounds();

	Z_Free(channels);
	channels = NULL;


	if (cv_numChannels.value == 999999999) //Alam_GBC: OH MY ROD!(ROD rimmiced with GOD!)
		CV_StealthSet(&cv_numChannels,cv_numChannels.defaultvalue);

#ifdef HW3SOUND
	if (hws_mode != HWS_DEFAULT_MODE)
	{
		HW3S_SetSourcesNum();
		return;
	}
#endif
	if (cv_numChannels.value)
		channels = (channel_t *)Z_Malloc(cv_numChannels.value * sizeof (channel_t), PU_STATIC, NULL);
	numofchannels = cv_numChannels.value;

	// Free all channels for use
	for (i = 0; i < numofchannels; i++)
		channels[i].sfxinfo = 0;

	S_ResetCaptions();
}


// Retrieve the lump number of sfx
//
lumpnum_t S_GetSfxLumpNum(sfxinfo_t *sfx)
{
	char namebuf[9];
	lumpnum_t sfxlump;

	sprintf(namebuf, "ds%s", sfx->name);

	sfxlump = W_CheckNumForName(namebuf);
	if (sfxlump != LUMPERROR)
		return sfxlump;

	strlcpy(namebuf, sfx->name, sizeof namebuf);

	sfxlump = W_CheckNumForName(namebuf);
	if (sfxlump != LUMPERROR)
		return sfxlump;

	return W_GetNumForName("dsthok");
}

//
// Sound Status
//

boolean S_SoundDisabled(void)
{
	return (
			sound_disabled ||
			( window_notinfocus && ! cv_playsoundifunfocused.value )
	);
}

// Stop all sounds, load level info, THEN start sounds.
void S_StopSounds(void)
{
	INT32 cnum;

#ifdef HW3SOUND
	if (hws_mode != HWS_DEFAULT_MODE)
	{
		HW3S_StopSounds();
		return;
	}
#endif

	// kill all playing sounds at start of level
	for (cnum = 0; cnum < numofchannels; cnum++)
		if (channels[cnum].sfxinfo)
			S_StopChannel(cnum);

	S_ResetCaptions();
}

void S_StopSoundByID(void *origin, sfxenum_t sfx_id)
{
	INT32 cnum;

	// Sounds without origin can have multiple sources, they shouldn't
	// be stopped by new sounds.
	if (!origin)
		return;
#ifdef HW3SOUND
	if (hws_mode != HWS_DEFAULT_MODE)
	{
		HW3S_StopSoundByID(origin, sfx_id);
		return;
	}
#endif
	for (cnum = 0; cnum < numofchannels; cnum++)
	{
		if (channels[cnum].sfxinfo == &S_sfx[sfx_id] && channels[cnum].origin == origin)
		{
			S_StopChannel(cnum);
			break;
		}
	}
}

void S_StopSoundByNum(sfxenum_t sfxnum)
{
	INT32 cnum;

#ifdef HW3SOUND
	if (hws_mode != HWS_DEFAULT_MODE)
	{
		HW3S_StopSoundByNum(sfxnum);
		return;
	}
#endif
	for (cnum = 0; cnum < numofchannels; cnum++)
	{
		if (channels[cnum].sfxinfo == &S_sfx[sfxnum])
		{
			S_StopChannel(cnum);
			break;
		}
	}
}

void S_StartCaption(sfxenum_t sfx_id, INT32 cnum, UINT16 lifespan)
{
	UINT8 i, set, moveup, start;
	boolean same = false;
	sfxinfo_t *sfx;

	if (!cv_closedcaptioning.value) // no captions at all
		return;

	// check for bogus sound #
	// I_Assert(sfx_id >= 0); -- allowing sfx_None; this shouldn't be allowed directly if S_StartCaption is ever exposed to Lua by itself
	I_Assert(sfx_id < NUMSFX);

	sfx = &S_sfx[sfx_id];

	if (sfx->caption[0] == '/') // no caption for this one
		return;

	start = ((closedcaptions[0].s && (closedcaptions[0].s-S_sfx == sfx_None)) ? 1 : 0);

	if (sfx_id)
	{
		for (i = start; i < (set = NUMCAPTIONS-1); i++)
		{
			same = ((sfx == closedcaptions[i].s) || (closedcaptions[i].s && fastcmp(sfx->caption, closedcaptions[i].s->caption)));
			if (same)
			{
				set = i;
				break;
			}
		}
	}
	else
	{
		set = 0;
		same = (closedcaptions[0].s == sfx);
	}

	moveup = 255;

	if (!same)
	{
		for (i = start; i < set; i++)
		{
			if (!(closedcaptions[i].c || closedcaptions[i].s) || (sfx->priority >= closedcaptions[i].s->priority))
			{
				set = i;
				if (closedcaptions[i].s && (sfx->priority >= closedcaptions[i].s->priority))
					moveup = i;
				break;
			}
		}
		for (i = NUMCAPTIONS-1; i > set; i--)
		{
			if (sfx == closedcaptions[i].s)
			{
				closedcaptions[i].c = NULL;
				closedcaptions[i].s = NULL;
				closedcaptions[i].t = 0;
				closedcaptions[i].b = 0;
			}
		}
	}

	if (moveup != 255)
	{
		for (i = moveup; i < NUMCAPTIONS-1; i++)
		{
			if (!(closedcaptions[i].c || closedcaptions[i].s))
				break;
		}
		for (; i > set; i--)
		{
			closedcaptions[i].c = closedcaptions[i-1].c;
			closedcaptions[i].s = closedcaptions[i-1].s;
			closedcaptions[i].t = closedcaptions[i-1].t;
			closedcaptions[i].b = closedcaptions[i-1].b;
		}
	}

	closedcaptions[set].c = ((cnum == -1) ? NULL : &channels[cnum]);
	closedcaptions[set].s = sfx;
	closedcaptions[set].t = lifespan;
	closedcaptions[set].b = 2; // bob
}

void S_StartSoundAtVolume(const void *origin_p, sfxenum_t sfx_id, INT32 volume)
{
	INT32 sep, pitch, priority, cnum;
	const sfxenum_t actual_id = sfx_id;
	sfxinfo_t *sfx;
	const boolean reverse = (stereoreverse.value ^ encoremode);
	const mobj_t *origin = (const mobj_t *)origin_p;

	listener_t listener  = {0,0,0,0};
	listener_t listener2 = {0,0,0,0};
	listener_t listener3 = {0,0,0,0};
	listener_t listener4 = {0,0,0,0};

	mobj_t *listenmobj = democam.soundmobj ? : players[displayplayers[0]].mo;
	mobj_t *listenmobj2 = NULL;
	mobj_t *listenmobj3 = NULL;
	mobj_t *listenmobj4 = NULL;

	if (S_SoundDisabled() || !sound_started)
		return;

	// Don't want a sound? Okay then...
	if (sfx_id == sfx_None)
		return;

	if (players[displayplayers[0]].awayviewtics)
		listenmobj = players[displayplayers[0]].awayviewmobj;

	if (r_splitscreen)
	{
		listenmobj2 = players[displayplayers[1]].mo;
		if (players[displayplayers[1]].awayviewtics)
			listenmobj2 = players[displayplayers[1]].awayviewmobj;

		if (r_splitscreen > 1)
		{
			listenmobj3 = players[displayplayers[2]].mo;
			if (players[displayplayers[2]].awayviewtics)
				listenmobj3 = players[displayplayers[2]].awayviewmobj;

			if (r_splitscreen > 2)
			{
				listenmobj4 = players[displayplayers[3]].mo;
				if (players[displayplayers[3]].awayviewtics)
					listenmobj4 = players[displayplayers[3]].awayviewmobj;
			}
		}
	}

#ifdef HW3SOUND
	if (hws_mode != HWS_DEFAULT_MODE)
	{
		HW3S_StartSound(origin, sfx_id);
		return;
	};
#endif

	if (camera[0].chase && !players[displayplayers[0]].awayviewtics)
	{
		listener.x = camera[0].x;
		listener.y = camera[0].y;
		listener.z = camera[0].z;
		listener.angle = camera[0].angle;
	}
	else if (listenmobj)
	{
		listener.x = listenmobj->x;
		listener.y = listenmobj->y;
		listener.z = listenmobj->z;
		listener.angle = listenmobj->angle;
	}
	else if (origin)
		return;

	if (listenmobj2)
	{
		if (camera[1].chase && !players[displayplayers[1]].awayviewtics)
		{
			listener2.x = camera[1].x;
			listener2.y = camera[1].y;
			listener2.z = camera[1].z;
			listener2.angle = camera[1].angle;
		}
		else
		{
			listener2.x = listenmobj2->x;
			listener2.y = listenmobj2->y;
			listener2.z = listenmobj2->z;
			listener2.angle = listenmobj2->angle;
		}
	}

	if (listenmobj3)
	{
		if (camera[2].chase && !players[displayplayers[2]].awayviewtics)
		{
			listener3.x = camera[2].x;
			listener3.y = camera[2].y;
			listener3.z = camera[2].z;
			listener3.angle = camera[2].angle;
		}
		else
		{
			listener3.x = listenmobj3->x;
			listener3.y = listenmobj3->y;
			listener3.z = listenmobj3->z;
			listener3.angle = listenmobj3->angle;
		}
	}

	if (listenmobj4)
	{
		if (camera[3].chase && !players[displayplayers[3]].awayviewtics)
		{
			listener4.x = camera[3].x;
			listener4.y = camera[3].y;
			listener4.z = camera[3].z;
			listener4.angle = camera[3].angle;
		}
		else
		{
			listener4.x = listenmobj4->x;
			listener4.y = listenmobj4->y;
			listener4.z = listenmobj4->z;
			listener4.angle = listenmobj4->angle;
		}
	}

	// check for bogus sound #
	I_Assert(sfx_id >= 1);
	I_Assert(sfx_id < NUMSFX);

	sfx = &S_sfx[sfx_id];

	if (sfx->skinsound != -1 && origin && origin->skin)
	{
		// redirect player sound to the sound in the skin table
		sfx_id = ((skin_t *)origin->skin)->soundsid[sfx->skinsound];
		sfx = &S_sfx[sfx_id];
	}

	// Initialize sound parameters
	pitch = NORM_PITCH;
	priority = NORM_PRIORITY;

	if (r_splitscreen && origin)
		volume = FixedDiv(volume<<FRACBITS, FixedSqrt((r_splitscreen+1)<<FRACBITS))>>FRACBITS;

	if (r_splitscreen && listenmobj2) // Copy the sound for the split player
	{
		// Check to see if it is audible, and if not, modify the params
		if (origin && origin != listenmobj2)
		{
			INT32 rc;
			rc = S_AdjustSoundParams(listenmobj2, origin, &volume, &sep, &pitch, sfx);

			if (!rc)
				goto dontplay; // Maybe the other player can hear it...

			if (origin->x == listener2.x && origin->y == listener2.y)
				sep = NORM_SEP;
		}
		else if (!origin)
			// Do not play origin-less sounds for the second player.
			// The first player will be able to hear it just fine,
			// we really don't want it playing twice.
			goto dontplay;
		else
			sep = NORM_SEP;

		// try to find a channel
		cnum = S_getChannel(origin, sfx);

		if (cnum < 0)
			return; // If there's no free channels, it's not gonna be free for player 1, either.

		// This is supposed to handle the loading/caching.
		// For some odd reason, the caching is done nearly
		// each time the sound is needed?

		// cache data if necessary
		// NOTE: set sfx->data NULL sfx->lump -1 to force a reload
		if (!sfx->data)
			sfx->data = I_GetSfx(sfx);

		// increase the usefulness
		if (sfx->usefulness++ < 0)
			sfx->usefulness = -1;

		// Avoid channel reverse if surround
		if (reverse
#ifdef SURROUND
			&& sep != SURROUND_SEP
#endif
		)
			sep = (~sep) & 255;

		// Assigns the handle to one of the channels in the
		// mix/output buffer.
		channels[cnum].handle = I_StartSound(sfx_id, volume, sep, pitch, priority, cnum);
	}

dontplay:

	if (r_splitscreen > 1 && listenmobj3) // Copy the sound for the third player
	{
		// Check to see if it is audible, and if not, modify the params
		if (origin && origin != listenmobj3)
		{
			INT32 rc;
			rc = S_AdjustSoundParams(listenmobj3, origin, &volume, &sep, &pitch, sfx);

			if (!rc)
				goto dontplay3; // Maybe the other player can hear it...

			if (origin->x == listener3.x && origin->y == listener3.y)
				sep = NORM_SEP;
		}
		else if (!origin)
			// Do not play origin-less sounds for the second player.
			// The first player will be able to hear it just fine,
			// we really don't want it playing twice.
			goto dontplay3;
		else
			sep = NORM_SEP;

		// try to find a channel
		cnum = S_getChannel(origin, sfx);

		if (cnum < 0)
			return; // If there's no free channels, it's not gonna be free for player 1, either.

		// This is supposed to handle the loading/caching.
		// For some odd reason, the caching is done nearly
		// each time the sound is needed?

		// cache data if necessary
		// NOTE: set sfx->data NULL sfx->lump -1 to force a reload
		if (!sfx->data)
			sfx->data = I_GetSfx(sfx);

		// increase the usefulness
		if (sfx->usefulness++ < 0)
			sfx->usefulness = -1;

		// Avoid channel reverse if surround
		if (reverse
#ifdef SURROUND
			&& sep != SURROUND_SEP
#endif
		)
			sep = (~sep) & 255;

		// Assigns the handle to one of the channels in the
		// mix/output buffer.
		channels[cnum].handle = I_StartSound(sfx_id, volume, sep, pitch, priority, cnum);
	}

dontplay3:

	if (r_splitscreen > 2 && listenmobj4) // Copy the sound for the split player
	{
		// Check to see if it is audible, and if not, modify the params
		if (origin && origin != listenmobj4)
		{
			INT32 rc;
			rc = S_AdjustSoundParams(listenmobj4, origin, &volume, &sep, &pitch, sfx);

			if (!rc)
				goto dontplay4; // Maybe the other player can hear it...

			if (origin->x == listener4.x && origin->y == listener4.y)
				sep = NORM_SEP;
		}
		else if (!origin)
			// Do not play origin-less sounds for the second player.
			// The first player will be able to hear it just fine,
			// we really don't want it playing twice.
			goto dontplay4;
		else
			sep = NORM_SEP;

		// try to find a channel
		cnum = S_getChannel(origin, sfx);

		if (cnum < 0)
			return; // If there's no free channels, it's not gonna be free for player 1, either.

		// This is supposed to handle the loading/caching.
		// For some odd reason, the caching is done nearly
		// each time the sound is needed?

		// cache data if necessary
		// NOTE: set sfx->data NULL sfx->lump -1 to force a reload
		if (!sfx->data)
			sfx->data = I_GetSfx(sfx);

		// increase the usefulness
		if (sfx->usefulness++ < 0)
			sfx->usefulness = -1;

		// Avoid channel reverse if surround
		if (reverse
#ifdef SURROUND
			&& sep != SURROUND_SEP
#endif
		)
			sep = (~sep) & 255;

		// Handle closed caption input.
		S_StartCaption(actual_id, cnum, MAXCAPTIONTICS);

		// Assigns the handle to one of the channels in the
		// mix/output buffer.
		channels[cnum].handle = I_StartSound(sfx_id, volume, sep, pitch, priority, cnum);
	}

dontplay4:

	// Check to see if it is audible, and if not, modify the params
	if (origin && origin != listenmobj)
	{
		INT32 rc;
		rc = S_AdjustSoundParams(listenmobj, origin, &volume, &sep, &pitch, sfx);

		if (!rc)
			return;

		if (origin->x == listener.x && origin->y == listener.y)
			sep = NORM_SEP;
	}
	else
		sep = NORM_SEP;

	// try to find a channel
	cnum = S_getChannel(origin, sfx);

	if (cnum < 0)
		return;

	// This is supposed to handle the loading/caching.
	// For some odd reason, the caching is done nearly
	// each time the sound is needed?

	// cache data if necessary
	// NOTE: set sfx->data NULL sfx->lump -1 to force a reload
	if (!sfx->data)
		sfx->data = I_GetSfx(sfx);

	// increase the usefulness
	if (sfx->usefulness++ < 0)
		sfx->usefulness = -1;

	// Avoid channel reverse if surround
	if (reverse
#ifdef SURROUND
		&& sep != SURROUND_SEP
#endif
	)
		sep = (~sep) & 255;

	// Handle closed caption input.
	S_StartCaption(actual_id, cnum, MAXCAPTIONTICS);

	// Assigns the handle to one of the channels in the
	// mix/output buffer.
	channels[cnum].handle = I_StartSound(sfx_id, volume, sep, pitch, priority, cnum);
}

void S_StartSound(const void *origin, sfxenum_t sfx_id)
{
	if (S_SoundDisabled())
		return;

	// the volume is handled 8 bits
#ifdef HW3SOUND
	if (hws_mode != HWS_DEFAULT_MODE)
		HW3S_StartSound(origin, sfx_id);
	else
#endif
		S_StartSoundAtVolume(origin, sfx_id, 255);
}

void S_StopSound(void *origin)
{
	INT32 cnum;

	// Sounds without origin can have multiple sources, they shouldn't
	// be stopped by new sounds.
	if (!origin)
		return;

#ifdef HW3SOUND
	if (hws_mode != HWS_DEFAULT_MODE)
	{
		HW3S_StopSound(origin);
		return;
	}
#endif
	for (cnum = 0; cnum < numofchannels; cnum++)
	{
		if (channels[cnum].sfxinfo && channels[cnum].origin == origin)
		{
			S_StopChannel(cnum);
			break;
		}
	}
}

//
// Updates music & sounds
//
static INT32 actualsfxvolume; // check for change through console
static INT32 actualdigmusicvolume;
#ifndef NO_MIDI
static INT32 actualmidimusicvolume;
#endif

void S_UpdateSounds(void)
{
	INT32 audible, cnum, volume, sep, pitch;
	channel_t *c;

	listener_t listener;
	listener_t listener2;
	listener_t listener3;
	listener_t listener4;

	mobj_t *listenmobj = democam.soundmobj ? : players[displayplayers[0]].mo;
	mobj_t *listenmobj2 = NULL;
	mobj_t *listenmobj3 = NULL;
	mobj_t *listenmobj4 = NULL;

	memset(&listener, 0, sizeof(listener_t));
	memset(&listener2, 0, sizeof(listener_t));
	memset(&listener3, 0, sizeof(listener_t));
	memset(&listener4, 0, sizeof(listener_t));

	// Update sound/music volumes, if changed manually at console
	if (actualsfxvolume != cv_soundvolume.value)
		S_SetSfxVolume (cv_soundvolume.value);
	if (actualdigmusicvolume != cv_digmusicvolume.value)
		S_SetDigMusicVolume (cv_digmusicvolume.value);
#ifndef NO_MIDI
	if (actualmidimusicvolume != cv_midimusicvolume.value)
		S_SetMIDIMusicVolume (cv_midimusicvolume.value);
#endif

	// We're done now, if we're not in a level.
	if (gamestate != GS_LEVEL)
	{
#ifndef NOMUMBLE
		// Stop Mumble cutting out. I'm sick of it.
		I_UpdateMumble(NULL, listener);
#endif

		goto notinlevel;
	}

	if (dedicated || sound_disabled)
		return;

	if (players[displayplayers[0]].awayviewtics)
		listenmobj = players[displayplayers[0]].awayviewmobj;

	if (r_splitscreen)
	{
		listenmobj2 = players[displayplayers[1]].mo;
		if (players[displayplayers[1]].awayviewtics)
			listenmobj2 = players[displayplayers[1]].awayviewmobj;

		if (r_splitscreen > 1)
		{
			listenmobj3 = players[displayplayers[2]].mo;
			if (players[displayplayers[2]].awayviewtics)
				listenmobj3 = players[displayplayers[2]].awayviewmobj;

			if (r_splitscreen > 2)
			{
				listenmobj4 = players[displayplayers[3]].mo;
				if (players[displayplayers[3]].awayviewtics)
					listenmobj4 = players[displayplayers[3]].awayviewmobj;
			}
		}
	}

	if (camera[0].chase && !players[displayplayers[0]].awayviewtics)
	{
		listener.x = camera[0].x;
		listener.y = camera[0].y;
		listener.z = camera[0].z;
		listener.angle = camera[0].angle;
	}
	else if (listenmobj)
	{
		listener.x = listenmobj->x;
		listener.y = listenmobj->y;
		listener.z = listenmobj->z;
		listener.angle = listenmobj->angle;
	}

#ifndef NOMUMBLE
	I_UpdateMumble(players[consoleplayer].mo, listener);
#endif

#ifdef HW3SOUND
	if (hws_mode != HWS_DEFAULT_MODE)
	{
		HW3S_UpdateSources();
		goto notinlevel;
	}
#endif

	if (listenmobj2)
	{
		if (camera[1].chase && !players[displayplayers[1]].awayviewtics)
		{
			listener2.x = camera[1].x;
			listener2.y = camera[1].y;
			listener2.z = camera[1].z;
			listener2.angle = camera[1].angle;
		}
		else
		{
			listener2.x = listenmobj2->x;
			listener2.y = listenmobj2->y;
			listener2.z = listenmobj2->z;
			listener2.angle = listenmobj2->angle;
		}
	}

	if (listenmobj3)
	{
		if (camera[2].chase && !players[displayplayers[2]].awayviewtics)
		{
			listener3.x = camera[2].x;
			listener3.y = camera[2].y;
			listener3.z = camera[2].z;
			listener3.angle = camera[2].angle;
		}
		else
		{
			listener3.x = listenmobj3->x;
			listener3.y = listenmobj3->y;
			listener3.z = listenmobj3->z;
			listener3.angle = listenmobj3->angle;
		}
	}

	if (listenmobj4)
	{
		if (camera[3].chase && !players[displayplayers[3]].awayviewtics)
		{
			listener4.x = camera[3].x;
			listener4.y = camera[3].y;
			listener4.z = camera[3].z;
			listener4.angle = camera[3].angle;
		}
		else
		{
			listener4.x = listenmobj4->x;
			listener4.y = listenmobj4->y;
			listener4.z = listenmobj4->z;
			listener4.angle = listenmobj4->angle;
		}
	}

	for (cnum = 0; cnum < numofchannels; cnum++)
	{
		c = &channels[cnum];

		if (c->sfxinfo)
		{
			if (I_SoundIsPlaying(c->handle))
			{
				// initialize parameters
				volume = 255; // 8 bits internal volume precision
				pitch = NORM_PITCH;
				sep = NORM_SEP;

				if (r_splitscreen && c->origin)
					volume = FixedDiv(volume<<FRACBITS, FixedSqrt((r_splitscreen+1)<<FRACBITS))>>FRACBITS;

				// check non-local sounds for distance clipping
				//  or modify their params
				if (c->origin && ((c->origin != players[displayplayers[0]].mo)
					|| (r_splitscreen && c->origin != players[displayplayers[1]].mo)
					|| (r_splitscreen > 1 && c->origin != players[displayplayers[2]].mo)
					|| (r_splitscreen > 2 && c->origin != players[displayplayers[3]].mo)))
				{
					// Whomever is closer gets the sound, but only in splitscreen.
					if (r_splitscreen)
					{
						const mobj_t *soundmobj = c->origin;
						fixed_t recdist = -1;
						INT32 i, p = -1;

						for (i = 0; i <= r_splitscreen; i++)
						{
							fixed_t thisdist = -1;

							if (i == 0 && listenmobj)
								thisdist = P_AproxDistance(listener.x-soundmobj->x, listener.y-soundmobj->y);
							else if (i == 1 && listenmobj2)
								thisdist = P_AproxDistance(listener2.x-soundmobj->x, listener2.y-soundmobj->y);
							else if (i == 2 && listenmobj3)
								thisdist = P_AproxDistance(listener3.x-soundmobj->x, listener3.y-soundmobj->y);
							else if (i == 3 && listenmobj4)
								thisdist = P_AproxDistance(listener4.x-soundmobj->x, listener4.y-soundmobj->y);
							else
								continue;

							if (recdist == -1 || (thisdist != -1 && thisdist < recdist))
							{
								recdist = thisdist;
								p = i;
							}
						}

						if (p != -1)
						{
							if (p == 1)
							{
								// Player 2 gets the sound
								audible = S_AdjustSoundParams(listenmobj2, c->origin, &volume, &sep, &pitch,
									c->sfxinfo);
							}
							else if (p == 2)
							{
								// Player 3 gets the sound
								audible = S_AdjustSoundParams(listenmobj3, c->origin, &volume, &sep, &pitch,
								c->sfxinfo);
							}
							else if (p == 3)
							{
								// Player 4 gets the sound
								audible = S_AdjustSoundParams(listenmobj4, c->origin, &volume, &sep, &pitch,
									c->sfxinfo);
							}
							else
							{
								// Player 1 gets the sound
								audible = S_AdjustSoundParams(listenmobj, c->origin, &volume, &sep, &pitch,
									c->sfxinfo);
							}

							if (audible)
								I_UpdateSoundParams(c->handle, volume, sep, pitch);
							else
								S_StopChannel(cnum);
						}
					}
					else if (listenmobj && !r_splitscreen)
					{
						// In the case of a single player, he or she always should get updated sound.
						audible = S_AdjustSoundParams(listenmobj, c->origin, &volume, &sep, &pitch,
							c->sfxinfo);

						if (audible)
							I_UpdateSoundParams(c->handle, volume, sep, pitch);
						else
							S_StopChannel(cnum);
					}
				}
			}
			else
			{
				// if channel is allocated but sound has stopped, free it
				S_StopChannel(cnum);
			}
		}
	}

notinlevel:
	I_UpdateSound();
}

void S_UpdateClosedCaptions(void)
{
	UINT8 i;
	boolean gamestopped = (paused || P_AutoPause());
	for (i = 0; i < NUMCAPTIONS; i++) // update captions
	{
		if (!closedcaptions[i].s)
			continue;

		if (i == 0 && (closedcaptions[0].s-S_sfx == sfx_None) && gamestopped)
			continue;

		if (!(--closedcaptions[i].t))
		{
			closedcaptions[i].c = NULL;
			closedcaptions[i].s = NULL;
		}
		else if (closedcaptions[i].c && !I_SoundIsPlaying(closedcaptions[i].c->handle))
		{
			closedcaptions[i].c = NULL;
			if (closedcaptions[i].t > CAPTIONFADETICS)
				closedcaptions[i].t = CAPTIONFADETICS;
		}
	}
}

void S_SetSfxVolume(INT32 volume)
{
	if (volume < 0 || volume > 31)
		CONS_Alert(CONS_WARNING, "sfxvolume should be between 0-31\n");

	CV_SetValue(&cv_soundvolume, volume&0x1F);
	actualsfxvolume = cv_soundvolume.value; // check for change of var

#ifdef HW3SOUND
	hws_mode == HWS_DEFAULT_MODE ? I_SetSfxVolume(volume&0x1F) : HW3S_SetSfxVolume(volume&0x1F);
#else
	// now hardware volume
	I_SetSfxVolume(volume&0x1F);
#endif
}

void S_ClearSfx(void)
{
#ifndef DJGPPDOS
	size_t i;
	for (i = 1; i < NUMSFX; i++)
		I_FreeSfx(S_sfx + i);
#endif
}

static void S_StopChannel(INT32 cnum)
{
	INT32 i;
	channel_t *c = &channels[cnum];

	if (c->sfxinfo)
	{
		// stop the sound playing
		if (I_SoundIsPlaying(c->handle))
			I_StopSound(c->handle);

		// check to see
		//  if other channels are playing the sound
		for (i = 0; i < numofchannels; i++)
			if (cnum != i && c->sfxinfo == channels[i].sfxinfo)
				break;

		// degrade usefulness of sound data
		c->sfxinfo->usefulness--;

		c->sfxinfo = 0;
	}
}

//
// S_CalculateSoundDistance
//
// Calculates the distance between two points for a sound.
// Clips the distance to prevent overflow.
//
fixed_t S_CalculateSoundDistance(fixed_t sx1, fixed_t sy1, fixed_t sz1, fixed_t sx2, fixed_t sy2, fixed_t sz2)
{
	fixed_t approx_dist, adx, ady;

	// calculate the distance to sound origin and clip it if necessary
	adx = abs((sx1>>FRACBITS) - (sx2>>FRACBITS));
	ady = abs((sy1>>FRACBITS) - (sy2>>FRACBITS));

	// From _GG1_ p.428. Approx. euclidian distance fast.
	// Take Z into account
	adx = adx + ady - ((adx < ady ? adx : ady)>>1);
	ady = abs((sz1>>FRACBITS) - (sz2>>FRACBITS));
	approx_dist = adx + ady - ((adx < ady ? adx : ady)>>1);

	if (approx_dist >= FRACUNIT/2)
		approx_dist = FRACUNIT/2-1;

	approx_dist <<= FRACBITS;

	return FixedDiv(approx_dist, mapobjectscale); // approx_dist
}

//
// Changes volume, stereo-separation, and pitch variables
// from the norm of a sound effect to be played.
// If the sound is not audible, returns a 0.
// Otherwise, modifies parameters and returns 1.
//
INT32 S_AdjustSoundParams(const mobj_t *listener, const mobj_t *source, INT32 *vol, INT32 *sep, INT32 *pitch,
	sfxinfo_t *sfxinfo)
{
	fixed_t approx_dist;
	angle_t angle;

	listener_t listensource;

	const boolean reverse = (stereoreverse.value ^ encoremode);

	(void)pitch;
	if (!listener)
		return false;

	if (listener == players[displayplayers[0]].mo && camera[0].chase)
	{
		listensource.x = camera[0].x;
		listensource.y = camera[0].y;
		listensource.z = camera[0].z;
		listensource.angle = camera[0].angle;
	}
	else if (r_splitscreen && listener == players[displayplayers[1]].mo && camera[1].chase)
	{
		listensource.x = camera[1].x;
		listensource.y = camera[1].y;
		listensource.z = camera[1].z;
		listensource.angle = camera[1].angle;
	}
	else if (r_splitscreen > 1 && listener == players[displayplayers[2]].mo && camera[2].chase)
	{
		listensource.x = camera[2].x;
		listensource.y = camera[2].y;
		listensource.z = camera[2].z;
		listensource.angle = camera[2].angle;
	}
	else if (r_splitscreen > 2 && listener == players[displayplayers[3]].mo && camera[3].chase)
	{
		listensource.x = camera[3].x;
		listensource.y = camera[3].y;
		listensource.z = camera[3].z;
		listensource.angle = camera[3].angle;
	}
	else
	{
		listensource.x = listener->x;
		listensource.y = listener->y;
		listensource.z = listener->z;
		listensource.angle = listener->angle;
	}

	if (sfxinfo->pitch & SF_OUTSIDESOUND) // Rain special case
	{
		fixed_t x, y, yl, yh, xl, xh, newdist;

		if (R_PointInSubsector(listensource.x, listensource.y)->sector->ceilingpic == skyflatnum)
			approx_dist = 0;
		else
		{
			// Essentially check in a 1024 unit radius of the player for an outdoor area.
			yl = listensource.y - 1024*FRACUNIT;
			yh = listensource.y + 1024*FRACUNIT;
			xl = listensource.x - 1024*FRACUNIT;
			xh = listensource.x + 1024*FRACUNIT;
			approx_dist = 1024*FRACUNIT;
			for (y = yl; y <= yh; y += FRACUNIT*64)
				for (x = xl; x <= xh; x += FRACUNIT*64)
				{
					if (R_PointInSubsector(x, y)->sector->ceilingpic == skyflatnum)
					{
						// Found the outdoors!
						newdist = S_CalculateSoundDistance(listensource.x, listensource.y, 0, x, y, 0);
						if (newdist < approx_dist)
						{
							approx_dist = newdist;
						}
					}
				}
		}
	}
	else
	{
		approx_dist = S_CalculateSoundDistance(listensource.x, listensource.y, listensource.z,
												source->x, source->y, source->z);
	}

	// Ring loss, deaths, etc, should all be heard louder.
	if (sfxinfo->pitch & SF_X8AWAYSOUND)
		approx_dist = FixedDiv(approx_dist,8*FRACUNIT);

	// Combine 8XAWAYSOUND with 4XAWAYSOUND and get.... 32XAWAYSOUND?
	if (sfxinfo->pitch & SF_X4AWAYSOUND)
		approx_dist = FixedDiv(approx_dist,4*FRACUNIT);

	if (sfxinfo->pitch & SF_X2AWAYSOUND)
		approx_dist = FixedDiv(approx_dist,2*FRACUNIT);

	if (approx_dist > S_CLIPPING_DIST)
		return 0;

	// angle of source to listener
	angle = R_PointToAngle2(listensource.x, listensource.y, source->x, source->y);

	if (angle > listensource.angle)
		angle = angle - listensource.angle;
	else
		angle = angle + InvAngle(listensource.angle);

	if (reverse)
		angle = InvAngle(angle);

#ifdef SURROUND
	// Produce a surround sound for angle from 105 till 255
	if (surround.value == 1 && (angle > ANG105 && angle < ANG255 ))
		*sep = SURROUND_SEP;
	else
#endif
	{
		angle >>= ANGLETOFINESHIFT;

		// stereo separation
		*sep = 128 - (FixedMul(S_STEREO_SWING, FINESINE(angle))>>FRACBITS);
	}

	// volume calculation
	if (approx_dist < S_CLOSE_DIST)
	{
		// SfxVolume is now hardware volume
		*vol = 255; // not snd_SfxVolume
	}
	else
	{
		// distance effect
		*vol = (15 * ((S_CLIPPING_DIST - approx_dist)>>FRACBITS)) / S_ATTENUATOR;
	}

	if (r_splitscreen)
		*vol = FixedDiv((*vol)<<FRACBITS, FixedSqrt((r_splitscreen+1)<<FRACBITS))>>FRACBITS;

	return (*vol > 0);
}

// Searches through the channels and checks if a sound is playing
// on the given origin.
INT32 S_OriginPlaying(void *origin)
{
	INT32 cnum;
	if (!origin)
		return false;

#ifdef HW3SOUND
	if (hws_mode != HWS_DEFAULT_MODE)
		return HW3S_OriginPlaying(origin);
#endif

	for (cnum = 0; cnum < numofchannels; cnum++)
		if (channels[cnum].origin == origin)
			return 1;
	return 0;
}

// Searches through the channels and checks if a given id
// is playing anywhere.
INT32 S_IdPlaying(sfxenum_t id)
{
	INT32 cnum;

#ifdef HW3SOUND
	if (hws_mode != HWS_DEFAULT_MODE)
		return HW3S_IdPlaying(id);
#endif

	for (cnum = 0; cnum < numofchannels; cnum++)
		if ((size_t)(channels[cnum].sfxinfo - S_sfx) == (size_t)id)
			return 1;
	return 0;
}

// Searches through the channels and checks for
// origin x playing sound id y.
INT32 S_SoundPlaying(void *origin, sfxenum_t id)
{
	INT32 cnum;
	if (!origin)
		return 0;

#ifdef HW3SOUND
	if (hws_mode != HWS_DEFAULT_MODE)
		return HW3S_SoundPlaying(origin, id);
#endif

	for (cnum = 0; cnum < numofchannels; cnum++)
	{
		if (channels[cnum].origin == origin
		 && (size_t)(channels[cnum].sfxinfo - S_sfx) == (size_t)id)
			return 1;
	}
	return 0;
}

//
// S_StartSoundName
// Starts a sound using the given name.
#define MAXNEWSOUNDS 10
static sfxenum_t newsounds[MAXNEWSOUNDS] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

void S_StartSoundName(void *mo, const char *soundname)
{
	INT32 i, soundnum = 0;
	// Search existing sounds...
	for (i = sfx_None + 1; i < NUMSFX; i++)
	{
		if (!S_sfx[i].name)
			continue;
		if (!stricmp(S_sfx[i].name, soundname))
		{
			soundnum = i;
			break;
		}
	}

	if (!soundnum)
	{
		for (i = 0; i < MAXNEWSOUNDS; i++)
		{
			if (newsounds[i] == 0)
				break;
			if (!S_IdPlaying(newsounds[i]))
			{
				S_RemoveSoundFx(newsounds[i]);
				break;
			}
		}

		if (i == MAXNEWSOUNDS)
		{
			CONS_Debug(DBG_GAMELOGIC, "Cannot load another extra sound!\n");
			return;
		}

		soundnum = S_AddSoundFx(soundname, false, 0, false);
		newsounds[i] = soundnum;
	}

	S_StartSound(mo, soundnum);
}

//
// Initializes sound stuff, including volume
// Sets channels, SFX volume,
//  allocates channel buffer, sets S_sfx lookup.
//
void S_InitSfxChannels(INT32 sfxVolume)
{
	INT32 i;

	if (dedicated)
		return;

	S_SetSfxVolume(sfxVolume);

	SetChannelsNum();

	// Note that sounds have not been cached (yet).
	for (i = 1; i < NUMSFX; i++)
	{
		S_sfx[i].usefulness = -1; // for I_GetSfx()
		S_sfx[i].lumpnum = LUMPERROR;
	}

	// precache sounds if requested by cmdline, or precachesound var true
	if (!sound_disabled && (M_CheckParm("-precachesound") || precachesound.value))
	{
		// Initialize external data (all sounds) at start, keep static.
		CONS_Printf(M_GetText("Loading sounds... "));

		for (i = 1; i < NUMSFX; i++)
			if (S_sfx[i].name)
				S_sfx[i].data = I_GetSfx(&S_sfx[i]);

		CONS_Printf(M_GetText(" pre-cached all sound data\n"));
	}
}

/// ------------------------
/// Music
/// ------------------------

#ifdef MUSICSLOT_COMPATIBILITY
const char *compat_special_music_slots[16] =
{
	"_title", // 1036  title screen
	"_intro", // 1037  intro
	"_clear", // 1038  level clear
	"_inv", // 1039  invincibility
	"_shoes",  // 1040  super sneakers
	"_minv", // 1041  Mario invincibility
	"_drown",  // 1042  drowning
	"_gover", // 1043  game over
	"_1up", // 1044  extra life
	"_conti", // 1045  continue screen
	"_super", // 1046  Super Sonic
	"_chsel", // 1047  character select
	"_creds", // 1048  credits
	"_inter", // 1049  Race Results
	"_stjr",   // 1050  Sonic Team Jr. Presents
	""
};
#endif

static char      music_name[7]; // up to 6-character name
static void      *music_data;
static UINT16    music_flags;
static boolean   music_looping;
static consvar_t *music_refade_cv;
static int       music_usage;

static char      queue_name[7];
static UINT16    queue_flags;
static boolean   queue_looping;
static UINT32    queue_position;
static UINT32    queue_fadeinms;

static tic_t     pause_starttic;

/// ------------------------
/// Music Definitions
/// ------------------------

enum
{
	MUSICDEF_20,
};

musicdef_t *musicdefstart = NULL;
struct cursongcredit cursongcredit; // Currently displayed song credit info

//
// search for music definition in wad
//
static UINT16 W_CheckForMusicDefInPwad(UINT16 wadid)
{
	UINT16 i;
	lumpinfo_t *lump_p;

	lump_p = wadfiles[wadid]->lumpinfo;
	for (i = 0; i < wadfiles[wadid]->numlumps; i++, lump_p++)
		if (memcmp(lump_p->name, "MUSICDEF", 8) == 0)
			return i;

	return INT16_MAX; // not found
}

static boolean
ReadMusicDefFields (UINT16 wadnum, int line, boolean fields, char *stoken,
		musicdef_t **defp, int *versionp)
{
	musicdef_t *def;
	//int version;

	char *value;
	char *textline;
	//int i;

	(void)versionp;

	if (!stricmp(stoken, "lump"))
	{
		value = strtok(NULL, " ");
		if (!value)
		{
			CONS_Alert(CONS_WARNING,
					"MUSICDEF: Field '%s' is missing name. (file %s, line %d)\n",
					stoken, wadfiles[wadnum]->filename, line);
			return false;
		}
		else
		{
			musicdef_t *prev = NULL;
			def = musicdefstart;

			// Search if this is a replacement
			//CONS_Printf("S_LoadMusicDefs: Searching for song replacement...\n");
			while (def)
			{
				if (!stricmp(def->name, value))
				{
					//CONS_Printf("S_LoadMusicDefs: Found song replacement '%s'\n", def->name);
					break;
				}

				prev = def;
				def = def->next;
			}

			// Nothing found, add to the end.
			if (!def)
			{
				def = Z_Calloc(sizeof (musicdef_t), PU_STATIC, NULL);
				STRBUFCPY(def->name, value);
				strlwr(def->name);
				if (prev != NULL)
					prev->next = def;
				//CONS_Printf("S_LoadMusicDefs: Added song '%s'\n", def->name);
			}

			(*defp) = def;
		}
	}
	else if (!stricmp(stoken, "version"))
	{
		if (fields)/* is this not the first field? */
		{
			CONS_Alert(CONS_WARNING,
					"MUSICDEF: Field '%s' must come first. (file %s, line %d)\n",
					stoken, wadfiles[wadnum]->filename, line);
			return false;
		}
		else
		{
			value = strtok(NULL, " ");
			if (!value)
			{
				CONS_Alert(CONS_WARNING,
						"MUSICDEF: Field '%s' is missing version. (file %s, line %d)\n",
						stoken, wadfiles[wadnum]->filename, line);
				return false;
			}
			else
			{
				/*
				if (strcasecmp(value, "2.2.0"))
					(*versionp) = MUSICDEF_221;
				*/
				;
			}
		}
	}
	else
	{
		//version = (*versionp);

		value = strtok(NULL, "");

		if (value)
		{
			// Find the equals sign.
			value = strchr(value, '=');
		}

		if (!value)
		{
			CONS_Alert(CONS_WARNING,
					"MUSICDEF: Field '%s' is missing value. (file %s, line %d)\n",
					stoken, wadfiles[wadnum]->filename, line);
			return false;
		}
		else
		{
			def = (*defp);

			if (!def)
			{
				CONS_Alert(CONS_ERROR,
						"MUSICDEF: No music definition before field '%s'. (file %s, line %d)\n",
						stoken, wadfiles[wadnum]->filename, line);
				return false;
			}

			// Skip the equals sign.
			value++;

			// Now skip funny whitespace.
			value += strspn(value, "\t ");

			textline = value;
			//i = atoi(value);

			/* based ignored lumps */
			if (!stricmp(stoken, "usage")) {
#if 0 // Ignore for now
				STRBUFCPY(def->usage, textline);
#endif
			} else if (!stricmp(stoken, "source")) {
				STRBUFCPY(def->source, textline);
			} else {
				CONS_Alert(CONS_WARNING,
						"MUSICDEF: Invalid field '%s'. (file %s, line %d)\n",
						stoken, wadfiles[wadnum]->filename, line);
			}
		}
	}

	return true;
}

void S_LoadMusicDefs(UINT16 wadnum)
{
	UINT16 lumpnum;
	char *lump;
	char *musdeftext;
	size_t size;

	char *lf;
	char *stoken;

	size_t nlf = 0xFFFFFFFF;
	size_t ncr;

	musicdef_t *def = NULL;
	int version = MUSICDEF_20;
	int line = 1; // for better error msgs
	boolean fields = false;

	lumpnum = W_CheckForMusicDefInPwad(wadnum);
	if (lumpnum == INT16_MAX)
		return;

	lump = W_CacheLumpNumPwad(wadnum, lumpnum, PU_CACHE);
	size = W_LumpLengthPwad(wadnum, lumpnum);

	// Null-terminated MUSICDEF lump.
	musdeftext = malloc(size+1);
	if (!musdeftext)
		I_Error("S_LoadMusicDefs: No more free memory for the parser\n");
	M_Memcpy(musdeftext, lump, size);
	musdeftext[size] = '\0';

	// Find music def
	stoken = musdeftext;
	for (;;)
	{
		lf = strpbrk(stoken, "\r\n");
		if (lf)
		{
			if (*lf == '\n')
				nlf = 1;
			else
				nlf = 0;
			*lf++ = '\0';/* now we can delimit to here */
		}

		stoken = strtok(stoken, " ");
		if (stoken)
		{
			if (! ReadMusicDefFields(wadnum, line, fields, stoken,
						&def, &version))
				break;
			fields = true;
		}

		if (lf)
		{
			do
			{
				line += nlf;
				ncr = strspn(lf, "\r");/* skip CR */
				lf += ncr;
				nlf = strspn(lf, "\n");
				lf += nlf;
			}
			while (nlf || ncr) ;

			stoken = lf;/* now the next nonempty line */
		}
		else
			break;/* EOF */
	}

	free(musdeftext);
}

//
// S_InitMusicDefs
//
// Simply load music defs in all wads.
//
void S_InitMusicDefs(void)
{
	UINT16 i;
	for (i = 0; i < numwadfiles; i++)
		S_LoadMusicDefs(i);
}

//
// S_ShowMusicCredit
//
// Display current song's credit on screen
//
void S_ShowMusicCredit(void)
{
	musicdef_t *def = musicdefstart;

	if (!cv_songcredits.value || demo.rewinding)
		return;

	if (!def) // No definitions
		return;

	while (def)
	{
		if (!stricmp(def->name, music_name))
		{
			cursongcredit.def = def;
			cursongcredit.anim = 5*TICRATE;
			cursongcredit.x = 0;
			cursongcredit.trans = NUMTRANSMAPS;
			return;
		}
		else
			def = def->next;
	}
}

/// ------------------------
/// Music Status
/// ------------------------

boolean S_DigMusicDisabled(void)
{
	return digital_disabled;
}

boolean S_MIDIMusicDisabled(void)
{
	return midi_disabled; // SRB2Kart: defined as "true" w/ NO_MIDI
}

boolean S_MusicDisabled(void)
{
	return (midi_disabled && digital_disabled);
}

boolean S_MusicPlaying(void)
{
	return I_SongPlaying();
}

boolean S_MusicPaused(void)
{
	return I_SongPaused();
}

boolean S_MusicNotInFocus(void)
{
	return (
			( window_notinfocus && ! cv_playmusicifunfocused.value )
	);
}

musictype_t S_MusicType(void)
{
	return I_SongType();
}

const char *S_MusicName(void)
{
	return music_name;
}

boolean S_MusicExists(const char *mname, boolean checkMIDI, boolean checkDigi)
{
	return (
		(checkDigi ? W_CheckNumForName(va("O_%s", mname)) != LUMPERROR : false)
		|| (checkMIDI ? W_CheckNumForName(va("D_%s", mname)) != LUMPERROR : false)
	);
}

/// ------------------------
/// Music Effects
/// ------------------------

boolean S_SpeedMusic(float speed)
{
	return I_SetSongSpeed(speed);
}

/// ------------------------
/// Music Seeking
/// ------------------------

UINT32 S_GetMusicLength(void)
{
	return I_GetSongLength();
}

boolean S_SetMusicLoopPoint(UINT32 looppoint)
{
	return I_SetSongLoopPoint(looppoint);
}

UINT32 S_GetMusicLoopPoint(void)
{
	return I_GetSongLoopPoint();
}

boolean S_SetMusicPosition(UINT32 position)
{
	return I_SetSongPosition(position);
}

UINT32 S_GetMusicPosition(void)
{
	return I_GetSongPosition();
}

/// ------------------------
/// Music Stacking (Jingles)
/// In this section: mazmazz doesn't know how to do dynamic arrays or struct pointers!
/// ------------------------

char music_stack_nextmusname[7];
boolean music_stack_noposition = false;
UINT32 music_stack_fadeout = 0;
UINT32 music_stack_fadein = 0;
static musicstack_t *music_stacks = NULL;
static musicstack_t *last_music_stack = NULL;

void S_SetStackAdjustmentStart(void)
{
	if (!pause_starttic)
		pause_starttic = gametic;
}

void S_AdjustMusicStackTics(void)
{
	if (pause_starttic)
	{
		musicstack_t *mst;
		for (mst = music_stacks; mst; mst = mst->next)
			mst->tic += gametic - pause_starttic;
		pause_starttic = 0;
	}
}

static void S_ResetMusicStack(void)
{
	musicstack_t *mst, *mst_next;
	for (mst = music_stacks; mst; mst = mst_next)
	{
		mst_next = mst->next;
		Z_Free(mst);
	}
	music_stacks = last_music_stack = NULL;
}

static void S_RemoveMusicStackEntry(musicstack_t *entry)
{
	musicstack_t *mst;
	for (mst = music_stacks; mst; mst = mst->next)
	{
		if (mst == entry)
		{
			// Remove ourselves from the chain and link
			// prev and next together

			if (mst->prev)
				mst->prev->next = mst->next;
			else
				music_stacks = mst->next;

			if (mst->next)
				mst->next->prev = mst->prev;
			else
				last_music_stack = mst->prev;

			break;
		}
	}
	Z_Free(entry);
}

static void S_RemoveMusicStackEntryByStatus(UINT16 status)
{
	musicstack_t *mst, *mst_next;

	if (!status)
		return;

	for (mst = music_stacks; mst; mst = mst_next)
	{
		mst_next = mst->next;
		if (mst->status == status)
			S_RemoveMusicStackEntry(mst);
	}
}

static void S_AddMusicStackEntry(const char *mname, UINT16 mflags, boolean looping, UINT32 position, UINT16 status)
{
	musicstack_t *mst, *new_mst;

	// if the first entry is empty, force master onto it
	if (!music_stacks)
	{
		music_stacks = Z_Calloc(sizeof (*mst), PU_MUSIC, NULL);
		strncpy(music_stacks->musname, (status == JT_MASTER ? mname : (S_CheckQueue() ? queue_name : mapmusname)), 7);
		music_stacks->musflags = (status == JT_MASTER ? mflags : (S_CheckQueue() ? queue_flags : mapmusflags));
		music_stacks->looping = (status == JT_MASTER ? looping : (S_CheckQueue() ? queue_looping : true));
		music_stacks->position = (status == JT_MASTER ? position : (S_CheckQueue() ? queue_position : S_GetMusicPosition()));
		music_stacks->tic = gametic;
		music_stacks->status = JT_MASTER;
		music_stacks->mlumpnum = S_GetMusicLumpNum(music_stacks->musname);
		music_stacks->noposition = S_CheckQueue();

		if (status == JT_MASTER)
			return; // we just added the user's entry here
	}

	// look for an empty slot to park ourselves
	for (mst = music_stacks; mst->next; mst = mst->next);

	// create our new entry
	new_mst = Z_Calloc(sizeof (*new_mst), PU_MUSIC, NULL);
	strncpy(new_mst->musname, mname, 7);
	new_mst->musname[6] = 0;
	new_mst->musflags = mflags;
	new_mst->looping = looping;
	new_mst->position = position;
	new_mst->tic = gametic;
	new_mst->status = status;
	new_mst->mlumpnum = S_GetMusicLumpNum(new_mst->musname);
	new_mst->noposition = false;

	mst->next = new_mst;
	new_mst->prev = mst;
	new_mst->next = NULL;
	last_music_stack = new_mst;
}

static musicstack_t *S_GetMusicStackEntry(UINT16 status, boolean fromfirst, INT16 startindex)
{
	musicstack_t *mst, *start_mst = NULL, *mst_next;

	// if the first entry is empty, force master onto it
	// fixes a memory corruption bug
	if (!music_stacks && status != JT_MASTER)
		S_AddMusicStackEntry(mapmusname, mapmusflags, true, S_GetMusicPosition(), JT_MASTER);

	if (startindex >= 0)
	{
		INT16 i = 0;
		for (mst = music_stacks; mst && i <= startindex; mst = mst->next, i++)
			start_mst = mst;
	}
	else
		start_mst = (fromfirst ? music_stacks : last_music_stack);

	for (mst = start_mst; mst; mst = mst_next)
	{
		mst_next = (fromfirst ? mst->next : mst->prev);

		if (!status || mst->status == status)
		{
			if (P_EvaluateMusicStatus(mst->status, mst->musname))
			{
				if (!S_MusicExists(mst->musname, !midi_disabled, !digital_disabled)) // paranoia
					S_RemoveMusicStackEntry(mst); // then continue
				else
					return mst;
			}
			else
				S_RemoveMusicStackEntry(mst); // then continue
		}
	}

	return NULL;
}

void S_RetainMusic(const char *mname, UINT16 mflags, boolean looping, UINT32 position, UINT16 status)
{
	musicstack_t *mst;

	if (!status) // we use this as a null indicator, don't push
	{
		CONS_Alert(CONS_ERROR, "Music stack entry must have a nonzero status.\n");
		return;
	}
	else if (status == JT_MASTER) // enforce only one JT_MASTER
	{
		for (mst = music_stacks; mst; mst = mst->next)
		{
			if (mst->status == JT_MASTER)
			{
				CONS_Alert(CONS_ERROR, "Music stack can only have one JT_MASTER entry.\n");
				return;
			}
		}
	}
	else // remove any existing status
		S_RemoveMusicStackEntryByStatus(status);

	S_AddMusicStackEntry(mname, mflags, looping, position, status);
}

boolean S_RecallMusic(UINT16 status, boolean fromfirst)
{
	UINT32 newpos = 0;
	boolean mapmuschanged = false;
	musicstack_t *result;
	musicstack_t *entry = Z_Calloc(sizeof (*result), PU_MUSIC, NULL);
#ifndef NO_MIDI
	boolean currentmidi = (I_SongType() == MU_MID || I_SongType() == MU_MID_EX);
	boolean midipref = cv_musicpref.value;
#endif

	if (status)
		result = S_GetMusicStackEntry(status, fromfirst, -1);
	else
		result = S_GetMusicStackEntry(JT_NONE, false, -1);

	if (result && !S_MusicExists(result->musname, !midi_disabled, !digital_disabled))
	{
		Z_Free(entry);
		return false; // music doesn't exist, so don't do anything
	}

	// make a copy of result, since we make modifications to our copy
	if (result)
	{
		*entry = *result;
		strncpy(entry->musname, result->musname, 7);
	}

	// no result, just grab mapmusname
	if (!result || !entry->musname[0] || ((status == JT_MASTER || (music_stacks ? !music_stacks->status : false)) && !entry->status))
	{
		strncpy(entry->musname, mapmusname, 7);
		entry->musflags = mapmusflags;
		entry->looping = true;
		entry->position = mapmusposition;
		entry->tic = gametic;
		entry->status = JT_MASTER;
		entry->mlumpnum = S_GetMusicLumpNum(entry->musname);
		entry->noposition = false; // don't set this until we do the mapmuschanged check, below. Else, this breaks some resumes.
	}

	if (entry->status == JT_MASTER)
	{
		mapmuschanged = strnicmp(entry->musname, mapmusname, 7);
		if (mapmuschanged)
		{
			strncpy(entry->musname, mapmusname, 7);
			entry->musflags = mapmusflags;
			entry->looping = true;
			entry->position = mapmusposition;
			entry->tic = gametic;
			entry->status = JT_MASTER;
			entry->mlumpnum = S_GetMusicLumpNum(entry->musname);
			entry->noposition = true;
		}
		S_ResetMusicStack();
	}
	else if (!entry->status)
	{
		Z_Free(entry);
		return false;
	}

	if (strncmp(entry->musname, S_MusicName(), 7) // don't restart music if we're already playing it
#ifndef NO_MIDI
		|| (midipref != currentmidi && S_PrefAvailable(midipref, entry->musname)) // but do if the user's preference has changed
#endif
		)
	{
		if (music_stack_fadeout)
			S_ChangeMusicEx(entry->musname, entry->musflags, entry->looping, 0, music_stack_fadeout, 0);
		else
		{
			S_ChangeMusicEx(entry->musname, entry->musflags, entry->looping, 0, 0, music_stack_fadein);

			if (!entry->noposition && !music_stack_noposition) // HACK: Global boolean to toggle position resuming, e.g., de-superize
			{
				UINT32 poslapse = 0;

				// To prevent the game from jumping past the end of the music, we need
				// to check if we can get the song's length. Otherwise, if the lapsed resume time goes
				// over a LOOPPOINT, mixer_sound.c will be unable to calculate the new resume position.
				if (S_GetMusicLength())
					poslapse = (UINT32)((float)(gametic - entry->tic)/(float)TICRATE*(float)MUSICRATE);

				newpos = entry->position + poslapse;
			}

			// If the newly recalled music lumpnum does not match the lumpnum that we stored in stack,
			// then discard the new position. That way, we will not recall an invalid position
			// when the music is replaced or digital/MIDI is toggled.
			if (newpos > 0 && S_MusicPlaying() && S_GetMusicLumpNum(entry->musname) == entry->mlumpnum)
				S_SetMusicPosition(newpos);
			else
			{
				S_StopFadingMusic();
				S_SetInternalMusicVolume(100);
			}
		}
		music_stack_noposition = false;
		music_stack_fadeout = 0;
		music_stack_fadein = JINGLEPOSTFADE;
	}

	Z_Free(entry);
	return true;
}

/// ------------------------
/// Music Playback
/// ------------------------

static lumpnum_t S_GetMusicLumpNum(const char *mname)
{
#ifndef NO_MIDI
	boolean midipref = cv_musicpref.value;

	if (S_PrefAvailable(midipref, mname))
		return W_GetNumForName(va(midipref ? "d_%s":"o_%s", mname));
	else if (S_PrefAvailable(!midipref, mname))
		return W_GetNumForName(va(midipref ? "o_%s":"d_%s", mname));
	else
		return LUMPERROR;
#else
	return W_GetNumForName(va("o_%s", mname));
#endif

}

static boolean S_LoadMusic(const char *mname)
{
	lumpnum_t mlumpnum;
	void *mdata;

	if (S_MusicDisabled())
		return false;

	mlumpnum = S_GetMusicLumpNum(mname);

	if (S_MIDIMusicDisabled() && S_MIDIExists(mname))
	{
#ifdef NO_MIDI
		CONS_Alert(CONS_ERROR, "A MIDI music lump %.6s was found,\nbut SRB2Kart does not support MIDI output.\nWe apologise for the inconvenience.\n", mname);
#endif
		return false;
	}

	if (mlumpnum == LUMPERROR)
	{
		CONS_Alert(CONS_ERROR, "Music %.6s could not be loaded: lump not found!\n", mname);
		return false;
	}

	// load & register it
	mdata = W_CacheLumpNum(mlumpnum, PU_MUSIC);


	if (I_LoadSong(mdata, W_LumpLength(mlumpnum)))
	{
		strncpy(music_name, mname, 7);
		music_name[6] = 0;
		music_data = mdata;
		return true;
	}
	else
	{
		CONS_Alert(CONS_ERROR, "Music %.6s could not be loaded: engine failure!\n", mname);
		return false;
	}
}

static void S_UnloadMusic(void)
{
	I_UnloadSong();

#ifndef HAVE_SDL //SDL uses RWOPS
	Z_ChangeTag(music_data, PU_CACHE);
#endif
	music_data = NULL;

	music_name[0] = 0;
	music_flags = 0;
	music_looping = false;

	music_refade_cv = 0;
	music_usage = 0;
}

static boolean S_PlayMusic(boolean looping, UINT32 fadeinms)
{
	//musicdef_t *def;

	if (S_MusicDisabled())
		return false;

	I_UpdateSongLagConditions();

	if ((!fadeinms && !I_PlaySong(looping)) ||
		(fadeinms && !I_FadeInPlaySong(fadeinms, looping)))
	{
		CONS_Alert(CONS_ERROR, "Music %.6s could not be played: engine failure!\n", music_name);
		S_UnloadMusic();
		return false;
	}

#if 0
	/* set loop point from MUSICDEF */
	for (def = musicdefstart; def; def = def->next)
	{
		if (strcasecmp(def->name, music_name) == 0)
		{
			if (def->loop_ms)
				S_SetMusicLoopPoint(def->loop_ms);
			break;
		}
	}
#endif

	S_InitMusicVolume(); // switch between digi and sequence volume

	if (S_MusicNotInFocus())
		S_PauseAudio();

	return true;
}

static void S_QueueMusic(const char *mmusic, UINT16 mflags, boolean looping, UINT32 position, UINT32 fadeinms)
{
	strncpy(queue_name, mmusic, 7);
	queue_flags = mflags;
	queue_looping = looping;
	queue_position = position;
	queue_fadeinms = fadeinms;
}

static boolean S_CheckQueue(void)
{
	return queue_name[0];
}

static void S_ClearQueue(void)
{
	queue_name[0] = queue_flags = queue_looping = queue_position = queue_fadeinms = 0;
}

static void S_ChangeMusicToQueue(void)
{
	S_ChangeMusicEx(queue_name, queue_flags, queue_looping, queue_position, 0, queue_fadeinms);
	S_ClearQueue();
}

void S_ChangeMusicEx(const char *mmusic, UINT16 mflags, boolean looping, UINT32 position, UINT32 prefadems, UINT32 fadeinms)
{
	char newmusic[7];
#ifndef NO_MIDI
	boolean currentmidi = (I_SongType() == MU_MID || I_SongType() == MU_MID_EX);
	boolean midipref = cv_musicpref.value;
#endif

	if (S_MusicDisabled()
		|| demo.rewinding // Don't mess with music while rewinding!
		|| demo.title) // SRB2Kart: Demos don't interrupt title screen music
		return;

	strncpy(newmusic, mmusic, 7);

	if(LUAh_MusicChange(music_name, newmusic, &mflags, &looping, &position, &prefadems, &fadeinms))
		return;

	newmusic[6] = 0;

 	// No Music (empty string)
	if (newmusic[0] == 0)
 	{
		if (prefadems)
			I_FadeSong(0, prefadems, &S_StopMusic);
		else
			S_StopMusic();
		return;
	}

	if (prefadems) // queue music change for after fade // allow even if the music is the same
		// && S_MusicPlaying() // Let the delay happen even if we're not playing music
	{
		CONS_Debug(DBG_DETAILED, "Now fading out song %s\n", music_name);
		S_QueueMusic(newmusic, mflags, looping, position, fadeinms);
		I_FadeSong(0, prefadems, S_ChangeMusicToQueue);
		return;
	}
	else if (strnicmp(music_name, newmusic, 6) || (mflags & MUSIC_FORCERESET)
#ifndef NO_MIDI
		|| (midipref != currentmidi && S_PrefAvailable(midipref, newmusic))
#endif
		)
 	{
		CONS_Debug(DBG_DETAILED, "Now playing song %s\n", newmusic);

		S_StopMusic();

		if (!S_LoadMusic(newmusic))
			return;

		music_flags = mflags;
		music_looping = looping;

		if (!S_PlayMusic(looping, fadeinms))
			return;

		if (position)
			I_SetSongPosition(position);

		I_SetSongTrack(mflags & MUSIC_TRACKMASK);
	}
	else if (fadeinms) // let fades happen with same music
	{
		I_SetSongPosition(position);
		I_FadeSong(100, fadeinms, NULL);
 	}
	else // reset volume to 100 with same music
	{
		I_StopFadingSong();
		I_FadeSong(100, 500, NULL);
	}
}

void S_ChangeMusicSpecial (const char *mmusic)
{
	if (cv_resetspecialmusic.value)
		S_ChangeMusic(mmusic, MUSIC_FORCERESET, true);
	else
		S_ChangeMusicInternal(mmusic, true);
}

void S_StopMusic(void)
{
	if (!I_SongPlaying()
		|| demo.rewinding // Don't mess with music while rewinding!
		|| demo.title) // SRB2Kart: Demos don't interrupt title screen music
		return;

	if (strcasecmp(music_name, mapmusname) == 0)
		mapmusresume = I_GetSongPosition();

	if (I_SongPaused())
		I_ResumeSong();

	S_SpeedMusic(1.0f);
	I_StopSong();
	S_UnloadMusic(); // for now, stopping also means you unload the song

	if (cv_closedcaptioning.value)
	{
		if (closedcaptions[0].s-S_sfx == sfx_None)
		{
			if (gamestate != wipegamestate)
			{
				closedcaptions[0].c = NULL;
				closedcaptions[0].s = NULL;
				closedcaptions[0].t = 0;
				closedcaptions[0].b = 0;
			}
			else
				closedcaptions[0].t = CAPTIONFADETICS;
		}
	}
}

//
// Stop and resume music, during game PAUSE.
//
void S_PauseAudio(void)
{
	if (I_SongPlaying() && !I_SongPaused())
		I_PauseSong();

	S_SetStackAdjustmentStart();
}

void S_ResumeAudio(void)
{
	if (S_MusicNotInFocus())
		return;

	if (I_SongPlaying() && I_SongPaused())
		I_ResumeSong();

	S_AdjustMusicStackTics();
}

void S_DisableSound(void)
{
	if (sound_started && !sound_disabled)
	{
		sound_disabled = true;
		S_StopSounds();
	}
}

void S_EnableSound(void)
{
	if (sound_started && sound_disabled)
	{
		sound_disabled = false;
		S_InitSfxChannels(cv_soundvolume.value);
	}
}

void S_SetMusicVolume(INT32 digvolume, INT32 seqvolume)
{
	if (digvolume < 0)
		digvolume = cv_digmusicvolume.value;

#ifdef NO_MIDI
	(void)seqvolume;
#else
	if (seqvolume < 0)
		seqvolume = cv_midimusicvolume.value;
#endif

	if (digvolume < 0 || digvolume > 31)
		CONS_Alert(CONS_WARNING, "digmusicvolume should be between 0-31\n");
	CV_SetValue(&cv_digmusicvolume, digvolume&31);
	actualdigmusicvolume = cv_digmusicvolume.value;   //check for change of var

#ifndef NO_MIDI
	if (seqvolume < 0 || seqvolume > 31)
		CONS_Alert(CONS_WARNING, "midimusicvolume should be between 0-31\n");
	CV_SetValue(&cv_midimusicvolume, seqvolume&31);
	actualmidimusicvolume = cv_midimusicvolume.value;   //check for change of var
#endif

	switch(I_SongType())
	{
#ifndef NO_MIDI
		case MU_MID:
		case MU_MID_EX:
		//case MU_MOD:
		//case MU_GME:
			I_SetMusicVolume(seqvolume&31);
			break;
#endif
		default:
			I_SetMusicVolume(digvolume&31);
			break;
	}
}

void
S_SetRestoreMusicFadeInCvar (consvar_t *cv)
{
	music_refade_cv = cv;
}

int
S_GetRestoreMusicFadeIn (void)
{
	if (music_refade_cv)
		return music_refade_cv->value;
	else
		return 0;
}

void
S_SetMusicUsage (int type)
{
	music_usage = type;
	I_UpdateSongLagConditions();
}

int
S_MusicUsage (void)
{
	return music_usage;
}

/// ------------------------
/// Music Fading
/// ------------------------

void S_SetInternalMusicVolume(INT32 volume)
{
	I_SetInternalMusicVolume(min(max(volume, 0), 100));
}

void S_StopFadingMusic(void)
{
	I_StopFadingSong();
}

boolean S_FadeMusicFromVolume(UINT8 target_volume, INT16 source_volume, UINT32 ms)
{
	if (source_volume < 0)
		return I_FadeSong(target_volume, ms, NULL);
	else
		return I_FadeSongFromVolume(target_volume, source_volume, ms, NULL);
}

boolean S_FadeOutStopMusic(UINT32 ms)
{
	return I_FadeSong(0, ms, &S_StopMusic);
}

/// ------------------------
/// Init & Others
/// ------------------------

//
// Per level startup code.
// Kills playing sounds at start of level,
//  determines music if any, changes music.
//
void S_StartEx(boolean reset)
{
	(void)reset;

	if (mapmusflags & MUSIC_RELOADRESET)
	{
		strncpy(mapmusname, mapheaderinfo[gamemap-1]->musname, 7);
		mapmusname[6] = 0;
		mapmusflags = (mapheaderinfo[gamemap-1]->mustrack & MUSIC_TRACKMASK);
		mapmusposition = mapheaderinfo[gamemap-1]->muspos;
		mapmusresume = 0;
	}

	S_StopMusic(); // Starting ambience should always be restarted, if playing.

	if (leveltime < (starttime + (TICRATE/2))) // SRB2Kart
		S_ChangeMusicEx((encoremode ? "estart" : "kstart"), 0, false, mapmusposition, 0, 0);
	else
		S_ChangeMusicEx(mapmusname, mapmusflags, true, mapmusposition, 0, 0);

	S_ResetMusicStack();
	music_stack_noposition = false;
	music_stack_fadeout = 0;
	music_stack_fadein = JINGLEPOSTFADE;
}

static void Command_Tunes_f(void)
{
	const char *tunearg;
	UINT16 tunenum, track = 0;
	UINT32 position = 0;
	const size_t argc = COM_Argc();

	if (argc < 2) //tunes slot ...
	{
		CONS_Printf("tunes <name/num> [track] [speed] [position] / <-show> / <-default> / <-none>:\n");
		CONS_Printf(M_GetText("Play an arbitrary music lump. If a map number is used, 'MAP##M' is played.\n"));
		CONS_Printf(M_GetText("If the format supports multiple songs, you can specify which one to play.\n\n"));
		CONS_Printf(M_GetText("* With \"-show\", shows the currently playing tune and track.\n"));
		CONS_Printf(M_GetText("* With \"-default\", returns to the default music for the map.\n"));
		CONS_Printf(M_GetText("* With \"-none\", any music playing will be stopped.\n"));
		return;
	}

	tunearg = COM_Argv(1);
	tunenum = (UINT16)atoi(tunearg);
	track = 0;

	if (!strcasecmp(tunearg, "-show"))
	{
		CONS_Printf(M_GetText("The current tune is: %s [track %d]\n"),
			mapmusname, (mapmusflags & MUSIC_TRACKMASK));
		return;
	}
	if (!strcasecmp(tunearg, "-none"))
	{
		S_StopMusic();
		return;
	}
	else if (!strcasecmp(tunearg, "-default"))
	{
		tunearg = mapheaderinfo[gamemap-1]->musname;
		track = mapheaderinfo[gamemap-1]->mustrack;
	}
	else if (!tunearg[2] && toupper(tunearg[0]) >= 'A' && toupper(tunearg[0]) <= 'Z')
		tunenum = (UINT16)M_MapNumber(tunearg[0], tunearg[1]);

	if (tunenum && tunenum >= 1036)
	{
		CONS_Alert(CONS_NOTICE, M_GetText("Valid music slots are 1 to 1035.\n"));
		return;
	}
	if (!tunenum && strlen(tunearg) > 6) // This is automatic -- just show the error just in case
		CONS_Alert(CONS_NOTICE, M_GetText("Music name too long - truncated to six characters.\n"));

	if (argc > 2)
		track = (UINT16)atoi(COM_Argv(2))-1;

	if (tunenum)
		snprintf(mapmusname, 7, "%sM", G_BuildMapName(tunenum));
	else
		strncpy(mapmusname, tunearg, 7);

	if (argc > 4)
		position = (UINT32)atoi(COM_Argv(4));

	mapmusname[6] = 0;
	mapmusflags = (track & MUSIC_TRACKMASK);
	mapmusposition = position;
	mapmusresume = 0;

	S_ChangeMusicEx(mapmusname, mapmusflags, true, mapmusposition, 0, 0);

	if (argc > 3)
	{
		float speed = (float)atof(COM_Argv(3));
		if (speed > 0.0f)
			S_SpeedMusic(speed);
	}
}

static void Command_RestartAudio_f(void)
{
	if (dedicated)  // No point in doing anything if game is a dedicated server.
		return;

	S_StopMusic();
	S_StopSounds();
	I_ShutdownMusic();
	I_ShutdownSound();
	I_StartupSound();
	I_InitMusic();

// These must be called or no sound and music until manually set.

	I_SetSfxVolume(cv_soundvolume.value);
#ifdef NO_MIDI
	S_SetMusicVolume(cv_digmusicvolume.value, -1);
#else
	S_SetMusicVolume(cv_digmusicvolume.value, cv_midimusicvolume.value);
#endif

	S_StartSound(NULL, sfx_strpst);

	if (Playing()) // Gotta make sure the player is in a level
		P_RestoreMusic(&players[consoleplayer]);
	else
		S_ChangeMusicInternal("titles", looptitle);
}

void GameSounds_OnChange(void)
{
	if (M_CheckParm("-nosound") || M_CheckParm("-noaudio"))
		return;

	if (sound_disabled)
	{
		sound_disabled = false;
		I_StartupSound(); // will return early if initialised
		S_InitSfxChannels(cv_soundvolume.value);
		S_StartSound(NULL, sfx_strpst);
	}
	else
	{
		sound_disabled = true;
		S_StopSounds();
	}
}

void GameDigiMusic_OnChange(void)
{
	if (M_CheckParm("-nomusic") || M_CheckParm("-noaudio"))
		return;
	else if (M_CheckParm("-nodigmusic"))
		return;

	if (digital_disabled)
	{
		digital_disabled = false;
		I_StartupSound(); // will return early if initialised
		I_InitMusic();

		if (Playing())
		{
			P_RestoreMusic(&players[consoleplayer]);
		}
		else if (
#ifndef NO_MIDI
			(!cv_musicpref.value || midi_disabled) &&
#endif
			S_DigExists("_title"))
		{
			S_ChangeMusicInternal("_title", looptitle);
		}
	}
	else
	{
		digital_disabled = true;
		if (S_MusicType() != MU_MID && S_MusicType() != MU_MID_EX)
		{
			S_StopMusic();
			if (!midi_disabled)
			{
				if (Playing())
					P_RestoreMusic(&players[consoleplayer]);
				else
					S_ChangeMusicInternal("_clear", false);
			}
		}
	}
}

#ifndef NO_MIDI
void GameMIDIMusic_OnChange(void)
{
	if (M_CheckParm("-nomusic") || M_CheckParm("-noaudio"))
		return;
	else if (M_CheckParm("-nomidimusic"))
		return;

	if (midi_disabled)
	{
		midi_disabled = false;
		I_StartupSound(); // will return early if initialised
		I_InitMusic();

		if (Playing())
			P_RestoreMusic(&players[consoleplayer]);
		else if ((cv_musicpref.value || digital_disabled) && S_MIDIExists("_clear"))
			S_ChangeMusicInternal("_clear", false);
	}
	else
	{
		midi_disabled = true;
		if (S_MusicType() == MU_MID || S_MusicType() == MU_MID_EX)
		{
			S_StopMusic();
			if (!digital_disabled)
			{
				if (Playing())
					P_RestoreMusic(&players[consoleplayer]);
				else
					S_ChangeMusicInternal("_clear", false);
			}
		}
	}
}
#endif

static void PlayMusicIfUnfocused_OnChange(void)
{
	if (window_notinfocus)
	{
		if (cv_playmusicifunfocused.value)
			I_PauseSong();
		else
			I_ResumeSong();
	}
}

static void PlaySoundIfUnfocused_OnChange(void)
{
	if (!cv_gamesounds.value)
		return;

	if (window_notinfocus)
	{
		if (cv_playsoundifunfocused.value)
			S_DisableSound();
		else
			S_EnableSound();
	}
}

#ifndef NO_MIDI
void MusicPref_OnChange(void)
{
	if (M_CheckParm("-nomusic") || M_CheckParm("-noaudio") ||
		M_CheckParm("-nomidimusic") || M_CheckParm("-nodigmusic"))
		return;

	if (Playing())
		P_RestoreMusic(&players[consoleplayer]);
	else if (S_PrefAvailable(cv_musicpref.value, "_clear"))
		S_ChangeMusicInternal("_clear", false);
}
#endif

#ifdef HAVE_OPENMPT
void ModFilter_OnChange(void)
{
	if (openmpt_mhandle)
		openmpt_module_set_render_param(openmpt_mhandle, OPENMPT_MODULE_RENDER_INTERPOLATIONFILTER_LENGTH, cv_modfilter.value);
}
#endif
