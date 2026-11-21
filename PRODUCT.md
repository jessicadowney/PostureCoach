# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML/CSS in a single file (`docs/index.html`), hosted on GitHub Pages. No framework, no build step.

## Users

Friends and colleagues of the author, shared by link. Desk workers managing lower back pain who are comfortable with a Terminal install. They arrive curious and already trust the sender, so the page can be warm and brief.

## Product Purpose

PostureCoach is a macOS menu bar app that nudges the user through a sit / stand / stretch cadence to help manage lower back pain, with periodic ergonomics reminders. Success: a visitor understands it in one scroll and installs it.

## Positioning

Lives only in the menu bar (no Dock icon) and stays quiet during Microsoft Teams meetings, so the reminders fit a real working day. It is a movement reminder, not a medical product.

## Operating Context

Install is `git clone`, move `PostureCoach.app` to /Applications, run `Install PostureCoach.command` (installs `rumps`, registers a launchd LaunchAgent). Requires macOS 10.13+ and Python 3. Default cadence: sit ~35 min, stand ~17 min (10 in pain mode), stretch hourly.

## Capabilities and Constraints

Menu bar countdown, distinct system sounds, optional spoken reminders, Teams-meeting quiet mode, escalating "nag" face, English and French (France) localization, launch at login. The app is unsigned and not notarized, so Gatekeeper can block the installer.

## Brand Commitments

The name PostureCoach is fixed. The app icon is free to replace with a new mark. Binding tone and look, in the owner's words: "Unhinged, gym coach, energetic, neon, jane fonda in 80s tights" (1980s aerobics-video energy). The facts, install steps and medical disclaimer stay accurate and plain.

## Evidence on Hand

README and app source only. No real screenshots, testimonials, user counts or downloads exist yet; none may be invented. Medical disclaimer must remain on the page.

## Product Principles

- Loud voice, honest facts: the page shouts like an 80s aerobics coach, but every claim is true and the limits (unsigned app, Python required, not medical advice) are stated plainly.
- Honest about limits: not medical advice, unsigned app, Python required.
- Small and local: menu bar only, nothing leaves the Mac.
- Show the rhythm, not a feature list.
