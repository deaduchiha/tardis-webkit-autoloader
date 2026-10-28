# TARDIS

## Visual identity guide

Version 1.0 · 28 October 2026

### Brand idea

**A clear way through complex systems.** Tardis brings a calm, dependable interface to technical tools. The paired pillars stand for structure and a passage between them: a memorable form that belongs to the Tardis name, rather than a generic chip, shield, or orbit.

### Equity and audience

The twin-pillar silhouette and saturated indigo already identify Tardis across Tardis and Tardis Games. Keep those two anchors. The audience includes people configuring homebrew and game libraries, plus technical contributors. Brand behavior should feel capable, precise, transparent, and composed.

## 1. Logo

The primary mark is the paired pillars. Each half is a mirrored solid form on a 256-unit square grid. A 16-unit central opening remains visible at small sizes. The angled shoulders use a consistent 15-degree cut. The mark is intentionally bold and silhouette-led.

The logo family includes symbol-only, custom TARDIS wordmark-only, horizontal signature, stacked signature, small-size symbol, black, white, indigo, square, app-icon, favicon, and web/PWA icon versions. Use the supplied vector masters; do not rebuild the lettering from a keyboard font.

### Clear space and size

Keep at least 24 units of clear space around the symbol, equal to the standard mark's side margin. Scale this zone with the logo. In lockups, leave at least the height of the letter T between mark and wordmark.

Minimums: symbol 16 px (use the small-size SVG below 24 px); wordmark 96 px wide; horizontal signature 140 px wide; print symbol 6 mm high and horizontal signature 28 mm wide. If the wordmark cannot meet its minimum, use the symbol alone.

### Backgrounds and handling

Preferred pairings are indigo on white or pale neutral, white on Tardis Indigo or Midnight, and white on a quiet dark image area. Use the square/app-icon asset when a container is needed. Maintain the supplied proportions and spacing. Do not stretch, rotate, outline, add shadows or gradients, recolor outside the palette, rearrange components, or place the mark over busy imagery.

## 2. Color

| Color | HEX | RGB | Approx. CMYK | Use |
|---|---|---|---|---|
| Tardis Indigo | `#0A00B0` | 10, 0, 176 | 94, 100, 0, 31 | Primary logo, icons, selected controls |
| Midnight | `#080914` | 8, 9, 20 | 60, 55, 0, 92 | Dark interface canvas |
| Panel | `#14152F` | 20, 21, 47 | 57, 55, 0, 82 | Cards and console surfaces |
| Paper | `#F5F5FF` | 245, 245, 255 | 4, 4, 0, 0 | Primary text on dark surfaces |
| Lavender | `#A6A2FF` | 166, 162, 255 | 35, 36, 0, 0 | Accessible dark-mode accent |
| Signal Cyan | `#56C7FF` | 86, 199, 255 | 66, 22, 0, 0 | Optional secondary highlight |

CMYK values are starting estimates; use the printer's ICC profile or spot-color specification for final production. Print runs should prioritize a solid one-color indigo or black master when color matching is not controlled.

Semantic interface colors are not logo colors: success `#88E6BC`, caution `#F3C977`, and error `#FF858E`. Pair every status color with a written status and preserve contrast; never communicate state by color alone.

## 3. Typography

The TARDIS wordmark is custom vector artwork. Use it as supplied. For product interfaces and brand communications, use the native system sans stack `-apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif`. It requires no download and remains readable on the PS5 WebKit browser and desktop systems. Use regular for body copy, semibold for controls and labels, and bold for headlines. Keep headlines short and sentence case outside the uppercase logo.

Use `SFMono-Regular, Consolas, "Liberation Mono", monospace` for payload names, logs, addresses, and version strings. Keep technical text at 14 px or larger in desktop views and 13 px or larger on compact screens where practical. Use 1.5 line height for explanatory copy and 1.6 for console output.

## 4. Shape, pattern, and layout

The paired-pillar repeat in `pattern/tardis-pillar-pattern.svg` is a quiet background texture. Use it at low opacity on large, calm surfaces; do not place it behind diagnostic copy. The pattern borrows the pillar geometry but leaves enough open field for content.

Use an 8 px spacing rhythm in digital layouts, with generous outer margins and a clear hierarchy. Prefer simple filled icons with consistent weight and squared or lightly rounded corners. Use 12 px card radii in the autoloader interface; reserve stronger indigo for selected or active controls. Keep error logs visually distinct and easy to scan.

## 5. Imagery and voice

Imagery should be purposeful, low-noise, and technically grounded: hardware, software surfaces, or restrained abstract structures. Favor dark navy or neutral fields with natural detail and one indigo cue. Avoid stock cyberpunk grids, glowing shields, generic chip outlines, and exploit screenshots used as decoration.

Write in a calm, direct voice. Say what is happening, what the user should do, and what the tool supports. Keep exploit and firmware details factual. Avoid exaggerated promises or vague claims of safety. Example: “ELF loader already running. Nothing to do.”

## 6. Motion and sound

The logo is static in core product screens. If used in a separate brand intro, reveal the two pillars from the center outward and resolve to the exact supplied mark within 600 ms. Do not delay exploit startup or obscure status text. Respect reduced-motion settings. No sound cue is defined for this identity.

## 7. PS5 WebKit Autoloader application

Use the brand header with symbol, TARDIS name, and the product descriptor “WebKit Autoloader.” The console remains the information priority: it is plain text, scrollable, and capped to a manageable number of lines. Keep progress labels descriptive, and retain the native payload log colors for success, warning, and error messages. The installer choice cards should have clear keyboard/controller focus and visible selected states.

The PS5 homescreen icon is a white paired-pillar mark on a solid indigo tile with 10 percent safe padding. Keep the name “Tardis WebKit Autoloader” in app metadata. Do not add remote fonts, images, or runtime dependencies to offline pages.

## 8. Assets and stewardship

Use `logo/` as the vector source of truth and `exports/` for ready-to-use raster and web sizes. Use RGB assets for screens and the one-color vector for controlled print production. The wordmark's final S is a consistent 8-unit vector stroke; keep its stroke width proportional when resizing. Review the rendered lockups before supplier handoff.

The PS5 project applies these rules in `frontend/autoloader/`, `frontend/installer-page/`, `frontend/pointer/`, and `assets/`. Review future changes against the logo, contrast, offline, and console-readability rules above. Trademark clearance and font licensing beyond the system fonts were not part of this work.
