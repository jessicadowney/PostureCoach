# PostureCoach

A macOS menu bar app that nudges you through a sit / stand / walk cadence
to help manage lower back pain, with periodic ergonomics reminders.

Default cadence: sit ~35 min (30-45 range), stand ~17 min (15-20, or 10 min
in "pain mode"), with a walk/stretch reminder every hour.

## Features

- Lives in the menu bar only (no Dock icon), shows the current phase and a
  countdown.
- Distinct alert sounds for stand-up, sit-down, and stretch-break cues,
  picked from a menu of macOS system sounds.
- Spoken reminders via text-to-speech, with a menu toggle.
- Automatically stays quiet (no speech) while you're in a Microsoft Teams
  meeting, but still shows the visual banner and chime.
- Escalating "nag" face in the menu bar if a sit/stand switch goes
  unacknowledged, with a one-click way to clear it.
- Full French (France) localization, auto-detected from the system
  language, with a manual override.
- Launches automatically at login via a `launchd` LaunchAgent.

## Install

1. Download/clone this repo.
2. Move `PostureCoach.app` into `/Applications`.
3. Run `Install PostureCoach.command` (double-click it, or if Gatekeeper
   blocks it, run `bash "Install PostureCoach.command"` in Terminal).

The installer finds a working Python 3 interpreter, installs the
[`rumps`](https://github.com/jaredks/rumps) menu bar library for it, and
registers a LaunchAgent so the app starts automatically at login.

## Requirements

- macOS 10.13+
- Python 3 (Homebrew's `python3` is preferred; falls back to whatever
  `python3` resolves to on `$PATH`)
- `rumps` (installed automatically by the installer)

## Repo layout

- `PostureCoach.app/Contents/Resources/posture_coach.py` — the entire app
  logic (menu, timers, notifications, localization).
- `PostureCoach.app/Contents/Info.plist` — app bundle metadata
  (`LSUIElement` hides the Dock icon).
- `PostureCoach.app/Contents/MacOS/PostureCoach` — launcher script; the
  installer rewrites this with the resolved Python interpreter path.
- `Install PostureCoach.command` — sets up the LaunchAgent and pins the
  Python interpreter.

## Notes

This app is a movement reminder, not medical advice. If pain is severe,
radiates down your leg, causes numbness or weakness, or persists more than
a couple of weeks, check with a clinician or physical therapist.
