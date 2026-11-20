---
name: PostureCoach
description: A 1982 aerobics class in Day-Glo, with the app as the instructor shouting the set list.
colors:
  hot-pink: "#ff2d95"
  acid-yellow: "#e6ff00"
  electric-cyan: "#00e1ff"
  ink: "#120a0f"
  white: "#ffffff"
  terminal-black: "#07040a"
  blush-text: "#f1e6ee"
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
spacing:
  xs: "10px"
  sm: "16px"
  md: "28px"
  lg: "56px"
  xl: "96px"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.acid-yellow}"
    rounded: "{rounded.none}"
    padding: "16px 30px"
    typography: "{typography.title}"
  button-alt:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "16px 30px"
  timer-badge:
    backgroundColor: "{colors.acid-yellow}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "26px 24px 22px"
  code-block:
    backgroundColor: "{colors.terminal-black}"
    textColor: "{colors.electric-cyan}"
    rounded: "{rounded.none}"
    padding: "16px 96px 16px 16px"
  copy-button:
    backgroundColor: "{colors.electric-cyan}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "6px 12px"
  nag-panel:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.white}"
    rounded: "{rounded.none}"
    padding: "28px 24px 26px"
---

# Design System: PostureCoach

## Overview

**Creative North Star: "The Instructor With a Whistle"**

The page is a 1982 aerobics class and the app is the instructor shouting the set list. Every section is a field drenched in one neon, set in extra-wide italic caps, with hard ink rules and skewed shapes that lean forward like a body mid-lunge. It is loud on purpose and it refuses the calm teal wellness-app page.

Density is generous at the section level (56px top, 96px bottom padding per field) and tight inside it: big type, short lines, one idea per row. Energy comes from slant (skewX -8deg), tilt (rotate -2.5deg and 1deg) and diagonal stripe bands, never from glow or haze.

