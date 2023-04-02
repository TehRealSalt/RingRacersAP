/// \file  menus/options-profiles-1.c
/// \brief Profiles Menu

#include "../k_menu.h"
#include "../s_sound.h"

// profile select
menuitem_t OPTIONS_Profiles[] = {
	{IT_KEYHANDLER | IT_NOTHING, NULL, "Select a Profile.",
		NULL, {.routine = M_HandleProfileSelect}, 0, 0},     // dummy menuitem for the control func
};

menu_t OPTIONS_ProfilesDef = {
	sizeof (OPTIONS_Profiles) / sizeof (menuitem_t),
	&OPTIONS_MainDef,
	0,
	OPTIONS_Profiles,
	32, 80,
	SKINCOLOR_ULTRAMARINE, 0,
	0,
	NULL,
	2, 5,
	M_DrawProfileSelect,
	M_OptionsTick,
	NULL,
	NULL,
	NULL,
};

consvar_t cv_dummyprofilename = CVAR_INIT ("dummyprofilename", "", CV_HIDDEN, NULL, NULL);
consvar_t cv_dummyprofileplayername = CVAR_INIT ("dummyprofileplayername", "", CV_HIDDEN, NULL, NULL);
consvar_t cv_dummyprofilekickstart = CVAR_INIT ("dummyprofilekickstart", "Off", CV_HIDDEN, CV_OnOff, NULL);
consvar_t cv_dummyprofilerumble = CVAR_INIT ("dummyprofilerumble", "On", CV_HIDDEN, CV_OnOff, NULL);

void M_ProfileSelectInit(INT32 choice)
{
	(void)choice;
	optionsmenu.profilemenu = true;
	optionsmenu.profilen = cv_currprofile.value;

	M_SetupNextMenu(&OPTIONS_ProfilesDef, false);
}

// Select the current profile for menu use and go to maindef.
void M_FirstPickProfile(INT32 c)
{
	if (c == MA_YES)
	{
		M_ResetOptions();			// Reset all options variables otherwise things are gonna go reaaal bad lol.
		optionsmenu.profile = NULL;	// Make sure to get rid of that, too.

		PR_ApplyProfile(optionsmenu.profilen, 0);

		if (restoreMenu == NULL)
			restoreMenu = &MainDef;
		M_SetupNextMenu(M_SpecificMenuRestore(M_InterruptMenuWithChallenges(restoreMenu)), false);
		restoreMenu = NULL;

		// Tell the game this is the last profile we picked.
		CV_StealthSetValue(&cv_ttlprofilen, optionsmenu.profilen);

		// Save em!
		PR_SaveProfiles();
		return;
	}
}

// Start menu edition. Call this with MA_YES if not used with a textbox.
static void M_StartEditProfile(INT32 c)
{

	const INT32 maxp = PR_GetNumProfiles();

	if (c == MA_YES)
	{
		if (optionsmenu.profilen == maxp)
			PR_InitNewProfile();	// initialize the new profile.

		optionsmenu.profile = PR_GetProfile(optionsmenu.profilen);
		// copy this profile's controls into optionsmenu so that we can edit controls without changing them directly.
		// we do this so that we don't edit a profile's controls in real-time and end up doing really weird shit.
		memcpy(&optionsmenu.tempcontrols, optionsmenu.profile->controls, sizeof(gamecontroldefault));

		// This is now used to move the card we've selected.
		optionsmenu.optx = 160;
		optionsmenu.opty = 35;
		optionsmenu.toptx = 130/2;
		optionsmenu.topty = 0;

		// setup cvars
		if (optionsmenu.profile->version)
		{
			CV_StealthSet(&cv_dummyprofilename, optionsmenu.profile->profilename);
			CV_StealthSet(&cv_dummyprofileplayername, optionsmenu.profile->playername);
			CV_StealthSetValue(&cv_dummyprofilekickstart, optionsmenu.profile->kickstartaccel);
			CV_StealthSetValue(&cv_dummyprofilerumble, optionsmenu.profile->rumble);
		}
		else
		{
			CV_StealthSet(&cv_dummyprofilename, "");
			CV_StealthSet(&cv_dummyprofileplayername, "");
			CV_StealthSetValue(&cv_dummyprofilekickstart, 0);	// off
			CV_StealthSetValue(&cv_dummyprofilerumble, 1);	// on
		}

		// Setup greyout and stuff.
		OPTIONS_EditProfile[popt_profilename].status = IT_STRING | IT_CVAR | IT_CV_STRING;
		OPTIONS_EditProfile[popt_profilepname].status = IT_STRING | IT_CVAR | IT_CV_STRING;
		OPTIONS_EditProfile[popt_char].status = IT_STRING | IT_CALL;

		if (gamestate != GS_MENU)	// If we're modifying things mid game, transtext some of those!
		{
			OPTIONS_EditProfile[popt_profilename].status |= IT_TRANSTEXT;
			OPTIONS_EditProfile[popt_profilepname].status |= IT_TRANSTEXT;
			OPTIONS_EditProfile[popt_char].status |= IT_TRANSTEXT;
		}

		M_SetupNextMenu(&OPTIONS_EditProfileDef, false);
		return;
	}
}

