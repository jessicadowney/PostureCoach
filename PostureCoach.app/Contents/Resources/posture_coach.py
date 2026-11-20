#!/usr/bin/env python3
"""
PostureCoach — a macOS menu bar app that nudges you through a
sit / stand / walk cadence to help manage lower back pain,
plus periodic ergonomics reminders.

Default cadence:
  Sit    35 min  (range 30-45)
  Stand  17 min  (range 15-20, or 10 min in "pain mode")
  Walk/stretch break every 60 min for 2-5 min

Requires: rumps (pip3 install --user rumps)
"""

import fcntl
import json
import os
import subprocess
import sys
import threading
import time

import rumps

try:
    import AppKit
    # Homebrew's framework Python re-execs through its own Python.app stub to
    # get a GUI run loop, which is why the Dock shows a generic "Python"
    # icon instead of our app. Force-creating the shared NSApplication here
    # and setting it to "accessory" hides it from the Dock/Cmd-Tab entirely,
    # regardless of which physical process ends up hosting the run loop.
    _ns_app = AppKit.NSApplication.sharedApplication()
    _ns_app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)
except Exception as _e:
    try:
        with open(os.path.expanduser(
            "~/Library/Application Support/PostureCoach/activation_policy_error.log"
        ), "a") as _f:
            _f.write(f"{_e!r}\n")
    except Exception:
        pass

APP_NAME = "PostureCoach"
SUPPORT_DIR = os.path.expanduser(f"~/Library/Application Support/{APP_NAME}")
CONFIG_PATH = os.path.join(SUPPORT_DIR, "config.json")

# (seconds overdue, face) — paired with nag_0..nag_N text keys in STRINGS.
# Escalates the longer an auto switch goes unacknowledged, Duolingo-style.
NAG_STAGES = [
    (3 * 60, "😕"),
    (8 * 60, "😟"),
    (15 * 60, "😣"),
    (25 * 60, "😫"),
]

SYSTEM_SOUNDS = [
    "Basso", "Blow", "Bottle", "Frog", "Funk", "Glass", "Hero",
    "Morse", "Ping", "Pop", "Purr", "Sosumi", "Submarine", "Tink",
]

DEFAULT_CONFIG = {
    "sit_minutes": 35,       # 30-45 min range
    "stand_minutes": 17,     # 15-20 min range (10 if pain_mode)
    "pain_mode": False,      # shortens standing blocks to 10 min
    "walk_interval_minutes": 60,   # remind to walk/stretch every hour
    "walk_minutes": 3,             # suggested 2-5 min
    "paused": False,
    "phase": "sit",                 # "sit" or "stand"
    "seen_intro": False,
    # distinct alert sounds per event type
    "stand_up_sound": "Pop",     # plays when it's time to stand
    "sit_down_sound": "Glass",   # plays when it's time to sit
    "stretch_sound": "Tink",     # plays for the walk/stretch reminder
    "speech_enabled": True,      # also speak reminders aloud via `say`
    "speech_voice": "",          # empty = system default voice
    "silent_in_meetings": True,  # skip spoken reminders during Teams calls
    "language": None,             # None = auto-detect once, then "en"/"fr"
}

