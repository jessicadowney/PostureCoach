---
name: PostureCoach
description: A 1982 aerobics class as a flat, warm picture book, with the app as the instructor shouting the set list.
colors:
  coral: "#ef6a50"
  sunflower: "#f5c23e"
  deep-teal: "#17757a"
  plum-ink: "#2a1632"
  paper: "#fff3e0"
  white: "#ffffff"
  code-plum: "#1c0e22"
typography:
  display:
    fontFamily: "Anybody, sans-serif"
    fontSize: "clamp(3.6rem, 12vw, 9rem)"
    fontWeight: 900
    lineHeight: 0.92
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Anybody, sans-serif"
    fontSize: "clamp(2.4rem, 7vw, 4.6rem)"
    fontWeight: 900
    lineHeight: 0.92
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Anybody, sans-serif"
    fontSize: "1.7rem"
    fontWeight: 900
    lineHeight: 1
  body:
    fontFamily: "Hanken Grotesk, system-ui, sans-serif"
    fontSize: "18px"
    fontWeight: 500
    lineHeight: 1.55
  label:
    fontFamily: "Hanken Grotesk, system-ui, sans-serif"
    fontSize: "0.85rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0.06em"
  code:
    fontFamily: "ui-monospace, Menlo, monospace"
    fontSize: "15px"
    fontWeight: 600
    lineHeight: 1.5
rounded:
  none: "0px"
  card: "18px"
spacing:
  xs: "10px"
  sm: "16px"
  md: "28px"
  lg: "56px"
  xl: "96px"
components:
  button-primary:
    backgroundColor: "{colors.plum-ink}"
    textColor: "{colors.sunflower}"
    rounded: "{rounded.none}"
    padding: "16px 30px"
    typography: "{typography.title}"
  button-alt:
    backgroundColor: "transparent"
    textColor: "{colors.plum-ink}"
    rounded: "{rounded.none}"
    padding: "16px 30px"
  timer-card:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.plum-ink}"
    rounded: "{rounded.card}"
    padding: "18px 18px 14px"
  code-block:
    backgroundColor: "{colors.code-plum}"
    textColor: "{colors.paper}"
    rounded: "{rounded.none}"
    padding: "16px 96px 16px 16px"
  copy-button:
    backgroundColor: "{colors.sunflower}"
    textColor: "{colors.plum-ink}"
    rounded: "{rounded.none}"
    padding: "6px 12px"
  nag-panel:
    backgroundColor: "{colors.plum-ink}"
    textColor: "{colors.white}"
    rounded: "{rounded.none}"
    padding: "28px 24px 26px"
---

# Design System: PostureCoach

## Overview

**Creative North Star: "The Instructor With a Whistle"**

The page is a 1982 aerobics class redrawn as a flat picture book, and the app is the instructor shouting the set list. Each section is a field of one warm colour (coral, sunflower or deep teal), set in extra-wide italic caps, with hard plum rules and skewed type that leans forward like a body mid-lunge. Authored flat SVG figures (a coach in leg warmers, and sit / stand / walk scenes) carry the story instead of effects. It is loud but friendly, and it refuses the calm teal wellness-app page and the neon-sign page.

Density is generous at the section level (56px top, 96px bottom padding per field) and tight inside it: big type, short lines, one idea per row. Energy comes from slant (skewX -8deg), tilt (rotate -3deg and 1deg) and diagonal tri-stripe seams, never from glow or haze.

