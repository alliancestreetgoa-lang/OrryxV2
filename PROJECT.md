# Orryx Commodities L.L.C-FZ — Website, Version 2

A second, completely different design for the same client. Version 1 stays as it is in `~/orryx-commodities` (repo `ORRYX`). Nothing in Version 1 was changed.

- **Local folder:** `~/orryx-v2`
- **Local preview:** `cd ~/orryx-v2 && python3 -m http.server 5300` → http://localhost:5300/
- **Repo:** https://github.com/alliancestreetgoa-lang/OrryxV2 (private; not live anywhere yet)
- **Built:** 20 November 2026

## The one rule that matters most: the logo

The owner said: use the registered logo **exactly as it is, with no changes**.

- The registered logo is the supplied file `assets/src/OC Logo - Dark Theme.png`.
- The site does not redraw it. `tools/trace_logo.py` follows the edges of that file point by point and writes the vector shapes. Check: `tools/compare.html` lays the vector over the original and counts differing pixels (1 of 1,573,538 differs by more than half; 237 by more than a quarter, all on soft edges).
- Never edit the logo shapes by hand, never type the name in a font to stand in for it, never use an AI redraw. A ChatGPT redraw was made early on 20 Nov and was thrown away because it was not exact.
- The orange mark never changes colour. Only the letters switch between white (on black) and black (on white), which are the two versions the owner supplied.
- The orange logo cannot sit on an orange background, so in the orange template it is always shown on a black plate. In all three templates the logo sits on its own black or white plate.
- To re-trace (only if the owner supplies a new logo file): replace the source file, run `python3 tools/trace_logo.py` from the project folder, then paste `tools/logo-defs.html` between the `LOGO-DEFS:START` and `LOGO-DEFS:END` marks in `index.html`.

Ready-made logo files for other uses are in `assets/logo/`: four SVG files (sharp at any size) and four PNG files 7,096 px wide (dark, light, transparent with white letters, transparent with black letters).

## Colours and type

Only the three logo colours are used, plus see-through versions of them:

| Colour | Value | Where it comes from |
|---|---|---|
| Orange | `#FE9102` | measured from the registered logo file |
| Black | `#000000` / `#060605` | logo background / letters in the supplied light version |
| White | `#FFFFFF` | logo letters |

Three colour templates, switched with the three dots in the menu bar (the choice is remembered on that device):

1. **Night** — black page, orange accents (the default).
2. **Day** — white page, orange accents, black text.
3. **Ember** — orange page, black accents.