# --- Localization: English and French (France). ---------------------------
STRINGS = {
    "ergonomics_tips": {
        "en": "Desk ergonomics check:\n"
              "• Screen at eye level\n"
              "• Elbows around 90°\n"
              "• Feet supported\n"
              "• Hips slightly above knees when sitting\n"
              "• Avoid locking your knees while standing",
        "fr": "Vérification ergonomique du poste :\n"
              "• Écran à hauteur des yeux\n"
              "• Coudes à environ 90°\n"
              "• Pieds bien posés au sol\n"
              "• Hanches légèrement au-dessus des genoux en position assise\n"
              "• Évitez de verrouiller les genoux en position debout",
    },
    "health_note": {
        "en": "This app is a movement reminder, not medical advice.\n\n"
              "If pain is severe, radiates down your leg, causes numbness or "
              "weakness, or persists more than a couple of weeks, it's worth "
              "checking with a clinician or physical therapist.",
        "fr": "Cette application est un rappel de mouvement, pas un avis médical.\n\n"
              "Si la douleur est intense, irradie dans la jambe, provoque des "
              "engourdissements ou une faiblesse, ou persiste plus de deux "
              "semaines, consultez un médecin ou un kinésithérapeute.",
    },
    "intro_text": {
        "en": "PostureCoach will nudge you between sitting and standing, with "
              "walk/stretch breaks worked in — the goal is movement variation, "
              "not standing all day.\n\n"
              "Rule of thumb: change position before you feel stiff. If standing "
              "starts to worsen your pain, turn on “Standing worsens my pain” "
              "in the menu to shorten standing blocks to 10 minutes.\n\n"
              "Right-click the menu bar icon any time to pause, skip ahead, or "
              "pick a different alert sound for stand-up / sit-down / stretch "
              "reminders. Spoken reminders automatically stay quiet while you're "
              "in a Teams meeting.",
        "fr": "PostureCoach vous invite à alterner entre position assise et "
              "debout, avec des pauses marche/étirement intégrées — l'objectif "
              "est de varier les positions, pas de rester debout toute la journée.\n\n"
              "Règle simple : changez de position avant de sentir une raideur. "
              "Si rester debout aggrave votre douleur, activez « Rester debout "
              "aggrave ma douleur » dans le menu pour réduire les blocs debout à "
              "10 minutes.\n\n"
              "Faites un clic droit sur l'icône de la barre de menus à tout "
              "moment pour mettre en pause, avancer, ou choisir un son différent "
              "pour les rappels. Les rappels vocaux restent silencieux "
              "automatiquement pendant une réunion Teams.",
    },
    "menu_ack": {"en": "✅ I switched, stop nagging", "fr": "✅ J'ai changé, arrête de me harceler"},
    "menu_pause": {"en": "Pause", "fr": "Mettre en pause"},
    "menu_resume": {"en": "Resume", "fr": "Reprendre"},
    "menu_skip": {"en": "Skip to next phase", "fr": "Passer à la phase suivante"},
    "menu_walk": {"en": "I'm taking a walk/stretch break", "fr": "Je fais une pause marche/étirement"},
    "menu_pain": {"en": "Standing worsens my pain (shorten to 10 min)",
                  "fr": "Rester debout aggrave ma douleur (réduire à 10 min)"},
    "menu_durations": {"en": "Adjust durations…", "fr": "Ajuster les durées…"},
    "menu_speech": {"en": "Speak reminders aloud", "fr": "Annoncer les rappels à voix haute"},
    "menu_meeting": {"en": "Stay quiet during Teams meetings", "fr": "Rester silencieux pendant les réunions Teams"},
    "menu_sounds": {"en": "Alert sounds", "fr": "Sons d'alerte"},
    "menu_sound_stand": {"en": "Stand-up cue", "fr": "Signal pour se lever"},
    "menu_sound_sit": {"en": "Sit-down cue", "fr": "Signal pour s'asseoir"},
    "menu_sound_stretch": {"en": "Stretch break cue", "fr": "Signal de pause étirement"},
    "menu_ergo": {"en": "Show ergonomics checklist", "fr": "Afficher la liste ergonomique"},
    "menu_health": {"en": "Health note", "fr": "Note santé"},
    "menu_about": {"en": "About PostureCoach", "fr": "À propos de PostureCoach"},
    "menu_quit": {"en": "Quit PostureCoach", "fr": "Quitter PostureCoach"},
    "menu_language": {"en": "Language", "fr": "Langue"},
    "lang_en": {"en": "English", "fr": "Anglais"},
    "lang_fr": {"en": "French (France)", "fr": "Français (France)"},

    "phase_sit": {"en": "Sit", "fr": "Assis"},
    "phase_stand": {"en": "Stand", "fr": "Debout"},

    "running_title": {"en": "PostureCoach is running", "fr": "PostureCoach est lancé"},
    "running_subtitle": {"en": "Look for the icon in your menu bar", "fr": "Regardez l'icône dans votre barre de menus"},
    "running_body": {"en": "Right-click it any time for settings, sounds, and the "
                           "ergonomics checklist. See 'About PostureCoach' for the full rundown.",
                      "fr": "Faites un clic droit à tout moment pour les réglages, les sons et la "
                            "liste ergonomique. Voir « À propos de PostureCoach » pour le détail."},
    "running_speak": {"en": "PostureCoach is running.", "fr": "PostureCoach est lancé."},

    "switch_title": {"en": "Time to switch", "fr": "C'est l'heure de changer"},
    "switch_subtitle": {"en": "Now: {phase}", "fr": "Maintenant : {phase}"},
    "switch_body": {"en": "Change position before you feel stiff. {tip}",
                     "fr": "Changez de position avant de sentir une raideur. {tip}"},
    "tip_stand": {"en": "Screen at eye level, elbows ~90°, don't lock your knees.",
                  "fr": "Écran à hauteur des yeux, coudes à ~90°, ne verrouillez pas les genoux."},
    "tip_sit": {"en": "Feet supported, hips slightly above knees, elbows ~90°.",
                "fr": "Pieds bien posés, hanches légèrement au-dessus des genoux, coudes à ~90°."},
    "speak_stand": {"en": "Time to stand up.", "fr": "C'est l'heure de se lever."},
    "speak_sit": {"en": "Time to sit down.", "fr": "C'est l'heure de s'asseoir."},

    "manual_switch_title": {"en": "Switched", "fr": "Changé"},
    "manual_switch_body": {"en": "Manually skipped ahead.", "fr": "Avancé manuellement."},

    "walk_title": {"en": "Time to move", "fr": "C'est l'heure de bouger"},
    "walk_subtitle": {"en": "Quick walk / stretch break", "fr": "Petite pause marche/étirement"},
    "walk_body": {"en": "Take {n} min to walk or stretch, then get back to it.",
                  "fr": "Prenez {n} min pour marcher ou vous étirer, puis reprenez."},
    "walk_speak": {"en": "Take a {n} minute stretch break.", "fr": "Prenez une pause étirement de {n} minutes."},

    "manual_walk_title": {"en": "Nice", "fr": "Bien joué"},
    "manual_walk_subtitle": {"en": "Walk/stretch logged", "fr": "Marche/étirement enregistré"},
    "manual_walk_body": {"en": "Timer for the next break has been reset.",
                          "fr": "Le minuteur de la prochaine pause a été réinitialisé."},
    "manual_walk_speak": {"en": "Nice, walk logged.", "fr": "Bien joué, marche enregistrée."},

    "speech_on_confirm": {"en": "Reminders will be spoken aloud.",
                           "fr": "Les rappels seront annoncés à voix haute."},

    "nag_title": {"en": "Still waiting on you", "fr": "Toujours en attente"},
    "nag_0": {"en": "Still haven't switched?", "fr": "Toujours pas changé ?"},
    "nag_1": {"en": "You really should switch now.", "fr": "Vous devriez vraiment changer maintenant."},
    "nag_2": {"en": "This is a repeat nudge — please switch.",
              "fr": "Ceci est un rappel répété — merci de changer."},
    "nag_3": {"en": "It's been a while. Your back will thank you for moving.",
              "fr": "Cela fait un moment. Votre dos vous remerciera de bouger."},

    "dur_sit_title": {"en": "Sit minutes", "fr": "Minutes assis"},
    "dur_sit_msg": {"en": "How many minutes should each sitting block be? (30-45 suggested)",
                     "fr": "Combien de minutes pour chaque bloc assis ? (30-45 suggéré)"},
    "dur_stand_title": {"en": "Stand minutes", "fr": "Minutes debout"},
    "dur_stand_msg": {"en": "How many minutes should each standing block be? (15-20 suggested, "
                            "or 10 if it's aggravating your back)",
                        "fr": "Combien de minutes pour chaque bloc debout ? (15-20 suggéré, "
                              "ou 10 si cela aggrave votre dos)"},
    "dur_walk_title": {"en": "Walk/stretch reminder", "fr": "Rappel marche/étirement"},
    "dur_walk_msg": {"en": "Remind me to walk or stretch every how many minutes?",
                      "fr": "Me rappeler de marcher ou m'étirer toutes les combien de minutes ?"},
    "btn_next": {"en": "Next", "fr": "Suivant"},
    "btn_save": {"en": "Save", "fr": "Enregistrer"},
    "btn_cancel": {"en": "Cancel", "fr": "Annuler"},
    "saved_title": {"en": "Saved", "fr": "Enregistré"},
    "saved_msg": {"en": "New durations are in effect now.", "fr": "Les nouvelles durées sont désormais actives."},
    "invalid_number_title": {"en": "Not a number", "fr": "Pas un nombre"},
    "invalid_number_msg": {"en": "That wasn't a whole number of minutes, so I kept the previous value ({val}).",
                            "fr": "Ce n'était pas un nombre entier de minutes, l'ancienne valeur ({val}) a été gardée."},
}