The build keeps a few cooler-than-brand details: the code block fill (#1c0e22) is a one-off darker plum and the illustration skin tones (#c98660, #f0c4a0, #8d5a3b) live only inside the SVGs.

**Key Characteristics:**
- Three flat colour fields (coral, sunflower, deep teal) plus a plum-ink field; no gradients except the tri-stripe seam.
- One display face, all caps, italic, weight 900, skewed.
- Hand-drawn-feel flat SVG illustration: round-capped strokes, flat fills, no outlines or gradients, drawn from the page palette.
- Square corners everywhere except one soft 18px paper timer card; 3 to 6px plum rules as the structural line.
- Live demo timer is the hero proof; copy is coach-voice, shouted.

## Colors

Warm, sun-baked flats on plum ink, one field colour per section.

### Primary
- **Coral** (#ef6a50): hero and FAQ fields, the theme colour, step numerals and nag-stage rules on ink, stripe seams, shirts and headbands in the illustrations.
- **Sunflower** (#f5c23e): the "Today's class" field, primary button text, headings, links, code borders and copy button on ink, the logo badge, leg-warmer stripes.
- **Deep Teal** (#17757a): the "moves" field (white text), the timer clock digits, stripe seams, leotard and tops in the illustrations.

### Neutral
- **Plum Ink** (#2a1632): all text on coral and sunflower, button fill, rules, outlines, the install and footer field, scrollbar track, illustration lines and hair.
- **Paper** (#fff3e0): the timer card, the second hero headline line (with a plum stroke), secondary copy on ink, nag stage labels, code text, shoes and screens in the illustrations.
- **White** (#ffffff): body text on teal and on ink.
- **Code Plum** (#1c0e22): code block fill only.

### Named Rules
**The One Field Per Section Rule.** A section is drenched in exactly one of coral, sunflower, teal or plum ink. Fields meet only through the tri-stripe seam.

**The Plum Text Rule.** Text on coral and sunflower is plum ink. On teal and ink it is white or paper, with sunflower for headings and links on ink. Paper-on-coral is reserved for the outlined hero headline.

## Typography

**Display Font:** Anybody (variable, 100 to 900, upright and italic; sans-serif fallback)
**Body Font:** Hanken Grotesk (variable, system-ui fallback)
**Label/Mono Font:** system monospace for code only

**Character:** Anybody pushed to its widest, heaviest italic reads as a shouted instruction. Hanken Grotesk stays plain and medium so the shouting has somewhere to rest.

### Hierarchy
- **Display** (900 italic caps, clamp(3.6rem, 12vw, 9rem), 0.92): the hero "Stand up!" only, each line skewed and stacked.
- **Headline** (900 italic caps, clamp(2.4rem, 7vw, 4.6rem), 0.92, -0.02em): section titles, always inside a skewed span.
- **Set Title** (900 italic caps, clamp(2.6rem, 9vw, 6rem), 0.95): the Sit / Stand / Walk rows, with a smaller sub-line (clamp 1rem to 1.6rem).
- **Title** (900 italic caps, 1.7rem to 1.9rem, 1): move cards, nag heading; FAQ summaries at 1.25rem.
- **Body** (500, 18px, 1.55): paragraphs at 30 to 62ch; lede is 1.3rem at weight 700, 34ch.
- **Label** (700 to 800 caps, 0.8 to 0.85rem, 0.06 to 0.08em): nav links, timer menu row, nag stage tags, copy button.

### Named Rules
**The Shout Rule.** Anything set in Anybody is italic, caps, weight 900. No upright or light cuts of the display face.

## Layout

Single column inside a 1040px wrapper with 16px side gutters. Sections are full-bleed colour fields stacked vertically; the hero is a 1.25fr / 1fr grid (copy left, illustrated stage right with the timer card overlapping the coach). Sets are a three-column row (200px scene, title, note) under a 6px plum rule; moves are a two-column grid with 48px column gap and 4px top rules; nag stages are four across. Spacing rhythm: 10, 16, 28, 56, 96px. At 760px and below everything collapses to one column, the coach illustration is hidden and the timer card goes full width, nag stages go to two, and step numerals shrink from 4.4rem to 3rem.

Sections join through skewed tri-stripe seams (44px tall, skewY -2.2deg, coral / sunflower / teal thirds, reversed on alternate joins) and a 64px bleed pseudo-element so fields overlap without gaps. The same coral / sunflower / teal stripe caps the nag panel.

## Elevation & Depth

Flat colour fields and flat illustration carry the structure; depth appears only as soft, offset drop shadows under objects that look lifted off the page and tilted.

### Shadow Vocabulary
- **Lift** (`box-shadow: 6px 8px 14px rgba(18,10,15,.4)`): the primary button at rest; grows to `8px 12px 18px` on hover, shrinks to `3px 4px 8px` when pressed.
- **Card** (`box-shadow: 8px 12px 22px rgba(42,22,50,.28)`): the paper timer card.
- **Ground** (`opacity .18` plum ellipse): the coach illustration's floor shadow.

### Named Rules
**The Lifted-Object Rule.** Shadows go under tilted or skewed objects only. Flat fields, rules, text blocks and illustration figures stay shadowless.

## Shapes

Square by default: radius 0 on every button, panel and code block. The single exception is the paper timer card at 18px, the one soft object, framed by a 3px plum border. Silhouette otherwise comes from skew (-8deg on headlines and buttons), tilt (-3deg timer, 1deg nag panel) and the diagonal stripe seams. Structure is drawn with thick plum rules (3px borders, 4px list rules, 6px set rules). Illustration is built from fat round-capped, round-joined strokes for limbs and torsos, plain circles for heads and hair, flat fills only, in the page palette. The logo is a sunflower parallelogram badge with a plum stroked raised-arm figure.

## Components

### Buttons
- **Shape:** square, skewed -8deg.
- **Primary:** plum fill, sunflower Anybody italic caps 1.1rem, padding 16px 30px, Lift shadow.
- **Hover / Active:** hover moves (-2px, -3px) with a deeper shadow; active presses (+2px, +3px) with a tighter one; 0.15s springy ease (cubic-bezier(.2,.8,.2,1)).
- **Alt:** transparent, plum text, 3px plum border, no shadow, sits beside primary (10px gap, stacks with 14px gap on mobile).

### Timer Card (signature)
Paper card, 18px corners, 3px plum border, tilted -3deg with the Card shadow, overlapping the coach illustration. A small uppercase menu row over a 3px plum rule, a giant Anybody phase word, a deep-teal clock (tabular numerals), a shout line and a small note. On each phase change it jolts (0.5s scale and skew settle); reduced-motion users get a static card.

### Illustration
Hero coach (raised arm, headband, leg warmers) and three 220x180 scenes (hunched sit, tall stand at a raised desk, striding walk) on a plum ground line. Each has a role and aria-label. Palette only: plum, coral, sunflower, teal, paper plus skin tones.

### Code Blocks
Code Plum fill, 3px sunflower border, paper 15px monospace, no radius, horizontal scroll. A sunflower copy button sits top-right (uppercase 12px label, paper on hover), label flips to "copied".

### Set List and Moves
Rows divided by thick plum top rules; Anybody italic titles with plain 700-weight notes at 30 to 36ch.

### Nag Panel
Plum panel tilted 1deg, topped by the tri-stripe: sunflower title, four stages each under a 4px coral rule with a paper caps label.

### Navigation
Brand badge plus uppercase 0.85rem links at weight 700; hover is a 3px underline with 5px offset. Wraps rather than collapsing.

### FAQ
Native details/summary with 4px plum rules; summaries are Anybody italic caps 1.25rem.

## Do's and Don'ts

### Do:
- **Do** drench each section in one field colour (coral #ef6a50, sunflower #f5c23e, deep teal #17757a, or plum ink #2a1632) with the text colours of The Plum Text Rule.
- **Do** set display type in Anybody 900 italic caps and skew headlines -8deg.
- **Do** keep corners square and draw structure with 3 to 6px plum rules; the 18px paper card is the only rounded object.
- **Do** draw new illustration as flat SVG with round-capped strokes in the page palette, with a role and aria-label.
- **Do** join fields with the tri-stripe seam, flipping its order on alternate joins.
- **Do** keep focus rings 4px: plum on light fields, sunflower on ink.
- **Do** write copy in a shouting coach voice, and keep real facts real.
- **Do** honour prefers-reduced-motion by stopping the demo loop, jolt and button transitions.

### Don't:
- **Don't** add neon, glow, haze, synthwave grids or gradients inside illustration; the world is flat and warm.
- **Don't** round corners or soften buttons into pills.
- **Don't** set text in Anybody upright or light, or in lowercase.
- **Don't** put shadows under flat fields, text blocks or illustration figures.
- **Don't** reach for calm wellness-app teal-and-white surfaces; teal here is a saturated field with white text.

### Not canonized (defects the build carries)
- Emoji faces (U+1F615 family) as the nag-stage icons are glyph icons; do not reuse them as an icon system.
- The Lift shadow still uses the old ink rgba(18,10,15) rather than plum rgba(42,22,50); colour drift, not a second ink.
- The footer's secondary copy and `.req` text hard-code #fff3e0 instead of var(--paper); same colour, untokenized.