Type: **Montserrat** for headings and labels (the closest web font to the logo's lettering) and **Manrope** for paragraphs. Arabic: Noto Kufi Arabic.

## The client (unchanged from Version 1)

| Item | Detail |
|---|---|
| Company | Orryx Commodities L.L.C-FZ (اوريكس كوموديتيز ش.ذ.م.م - منطقة حرة) |
| Free zone | Meydan Free Zone, Dubai, U.A.E. |
| Licence No. | 2538901.01 (formation No. 2538901) |
| Company type | Limited Liability Company |
| Manager | Stallone Dominic Shaikh |
| Issued / valid to | 17/10/2025 → 16/10/2027 |
| Address | Meydan Grandstand, 6th floor, Meydan Road, Nad Al Sheba, Dubai, U.A.E. |

Licensed activities: 7020.00 management consultancy, 7020.11 strategy advisory, 6619.14 financial consultancy (activity authorisation issued 18/11/2026), 7490.02 business brokerage of small and medium sized businesses including professional practices, **not real estate brokerage**.

**Content rules (same as Version 1)**

- Do not claim commodity trading. It is not on the licence.
- Brokerage wording must keep "not real estate brokerage".
- Only state facts the client has given. No invented phone, email, clients or reviews.
- Our own wording, for the client to confirm: the four "feelings" and their quotes, the activity descriptions, the five-step method, the brokerage steps.

## Files

```
index.html          the whole page (the traced logo shapes are near the top)
css/style.css       all styles; the three templates are the first three blocks
js/main.js          all motion and behaviour
vendor/             GSAP 3.12.5, ScrollTrigger, Lenis 1.1.14 (same local copies as Version 1)
assets/img/         hero, management, strategy, finance, brokerage, method, dubai, enquire (.webp),
                    favicon.png, apple-touch-icon.png, og.png
assets/src/         the three logo files the owner supplied + full-size originals of the eight pictures
assets/logo/        exact logo exports (SVG and 7,096 px PNG)
tools/              trace_logo.py, logo-defs.html, compare.html
```

No build step. Plain HTML, CSS and JavaScript.

## Sections (top to bottom)

1. **Opening** — the exact logo draws itself in, then the page lifts away.
2. **Hero** — glass picture of the four services on an orange ribbon; headline "One continuous line from your question to a closed deal."; two buttons; four facts in a glass bar. The hero is always a dark scene, in every template.
3. **Moving band** — the four activity names; speeds up with scrolling.
4. **01 Start here** — "How does the business feel right now?" Four feelings (Stretched, Unsure, Exposed, Ready). Each one changes the quote, the answer and how the orb moves, and points to one licensed activity.
5. **02 Licensed activities** — four glass cards that stack on top of each other while scrolling, each with its picture and a small moving diagram.
6. **03 Method** — five steps; the picture pans and a bar fills as each step is reached.
7. **04 Brokerage desk** — seller ↔ Orryx logo ↔ buyer with flowing lines; Prepare, Match, Arrange.
8. **05 Licence** — glass licence card that tilts with the mouse, with a ring counting the days left to 16/10/2027; registered address with Maps link.
9. **06 Questions** — the same six questions and answers as Version 1.
10. **07 Enquire** — enquiry form.
11. **Footer** — details, template switch, the exact logo large.

## Pictures

Eight pictures were generated on 20 November 2026 in ChatGPT (Chrome), in one chat titled "Recreate exact logo image". Shared style: clear liquid glass, glowing orange light, pure black background, no text. They are always shown inside dark frames, so they look right in all three templates.

## How to change things

- **Enquiry email:** set `CONTACT_EMAIL` at the top of `js/main.js`. While it is empty the form shows a holding message.
- **After editing CSS or JS:** raise the `?v=` number on the `style.css` and `main.js` links in `index.html`, or browsers keep showing the old version.
- **Licence renewal:** the dates are in `js/main.js` (`start` and `end`) and as text in `index.html` (licence card, Questions, footer).
- **Testing the opening:** add `?hold=1.2` to the address to freeze the opening animation at that second.

## Things learned while building (for whoever edits next)

- GSAP rounds pixel values to whole numbers unless `autoRound: false` is set. This froze the line-drawing and the licence ring until fixed.
- Do not put a CSS `transition: transform` on anything GSAP also moves. Hover moves here use the separate `translate` property instead.
- `img { max-width: 100% }` silently caps a picture that is meant to be wider than the screen (phone hero). That rule has `max-width: none`.
- Full-page screenshots give wrong results because the hero uses screen-height units. Take screen-sized shots while scrolling.

## Tested

20 November 2026, all with no errors and no sideways scrolling: 1440×850 (all three templates, every section), 1366×768, 1280×620 (hero fits one screen), 1024×768, 768×1024, 390×720, 360×640.

## Open items

- Not live. The repo is private. To publish like Version 1 it must be made public and GitHub Pages switched on. The owner decides.
- The page carries `noindex`, so search engines ignore it while two versions exist. Remove that line (and add the Version 1 search files: JSON-LD, sitemap.xml, robots.txt, llms.txt) only if this version is chosen as the real site.
- No service pages in this version yet (Version 1 has four).
- Still needed from the client: email, phone, domain. The enquiry form is not connected.
- Client to confirm our descriptive wording, as in Version 1.