The build diverges from the contract in one place: ink is a near-black warm brown-violet (#120a0f), not a clear deep violet. The prose follows the build.

**Key Characteristics:**
- Four flat colour fields (pink, yellow, cyan, ink), no gradients except the tri-colour stripe band.
- One display face, all caps, italic, weight 900, skewed.
- Square corners everywhere; thick ink rules (3 to 6px) as the structural line.
- Soft drop shadows only under lifted, tilted objects (button, timer badge).
- Live demo timer is the hero proof; copy is coach-voice, shouted.

## Colors

Day-Glo flats on warm ink, one neon per section.

### Primary
- **Hot Pink** (#ff2d95): hero and FAQ fields, the theme colour, step numerals and nag-stage rules on ink, the clock digits in the timer.
- **Acid Yellow** (#e6ff00): the "Today's class" field, the timer badge, primary button text, headings and links on ink, focus ring on ink, the logo badge.
- **Electric Cyan** (#00e1ff): the "moves" field, code blocks and their borders, the copy button, small labels on ink.

### Neutral
- **Ink** (#120a0f): all text on neon fields, button fill, rules, the install and footer field, scrollbar track.
- **White** (#ffffff): hero headline over pink, body text on ink.
- **Terminal Black** (#07040a): code block fill only.
- **Blush Text** (#f1e6ee): secondary copy on ink (requirements, footer).

### Named Rules
**The One Neon Per Field Rule.** A section is drenched in exactly one of pink, yellow or cyan, with ink text. Never put two neons side by side as text and ground; neons meet only at the stripe bands.

**The Ink Text Rule.** Text on a neon field is ink. On ink it is white, blush, or a neon heading. White on neon is reserved for the oversized hero headline.

## Typography

**Display Font:** Anybody (variable, 100 to 900, upright and italic; sans-serif fallback)
**Body Font:** Hanken Grotesk (variable, system-ui fallback)
**Label/Mono Font:** system monospace for code only

**Character:** Anybody pushed to its widest, heaviest italic reads as a shouted instruction. Hanken Grotesk stays plain and medium so the shouting has somewhere to rest.

### Hierarchy
- **Display** (900 italic caps, clamp(3.6rem, 12vw, 9rem), 0.92): the hero "Stand up!" only, each line skewed and stacked.
- **Headline** (900 italic caps, clamp(2.4rem, 7vw, 4.6rem), 0.92, -0.02em): section titles, always inside a skewed span.
- **Set Title** (900 italic caps, clamp(2.6rem, 9vw, 6rem), 0.95): the Sit / Stand / Walk rows, with a smaller sub-line (clamp 1rem to 2.2rem).
- **Title** (900 italic caps, 1.7rem to 1.9rem, 1): move cards, nag heading, FAQ summaries at 1.25rem.
- **Body** (500, 18px, 1.55): paragraphs at 30 to 62ch; lede is 1.3rem at weight 700, 34ch.
- **Label** (700 to 800 caps, 0.8 to 0.85rem, 0.06 to 0.08em): nav links, timer menu row, nag stage tags, copy button.

### Named Rules
**The Shout Rule.** Anything set in Anybody is italic, caps, weight 900. No upright or light cuts of the display face.

## Layout

Single column inside a 1040px wrapper with 16px side gutters. Sections are full-bleed colour fields stacked vertically; the hero is a 1.25fr / 1fr grid (copy left, timer right). Sets are a two-column row (title, note) under a 6px ink rule; moves are a two-column grid with 48px column gap and 4px top rules; nag stages are four across. Spacing rhythm: 10, 16, 28, 56, 96px. At 760px and below everything collapses to one column, nag stages to two, and step numerals shrink from 4.4rem to 3rem.

Sections join through skewed stripe bands (44px tall, skewY -2.2deg, pink / yellow / cyan thirds, reversed on alternate joins) and a 64px bleed pseudo-element so fields overlap without seams.

## Elevation & Depth

Flat colour fields carry the structure; depth appears only as soft, offset drop shadows under objects that look lifted off the page and tilted.

### Shadow Vocabulary
- **Lift** (`box-shadow: 6px 8px 14px rgba(18,10,15,.4)`): the primary button at rest; grows to `8px 12px 18px` on hover, shrinks to `3px 4px 8px` when pressed.
- **Badge** (`box-shadow: 10px 14px 24px rgba(18,10,15,.35)`): the live timer badge.
- **Headline cast** (`text-shadow: 5px 5px 18px rgba(18,10,15,.35)`): hero white headline over pink only.

### Named Rules
**The Lifted-Object Rule.** Shadows go under tilted or skewed objects only. Flat fields, rules and text blocks stay shadowless.

## Shapes

Square. Radius is 0 on every button, badge, panel and code block. Silhouette comes from skew (-8deg on headlines and buttons), tilt (-2.5deg timer, 1deg nag panel) and the diagonal stripe bands. Structure is drawn with thick ink rules (3px borders, 4px list rules, 6px set rules). The logo is a yellow parallelogram badge with a stroked raised-arm figure.

## Components

### Buttons
- **Shape:** square, skewed -8deg.
- **Primary:** ink fill, acid-yellow Anybody italic caps 1.1rem, padding 16px 30px, Lift shadow.
- **Hover / Active:** hover moves (-2px, -3px) with a deeper shadow; active presses (+2px, +3px) with a tighter one; 0.15s springy ease (cubic-bezier(.2,.8,.2,1)).
- **Alt:** transparent, ink text, 3px ink border, no shadow, sits beside primary (10px gap, stacks with 14px gap on mobile).

### Timer Badge (signature)
Yellow card tilted -2.5deg with the Badge shadow. A small uppercase menu row over a 3px ink rule, a giant Anybody phase word, a pink clock with a 2px ink stroke (tabular numerals), and a shout line. On each phase change it jolts (0.5s scale and skew settle); reduced-motion users get a static badge.

### Code Blocks
Terminal Black fill, 3px cyan border, cyan 15px monospace, no radius, horizontal scroll. A cyan copy button sits top-right (uppercase 12px label, yellow on hover), label flips to "copied".

### Set List and Moves
Rows divided by thick ink top rules; Anybody italic titles with plain 700-weight notes at 30 to 36ch.

### Nag Panel
Ink panel tilted 1deg: yellow title, four stages each under a 4px pink rule with a cyan caps label.

### Navigation
Brand badge plus uppercase 0.85rem links at weight 700; hover is a 3px underline with 5px offset. Wraps rather than collapsing.

### FAQ
Native details/summary with 4px ink rules; summaries are Anybody italic caps 1.25rem.

## Do's and Don'ts

### Do:
- **Do** drench each section in one neon (#ff2d95, #e6ff00 or #00e1ff) with ink (#120a0f) text.
- **Do** set display type in Anybody 900 italic caps and skew headlines -8deg.
- **Do** keep corners square and draw structure with 3 to 6px ink rules.
- **Do** join fields with the tri-colour stripe band, flipping its order on alternate joins.
- **Do** keep focus rings 4px: ink on neon, yellow on ink.
- **Do** write copy in a shouting coach voice, and keep real facts real.
- **Do** honour prefers-reduced-motion by stopping the demo loop, jolt and button transitions.

### Don't:
- **Don't** add glow, haze, synthwave grids or suns; the world is flat Day-Glo, not neon-sign.
- **Don't** round corners or soften buttons into pills.
- **Don't** set text in Anybody upright or light, or in lowercase.
- **Don't** put shadows under flat fields or text blocks.
- **Don't** reach for calm teal or white wellness-app surfaces.

### Not canonized (defects the build carries)
- Emoji faces (U+1F615 family) as the nag-stage icons are glyph icons; do not reuse them as an icon system.
- The favicon strokes with #1a0638 while the page mark uses #120a0f; ink drift, not a second ink.
- White hero headline on hot pink is roughly 3.4:1, tolerable only at display size; do not use white on pink for text below large size.