void M_HandleProfileSelect(INT32 ch)
{
	const UINT8 pid = 0;
	INT32 maxp = PR_GetNumProfiles();
	boolean creatable = (maxp < MAXPROFILES);
	(void) ch;

	if (menutransition.tics == 0 && optionsmenu.resetprofile)
	{
		optionsmenu.profile = NULL;	// Make sure to reset that when transitions are done.'
		optionsmenu.resetprofile = false;
	}

	if (!creatable)
	{
		maxp = MAXPROFILES;
	}

	if (menucmd[pid].dpad_lr > 0)
	{
		optionsmenu.profilen++;
		optionsmenu.offset += (128 + 128/8);

		if (optionsmenu.profilen > maxp)
		{
			optionsmenu.profilen = 0;
			optionsmenu.offset -= (128 + 128/8)*(maxp+1);
		}

		S_StartSound(NULL, sfx_s3k5b);
		M_SetMenuDelay(pid);

	}
	else if (menucmd[pid].dpad_lr < 0)
	{
		optionsmenu.profilen--;
		optionsmenu.offset -= (128 + 128/8);

		if (optionsmenu.profilen < 0)
		{
			optionsmenu.profilen = maxp;
			optionsmenu.offset += (128 + 128/8)*(maxp+1);
		}

		S_StartSound(NULL, sfx_s3k5b);
		M_SetMenuDelay(pid);
	}

	else if (M_MenuConfirmPressed(pid))
	{

		// Boot profile setup has already been done.
		if (cv_currprofile.value > -1)
		{

			if (optionsmenu.profilen == 0)	// Guest profile, you can't edit that one!
			{
				S_StartSound(NULL, sfx_s3k7b);
				M_StartMessage(M_GetText("The Guest profile cannot be edited.\nCreate a new profile instead."), NULL, MM_NOTHING);
				M_SetMenuDelay(pid);
				return;
			}
			else if (creatable && optionsmenu.profilen == maxp && gamestate != GS_MENU)
			{
				S_StartSound(NULL, sfx_s3k7b);
				M_StartMessage(M_GetText("Cannot create a new profile\nmid-game. Return to the\ntitle screen first."), NULL, MM_NOTHING);
				M_SetMenuDelay(pid);
				return;
			}

			S_StartSound(NULL, sfx_s3k5b);
			M_StartEditProfile(MA_YES);
		}
		else
		{
			// We're on the profile selection screen.
			if (creatable && optionsmenu.profilen == maxp)
			{
				M_StartEditProfile(MA_YES);
				M_SetMenuDelay(pid);
				return;
			}
			else
			{
#if 0
				if (optionsmenu.profilen == 0)
				{
					M_StartMessage(M_GetText("Are you sure you wish\nto use the Guest Profile?\nThis profile cannot be customised.\nIt is recommended to create\na new Profile instead.\n\nPress (A) to confirm or (B) to cancel"), FUNCPTRCAST(M_FirstPickProfile), MM_YESNO);
					return;
				}
#endif

				M_FirstPickProfile(MA_YES);
				M_SetMenuDelay(pid);
				return;
			}
		}
	}

	else if (M_MenuBackPressed(pid))
	{
		optionsmenu.resetprofilemenu = true;
		M_GoBack(0);
		M_SetMenuDelay(pid);
	}
}