def tr(cfg, key, **kw):
    lang = (cfg or {}).get("language") or "en"
    entry = STRINGS.get(key, {})
    s = entry.get(lang) or entry.get("en") or key
    return s.format(**kw) if kw else s


def detect_system_language():
    try:
        out = subprocess.run(
            ["defaults", "read", "-g", "AppleLocale"],
            capture_output=True, text=True, timeout=3,
        ).stdout.strip()
        return "fr" if out.lower().startswith("fr") else "en"
    except Exception:
        return "en"


def _log_error(text):
    try:
        with open(os.path.join(SUPPORT_DIR, "error.log"), "a") as f:
            f.write(f"{time.ctime()}: {text}\n")
    except Exception:
        pass


def load_config():
    os.makedirs(SUPPORT_DIR, exist_ok=True)
    cfg = dict(DEFAULT_CONFIG)
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                cfg.update(json.load(f))
        except Exception as e:
            # Don't let a corrupted/half-written config silently reset
            # everything with no trace of why.
            _log_error(f"load_config failed, using defaults: {e!r}")
    if not cfg.get("language"):
        cfg["language"] = detect_system_language()
    return cfg


def save_config(cfg):
    # Write to a temp file and rename over the real one so a crash or kill
    # mid-write can never leave config.json half-written/corrupted.
    try:
        os.makedirs(SUPPORT_DIR, exist_ok=True)
        tmp_path = CONFIG_PATH + ".tmp"
        with open(tmp_path, "w") as f:
            json.dump(cfg, f, indent=2)
        os.replace(tmp_path, CONFIG_PATH)
    except Exception as e:
        _log_error(f"save_config failed: {e!r}")


