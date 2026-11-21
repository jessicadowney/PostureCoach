---
name: PostureCoach
description: A quiet, polished class timetable in azul ink on a near-white ground, with terracotta, coral and sage as the only warm notes.
colors:
  ground: "#f7f8f5"
  card: "#ffffff"
  paper: "#f3f6f1"
  ink: "#1b3556"
  muted: "#55677f"
  azul: "#2d63a8"
  azul-pressed: "#1f4d87"
  field-azul: "#24507f"
  navy: "#14283f"
  code-navy: "#0e1d30"
  sage-tint: "#e4ebe1"
  sage: "#6f9272"
  sage-light: "#cfe0cb"
  coral: "#ef7a63"
  terracotta: "#ad4f2c"
typography:
  display:
    fontFamily: "Anybody, sans-serif"
    fontSize: "clamp(2.8rem, 6.6vw, 5rem)"
    fontWeight: 700
    lineHeight: 0.98
    letterSpacing: "0em"
  headline:
    fontFamily: "Anybody, sans-serif"
    fontSize: "clamp(1.7rem, 3.6vw, 2.5rem)"
    fontWeight: 700
    lineHeight: 1.02
    letterSpacing: "0em"
  title:
    fontFamily: "Anybody, sans-serif"
    fontSize: "1.05rem"
    fontWeight: 700
    lineHeight: 1.2
  body:
    fontFamily: "Hanken Grotesk, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Hanken Grotesk, system-ui, sans-serif"
    fontSize: "0.82rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.04em"
  code:
    fontFamily: "ui-monospace, Menlo, monospace"
    fontSize: "14.5px"
    fontWeight: 500
    lineHeight: 1.55
rounded:
  none: "0px"
  sm: "6px"
  md: "8px"
  card: "14px"
spacing:
  xs: "8px"
  sm: "16px"
  md: "32px"
  lg: "64px"
  xl: "88px"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.none}"
    padding: "14px 26px"
  button-primary-hover:
    backgroundColor: "{colors.azul}"
    textColor: "{colors.paper}"
  button-primary-active:
    backgroundColor: "{colors.azul-pressed}"
  button-alt:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "14px 26px"
  button-alt-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  timer-card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "20px 20px 16px"
  cadence-bar-sit:
    backgroundColor: "{colors.ink}"
    rounded: "{rounded.none}"
    height: "22px"
  cadence-bar-stand:
    backgroundColor: "{colors.sage}"
    rounded: "{rounded.none}"
    height: "22px"
  nag-panel:
    backgroundColor: "{colors.navy}"
    textColor: "{colors.paper}"
    rounded: "{rounded.card}"
    padding: "32px 32px 30px"
  code-block:
    backgroundColor: "{colors.code-navy}"
    textColor: "{colors.paper}"
    rounded: "{rounded.md}"
    padding: "16px 92px 16px 18px"
  copy-button:
    backgroundColor: "transparent"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "6px 12px"
---

# Design System: PostureCoach

## Overview

**Creative North Star: "The Quiet Timetable"**

The page is a class timetable printed in azul ink on near-white paper. The coach-voice copy still does the shouting; the design stays calm and lets the words and one live timer carry the energy. Colour is divided by job: azul for ink, links and the one deep field; sage for the quiet "today's class" band; navy for the dark closing sections; and a small warm group of coral and terracotta that appears only on the hero disc, the "UP!" word, the logo badge, the nag faces, step numerals and the stretch dashes.

Density is generous at section level (88px top and bottom, 64px on mobile) and plain inside it: one 960px column, short lines, thin rules. Everything loud was removed on purpose. There are no tilts, skews, stripe seams, heavy rules or hard shadows, and section edges are straight. The only motion is a 350ms fade-and-rise on the timer when the demo phase changes.

**Key Characteristics:**
- Near-white ground with azul-ink text; sage tint, azul and navy are the three section fields.
- Warm colour is rationed: coral and terracotta are accents and graphic marks, never fields.
- One display face (Anybody, italic caps, weight 700) at modest sizes; Hanken Grotesk 17px for everything else.
- Hairline structure: 1 to 1.5px rules and borders, square buttons, one soft 14px card radius for the timer and nag panel.
- Flat graphic devices (coral disc cut by ground-coloured stripes, cadence bars, round nag faces) in palette colours only.

## Colors

Cool azul ink on a quiet ground, with sage for calm and a few drops of terracotta and coral for warmth.