def _applescript_escape(text):
    return text.replace("\\", "\\\\").replace('"', '\\"')


def in_teams_meeting():
    """Heuristic: Teams shows a separate window on top of its main one
    while you're in a call/meeting, so more than one window open is a
    reasonable signal.
    shortcut: checks both the classic ("Microsoft Teams") and new
    ("MSTeams") client process names; if Microsoft renames it again,
    update this list."""
    for proc_name in ("Microsoft Teams", "MSTeams"):
        script = f'tell application "System Events" to count windows of process "{proc_name}"'
        try:
            result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=3)
            if int(result.stdout.strip()) > 1:
                return True
        except Exception:
            pass
    return False


def notify(title, subtitle, message, sound_name=None, speak_text=None, cfg=None, in_meeting=False):
    """Native macOS notification, with the sound played directly via afplay.

    macOS ties a notification's own "sound name" to per-app Notification
    Center permissions, which can end up silently muted even when system
    audio is fine and Focus/DND is off. Playing the sound ourselves with
    afplay sidesteps that setting entirely. Optionally also speaks a short
    phrase aloud (useful when a chime is hard to pick out over music),
    unless silent_in_meetings is on and `in_meeting` says a Teams meeting
    looks active (checked on a background thread, not here, since the
    System Events call it needs can take a few seconds).
    """
    script = (
        f'display notification "{_applescript_escape(message)}" '
        f'with title "{_applescript_escape(title)}" '
        f'subtitle "{_applescript_escape(subtitle)}"'
    )
    try:
        subprocess.run(["osascript", "-e", script], check=False)
    except Exception:
        try:
            rumps.notification(title, subtitle, message, sound=False)
        except Exception:
            pass
    if sound_name:
        preview_sound(sound_name)
    if speak_text and cfg and cfg.get("speech_enabled"):
        if cfg.get("silent_in_meetings") and in_meeting:
            pass
        else:
            speak(speak_text, cfg.get("speech_voice"))


def speak(text, voice=None):
    # Popen, not run: `say` takes seconds to finish and this is called from
    # the main-thread timer tick — waiting on it would freeze the whole app.
    cmd = ["say"]
    if voice:
        cmd += ["-v", voice]
    cmd.append(text)
    try:
        subprocess.Popen(cmd)
    except Exception:
        pass


def preview_sound(sound_name):
    # Popen, not run: same reasoning as speak() — don't block on playback.
    path = f"/System/Library/Sounds/{sound_name}.aiff"
    try:
        subprocess.Popen(["afplay", path])
    except Exception:
        pass


class PostureCoachApp(rumps.App):
    def __init__(self):
        super().__init__(APP_NAME, title="\U0001FA91 Sit", quit_button=None)
        self.cfg = load_config()
        save_config(self.cfg)  # persist auto-detected language on first run

        self.phase_seconds_left = self._phase_length(self.cfg["phase"]) * 60
        self.since_last_walk_sec = 0
        self.unacked_since = None
        self.nag_stage = -1
        self.in_meeting = False
        threading.Thread(target=self._watch_meetings, daemon=True).start()

        self.ack_item = rumps.MenuItem(self.tr("menu_ack"), callback=self.acknowledge)
        self.pause_item = rumps.MenuItem(self.tr("menu_pause"), callback=self.toggle_pause)
        self.skip_item = rumps.MenuItem(self.tr("menu_skip"), callback=self.skip_phase)
        self.walk_item = rumps.MenuItem(self.tr("menu_walk"), callback=self.manual_walk)
        self.pain_item = rumps.MenuItem(self.tr("menu_pain"), callback=self.toggle_pain_mode)
        self.pain_item.state = self.cfg["pain_mode"]
        self.durations_item = rumps.MenuItem(self.tr("menu_durations"), callback=self.adjust_durations)
        self.speech_item = rumps.MenuItem(self.tr("menu_speech"), callback=self.toggle_speech)
        self.speech_item.state = self.cfg["speech_enabled"]
        self.meeting_item = rumps.MenuItem(self.tr("menu_meeting"), callback=self.toggle_silent_in_meetings)
        self.meeting_item.state = self.cfg["silent_in_meetings"]

        self.sound_menus = {}
        self.sounds_parent = rumps.MenuItem(self.tr("menu_sounds"))
        self.sound_submenus = {}
        for key, label_key in (
            ("stand_up_sound", "menu_sound_stand"),
            ("sit_down_sound", "menu_sound_sit"),
            ("stretch_sound", "menu_sound_stretch"),
        ):
            submenu = rumps.MenuItem(self.tr(label_key))
            self.sound_submenus[key] = (submenu, label_key)
            items = {}
            for sound in SYSTEM_SOUNDS:
                item = rumps.MenuItem(sound, callback=self._make_sound_picker(key, sound))
                item.state = (self.cfg[key] == sound)
                submenu.add(item)
                items[sound] = item
            self.sound_menus[key] = items
            self.sounds_parent.add(submenu)

        self.lang_items = {}
        self.lang_parent = rumps.MenuItem(self.tr("menu_language"))
        for code in ("en", "fr"):
            item = rumps.MenuItem(self.tr(f"lang_{code}"), callback=self._make_lang_picker(code))
            item.state = (self.cfg["language"] == code)
            self.lang_items[code] = item
            self.lang_parent.add(item)

        self.ergo_item = rumps.MenuItem(self.tr("menu_ergo"), callback=self.show_ergonomics)
        self.health_item = rumps.MenuItem(self.tr("menu_health"), callback=self.show_health_note)
        self.about_item = rumps.MenuItem(self.tr("menu_about"), callback=self.show_about)
        self.quit_item = rumps.MenuItem(self.tr("menu_quit"), callback=self.quit_app)

        self.menu = [
            self.ack_item,
            self.pause_item,
            self.skip_item,
            self.walk_item,
            None,
            self.pain_item,
            self.durations_item,
            self.sounds_parent,
            self.speech_item,
            self.meeting_item,
            self.lang_parent,
            None,
            self.ergo_item,
            self.health_item,
            self.about_item,
            None,
            self.quit_item,
        ]

        if not self.cfg["seen_intro"]:
            self.cfg["seen_intro"] = True
            save_config(self.cfg)
            # Non-blocking: a modal alert here can end up hidden on another
            # display/space before the status bar item even exists, making
            # the app look like it never launched. Use a plain notification
            # instead; full details are always in the About menu item.
            notify(
                self.tr("running_title"),
                self.tr("running_subtitle"),
                self.tr("running_body"),
                speak_text=self.tr("running_speak"),
                cfg=self.cfg,
                in_meeting=self.in_meeting,
            )

        self._refresh_pause_label()
        self._refresh_title()
        self.timer = rumps.Timer(self.tick, 1)
        self.timer.start()

    def tr(self, key, **kw):
        return tr(self.cfg, key, **kw)

    def _watch_meetings(self):
        # Runs off the main thread: the System Events call this needs can
        # take a couple of seconds, which would otherwise freeze the menu
        # bar and stall the countdown every time it's checked.
        while True:
            try:
                self.in_meeting = in_teams_meeting()
            except Exception:
                pass
            time.sleep(5)

    def _make_sound_picker(self, key, sound):
        def _pick(_sender):
            self.cfg[key] = sound
            save_config(self.cfg)
            for name, item in self.sound_menus[key].items():
                item.state = (name == sound)
            preview_sound(sound)
        return _pick

    def _make_lang_picker(self, code):
        def _pick(_sender):
            self.cfg["language"] = code
            save_config(self.cfg)
            for c, item in self.lang_items.items():
                item.state = (c == code)
            self._relabel_menu()
        return _pick

    def _relabel_menu(self):
        self.ack_item.title = self.tr("menu_ack")
        self._refresh_pause_label()
        self.skip_item.title = self.tr("menu_skip")
        self.walk_item.title = self.tr("menu_walk")
        self.pain_item.title = self.tr("menu_pain")
        self.durations_item.title = self.tr("menu_durations")
        self.sounds_parent.title = self.tr("menu_sounds")
        for key, (submenu, label_key) in self.sound_submenus.items():
            submenu.title = self.tr(label_key)
        self.speech_item.title = self.tr("menu_speech")
        self.meeting_item.title = self.tr("menu_meeting")
        self.lang_parent.title = self.tr("menu_language")
        self.ergo_item.title = self.tr("menu_ergo")
        self.health_item.title = self.tr("menu_health")
        self.about_item.title = self.tr("menu_about")
        self.quit_item.title = self.tr("menu_quit")
        self._refresh_title()

    def _phase_cues(self, phase):
        """Returns (tip, sound_name, speak_text) for the given phase."""
        if phase == "stand":
            return self.tr("tip_stand"), self.cfg["stand_up_sound"], self.tr("speak_stand")
        return self.tr("tip_sit"), self.cfg["sit_down_sound"], self.tr("speak_sit")

    def _phase_length(self, phase):
        if phase == "sit":
            return self.cfg["sit_minutes"]
        return 10 if self.cfg["pain_mode"] else self.cfg["stand_minutes"]

    def _refresh_pause_label(self):
        self.pause_item.title = self.tr("menu_resume") if self.cfg["paused"] else self.tr("menu_pause")

    def _refresh_title(self):
        mins, secs = divmod(max(self.phase_seconds_left, 0), 60)
        icon = "\U0001FA91" if self.cfg["phase"] == "sit" else "\U0001F9CD"
        label = self.tr("phase_sit") if self.cfg["phase"] == "sit" else self.tr("phase_stand")
        paused = " ⏸" if self.cfg["paused"] else ""
        if self.unacked_since is not None and self.nag_stage >= 0:
            icon = NAG_STAGES[self.nag_stage][1]
        self.title = f"{icon} {label} {mins:02d}:{secs:02d}{paused}"

    def _check_nag(self):
        if self.unacked_since is None:
            return
        overdue = time.time() - self.unacked_since
        for i, (threshold, face) in enumerate(NAG_STAGES):
            if overdue >= threshold and i > self.nag_stage:
                self.nag_stage = i
                text = self.tr(f"nag_{i}")
                phase_label = self.tr("phase_sit") if self.cfg["phase"] == "sit" else self.tr("phase_stand")
                notify(self.tr("nag_title"), f"{face} {phase_label}", text,
                       sound_name=self.cfg["stretch_sound"], speak_text=text, cfg=self.cfg,
                       in_meeting=self.in_meeting)

    def acknowledge(self, _sender):
        self.unacked_since = None
        self.nag_stage = -1
        self._refresh_title()

    def tick(self, _timer):
        if self.cfg["paused"]:
            self._refresh_title()
            return

        self.phase_seconds_left -= 1
        self.since_last_walk_sec += 1

        if self.phase_seconds_left <= 0:
            self._switch_phase()

        self._check_nag()

        walk_interval_sec = self.cfg["walk_interval_minutes"] * 60
        if self.since_last_walk_sec >= walk_interval_sec:
            self.since_last_walk_sec = 0
            notify(
                self.tr("walk_title"),
                self.tr("walk_subtitle"),
                self.tr("walk_body", n=self.cfg["walk_minutes"]),
                sound_name=self.cfg["stretch_sound"],
                speak_text=self.tr("walk_speak", n=self.cfg["walk_minutes"]),
                cfg=self.cfg,
                in_meeting=self.in_meeting,
            )

        self._refresh_title()

    def _switch_phase(self, manual=False):
        old_phase = self.cfg["phase"]
        new_phase = "stand" if old_phase == "sit" else "sit"
        self.cfg["phase"] = new_phase
        self.phase_seconds_left = self._phase_length(new_phase) * 60
        save_config(self.cfg)

        phase_label = self.tr("phase_stand") if new_phase == "stand" else self.tr("phase_sit")
        tip, sound_name, speak_text = self._phase_cues(new_phase)

        if not manual:
            notify(
                self.tr("switch_title"),
                self.tr("switch_subtitle", phase=phase_label),
                self.tr("switch_body", tip=tip),
                sound_name=sound_name,
                speak_text=speak_text,
                cfg=self.cfg,
                in_meeting=self.in_meeting,
            )
            self.unacked_since = time.time()
            self.nag_stage = -1
        else:
            self.unacked_since = None
            self.nag_stage = -1

    def skip_phase(self, _sender):
        self._switch_phase(manual=True)
        _tip, sound_name, speak_text = self._phase_cues(self.cfg["phase"])
        phase_label = self.tr("phase_stand") if self.cfg["phase"] == "stand" else self.tr("phase_sit")
        notify(
            self.tr("manual_switch_title"),
            self.tr("switch_subtitle", phase=phase_label),
            self.tr("manual_switch_body"),
            sound_name=sound_name,
            speak_text=speak_text,
            cfg=self.cfg,
            in_meeting=self.in_meeting,
        )
        self._refresh_title()

    def toggle_pause(self, _sender):
        self.cfg["paused"] = not self.cfg["paused"]
        save_config(self.cfg)
        self._refresh_pause_label()
        self._refresh_title()

    def manual_walk(self, _sender):
        self.since_last_walk_sec = 0
        notify(
            self.tr("manual_walk_title"),
            self.tr("manual_walk_subtitle"),
            self.tr("manual_walk_body"),
            sound_name=self.cfg["stretch_sound"],
            speak_text=self.tr("manual_walk_speak"),
            cfg=self.cfg,
            in_meeting=self.in_meeting,
        )

    def toggle_speech(self, _sender):
        self.cfg["speech_enabled"] = not self.cfg["speech_enabled"]
        self.speech_item.state = self.cfg["speech_enabled"]
        save_config(self.cfg)
        if self.cfg["speech_enabled"]:
            speak(self.tr("speech_on_confirm"), self.cfg.get("speech_voice"))

    def toggle_silent_in_meetings(self, _sender):
        self.cfg["silent_in_meetings"] = not self.cfg["silent_in_meetings"]
        self.meeting_item.state = self.cfg["silent_in_meetings"]
        save_config(self.cfg)

    def toggle_pain_mode(self, _sender):
        self.cfg["pain_mode"] = not self.cfg["pain_mode"]
        self.pain_item.state = self.cfg["pain_mode"]
        save_config(self.cfg)
        if self.cfg["phase"] == "stand":
            self.phase_seconds_left = min(self.phase_seconds_left, self._phase_length("stand") * 60)
        self._refresh_title()

    def adjust_durations(self, _sender):
        r1 = rumps.Window(
            title=self.tr("dur_sit_title"),
            message=self.tr("dur_sit_msg"),
            default_text=str(self.cfg["sit_minutes"]),
            ok=self.tr("btn_next"),
            cancel=self.tr("btn_cancel"),
        ).run()
        if not r1.clicked:
            return
        try:
            sit_val = max(5, int(r1.text.strip()))
        except ValueError:
            sit_val = self.cfg["sit_minutes"]
            rumps.alert(title=self.tr("invalid_number_title"), message=self.tr("invalid_number_msg", val=sit_val))

        r2 = rumps.Window(
            title=self.tr("dur_stand_title"),
            message=self.tr("dur_stand_msg"),
            default_text=str(self.cfg["stand_minutes"]),
            ok=self.tr("btn_next"),
            cancel=self.tr("btn_cancel"),
        ).run()
        if not r2.clicked:
            return
        try:
            stand_val = max(5, int(r2.text.strip()))
        except ValueError:
            stand_val = self.cfg["stand_minutes"]
            rumps.alert(title=self.tr("invalid_number_title"), message=self.tr("invalid_number_msg", val=stand_val))

        r3 = rumps.Window(
            title=self.tr("dur_walk_title"),
            message=self.tr("dur_walk_msg"),
            default_text=str(self.cfg["walk_interval_minutes"]),
            ok=self.tr("btn_save"),
            cancel=self.tr("btn_cancel"),
        ).run()
        if not r3.clicked:
            return
        try:
            walk_val = max(15, int(r3.text.strip()))
        except ValueError:
            walk_val = self.cfg["walk_interval_minutes"]
            rumps.alert(title=self.tr("invalid_number_title"), message=self.tr("invalid_number_msg", val=walk_val))

        self.cfg["sit_minutes"] = sit_val
        self.cfg["stand_minutes"] = stand_val
        self.cfg["walk_interval_minutes"] = walk_val
        save_config(self.cfg)
        self.phase_seconds_left = min(self.phase_seconds_left, self._phase_length(self.cfg["phase"]) * 60)
        self._refresh_title()
        rumps.alert(title=self.tr("saved_title"), message=self.tr("saved_msg"))

    def show_ergonomics(self, _sender):
        rumps.alert(title=self.tr("menu_ergo"), message=self.tr("ergonomics_tips"))

    def show_health_note(self, _sender):
        rumps.alert(title=self.tr("menu_health"), message=self.tr("health_note"))

    def show_about(self, _sender):
        rumps.alert(title=self.tr("menu_about"), message=self.tr("intro_text"))

    def quit_app(self, _sender):
        rumps.quit_application()


def _acquire_single_instance_lock():
    """Refuse to run a second copy (e.g. a double-click while the LaunchAgent
    copy is already up) — two instances would fight over notifications/config."""
    os.makedirs(SUPPORT_DIR, exist_ok=True)
    lock_path = os.path.join(SUPPORT_DIR, "posturecoach.lock")
    lock_file = open(lock_path, "w")
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("PostureCoach: another instance is already running, exiting.", flush=True)
        sys.exit(0)
    return lock_file  # keep a reference so the lock isn't released by GC


if __name__ == "__main__":
    print("PostureCoach: starting up...", flush=True)
    _lock_file = _acquire_single_instance_lock()
    _app = PostureCoachApp()
    print(f"PostureCoach: menu bar item created (title={_app.title!r}), entering run loop...", flush=True)
    _app.run()