### Primary
- **Azul Ink** (#1b3556): all body and heading text on light grounds, the primary button fill, hairline rules and borders, the sit bar.
- **Azul** (#2d63a8): links, the summary plus sign, the timer clock digits, focus ring on light grounds, scrollbar thumb, primary button hover (pressed #1f4d87).
- **Field Azul** (#24507f): the full-width "The moves" section, with white text and sage-light links.

### Secondary
- **Terracotta** (#ad4f2c): the "UP!" word in the hero headline and the logo badge and favicon. Nowhere else.
- **Coral** (#ef7a63): the hero disc, nag-stage faces, install step numerals, nag stage labels and the dashed stretch bar.

### Tertiary
- **Sage** (#6f9272): the stand bar.
- **Sage Tint** (#e4ebe1): the "Today's class" section field.
- **Sage Light** (#cfe0cb): links, nag heading, selection and focus ring on dark fields.

### Neutral
- **Ground** (#f7f8f5): page background, theme colour, and the stripes that cut the hero disc.
- **Card White** (#ffffff): the timer card.
- **Paper** (#f3f6f1): text on navy, primary button text.
- **Muted Slate** (#55677f): nav links, ledes, notes and secondary copy on light grounds.
- **Navy** (#14283f): nag panel, install section, footer.
- **Code Navy** (#0e1d30): code block fill only.

### Named Rules
**The Warm Ration Rule.** Coral and terracotta are marks, not fields. Coral is for graphic shapes and small labels; terracotta is for the logo and one headline word. If a surface is larger than a disc or a line of type, it is azul, sage or navy.

**The Ink-and-Ground Rule.** Text on the light grounds is Azul Ink or Muted Slate. On Field Azul and Navy it is white or Paper, with Sage Light for links and headings. Azul text is for links and the clock only.

## Typography

**Display Font:** Anybody (variable, 100 to 900, upright and italic; sans-serif fallback)
**Body Font:** Hanken Grotesk (variable, system-ui fallback)
**Label/Mono Font:** system monospace for code only

**Character:** Anybody italic caps at weight 700 reads as a clear instruction without raising its voice. Hanken Grotesk stays plain at 400 so the display face has somewhere to rest.

### Hierarchy
- **Display** (700 italic caps, clamp(2.8rem, 6.6vw, 5rem), 0.98): the hero "Stand up!" only, two stacked lines.
- **Headline** (700 italic caps, clamp(1.7rem, 3.6vw, 2.5rem), 1.02): section titles.
- **Set Title** (700 italic caps, clamp(1.9rem, 4.2vw, 2.8rem), 1): the Sit / Stand / Stretch rows, with a 0.9rem sentence-case sub-line in Muted Slate.
- **Title** (700 italic caps, 1.05rem to 1.25rem): move cards, nag heading, FAQ summaries, brand name; timer phase and clock at 2rem and 1.9rem.
- **Body** (400, 17px, 1.6): paragraphs at 30 to 62ch; lede 1.2rem in Muted Slate, 36ch.
- **Label** (600 caps, 0.72 to 0.82rem, 0.04 to 0.1em): nav links, timer menu row, nag stage tags, copy button.

### Named Rules
**The One Display Face Rule.** Anything set in Anybody is italic, caps and weight 700, and stays at or below 5rem. Upright, light or heavier cuts are not part of the system.

## Layout

One column inside a 960px wrapper with 20px side gutters. Sections are full-bleed fields with straight edges, stacked vertically with 88px of vertical padding (64px at 760px and below). The hero is a 1.1fr / 1fr grid (copy left, stage right) where the stage stacks the coral disc (up to 380px) and the timer card (68% of the stage, up to 270px) in one centred grid cell. Set rows are three columns (240px bar, title, note) between 1.5px rules; moves are a two-column grid with a 56px column gap; nag stages are four across; install steps are a 56px numeral column plus content. Spacing rhythm: 8, 16, 32, 64, 88px. At 760px and below everything collapses to one column, the hero disc is hidden and the timer goes full width, nag stages go to two, and step numerals shrink to 1.7rem.

## Elevation & Depth

Flat. Sections and rules do all the structuring; there is one soft shadow and no other.

### Shadow Vocabulary
- **Card** (`box-shadow: 0 18px 36px -18px rgba(27,53,86,.45)`): the white timer card only, so it reads as sitting on the disc.

### Named Rules
**The One Shadow Rule.** The timer card is the only object that casts a shadow. Buttons, panels, bars and fields stay flat; state is shown by colour change.

## Shapes

Square by default: radius 0 on buttons, bars and fields. Two soft radii exist: 14px on the timer card and nag panel, and 6 to 8px on code blocks and the copy button. Structure is drawn with 1px and 1.5px rules in Azul Ink (the 1.5px for set rows, FAQ and button borders; 1px at reduced opacity on dark fields and inside the timer). Three graphic devices recur. The hero disc is a full coral circle cut by four ground-coloured horizontal stripes that thicken downward (5, 8, 11, 16 units), with no ring. The cadence bar is a 22px unskewed slab whose length is the cadence. The nag faces are 40px coral circles with navy features. The logo is a terracotta rounded-square badge with a white round-capped "P" stroke; the favicon is the same mark.

## Components

### Buttons
- **Shape:** square, 1.5px border, Anybody italic caps 0.95rem, padding 14px 26px.
- **Primary:** Azul Ink fill, Paper text. Hover and active change colour only (azul, then #1f4d87); nothing moves.
- **Alt:** transparent, Azul Ink text and border, 10px beside primary (stacks with 12px gap on mobile). Hover fills with Azul Ink.
- **Transition:** 200ms on background, text and border colour.

### Timer Card (signature)
White card, 14px corners, 1.5px Azul Ink border, untilted, with the Card shadow, centred over the disc. A small uppercase menu row over a hairline, a 2rem Anybody phase word, an Azul tabular-numeral clock, a 600-weight shout line and a small note. On each phase change the phase and shout fade and rise 5px over 350ms; reduced-motion users get no loop and no animation.

### Hero Disc
Decorative, aria-hidden: a coral circle with four ground-coloured cut-stripes across its lower half. Flat, no shadow, no ring. Hidden at 760px and below so the timer stays in the first screen.

### Cadence Bars
Each set row leads with a 22px bar sized to the default cadence against the full column: Sit is a full-width Azul Ink bar (35 min), Stand is a 49% Sage bar (17 min), Stretch is a full-width run of coral dashes (6px on, 8px off) for the hourly reminder. A new set type gets a bar proportional to its minutes in a palette colour.

### Set List and Moves
Set rows sit between 1.5px Azul Ink rules on the Sage Tint field. Moves sit on Field Azul under 1px white-at-30% top rules, with white Anybody titles and pale azul-white copy.

### Nag Panel
Navy panel, 14px corners, no tilt or cap. Sage Light title, Paper copy, four stages each under a 1px Paper-at-30% rule with a 40px coral face and a coral caps label.

### Code Blocks
Code Navy fill, 1px Paper-at-20% border, 8px corners, Paper 14.5px monospace, horizontal scroll. A transparent outlined copy button sits top-right; hover fills Paper with ink text; label flips to "copied".

### Navigation
Terracotta brand badge plus Anybody wordmark, then 0.82rem uppercase links at weight 600 in Muted Slate; hover darkens to Azul Ink with no underline. Wraps rather than collapsing.

### FAQ
Native details/summary between 1.5px Azul Ink rules; Anybody italic caps 1rem summaries with an Azul plus that rotates 45 degrees on open; summary text turns Azul on hover.

## Do's and Don'ts

### Do:
- **Do** keep the ground near-white (#f7f8f5) and set text in Azul Ink (#1b3556), with Muted Slate (#55677f) for secondary copy.
- **Do** give each large section one field: sage tint, Field Azul or Navy; leave the hero and FAQ on the ground.
- **Do** keep terracotta (#ad4f2c) to the logo badge and the "UP!" word, and coral (#ef7a63) to the disc, nag faces, step numerals, stage labels and stretch dashes.
- **Do** set display type in Anybody 700 italic caps, no larger than 5rem.
- **Do** draw structure with 1 to 1.5px rules and keep buttons square with 1.5px borders and a colour-only hover.
- **Do** build graphic devices from flat palette shapes and mark them aria-hidden when decorative.
- **Do** size cadence bars to the real minutes, and keep the numbers beside them true.
- **Do** keep focus rings 2px with 3px offset: Azul on light grounds, Sage Light on Field Azul and Navy.
- **Do** honour prefers-reduced-motion by stopping the demo loop, the phase fade and all transitions.

### Don't:
- **Don't** tilt, skew or rotate content, or join sections with stripes, seams or diagonal edges; section edges are straight.
- **Don't** use heavy rules (over 1.5px), hard offset shadows, glow, haze or neon.
- **Don't** fill a section with coral or terracotta, or set body text in them.
- **Don't** add motion beyond the 350ms phase fade and the 200ms colour and plus-icon transitions.
- **Don't** set Anybody upright, light, heavier than 700 or in lowercase.
- **Don't** round buttons into pills or add radii beyond 6, 8 and 14px.

### Not canonized (defects the build carries)
- The logo badge, favicon, disc and nag-face SVG fills (#ad4f2c, #ef7a63, #14283f, #f3f6f1, #f7f8f5) and the CSS one-offs #1f4d87, #e4ecf6, #d5deea and #0e1d30 are hard-coded rather than tokenized; same palette, untokenized.
- The `.hero h1` second-line colour change and the inline `margin-bottom:28px` on the FAQ heading are one-offs, not rules.
