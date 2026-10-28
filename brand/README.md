# TARDIS visual identity

This folder contains the approved Keystone identity and its use in the PS5 WebKit Autoloader.

## Approved direction

Keystone is an evolutionary redraw of the existing paired-pillar mark used by Tardis and Tardis Games. The mirror-balanced geometry preserves the recognition cue while making the symbol dependable at app-icon and favicon sizes. The custom TARDIS wordmark uses a compact geometric alphabet with square terminals; the T has a centered stem, the A has an open counter, and the R has a short diagonal leg. Keep the symbol and wordmark proportions fixed in the supplied lockups.

## Files

- `logo/` contains the primary vector masters: symbol, small-size symbol, custom wordmark, horizontal signature, and stacked signature.
- `exports/` contains black, reversed, indigo, square, app-icon, favicon, PNG, and web/PWA icon exports.
- `pattern/` contains the paired-pillar repeat graphic.
- `brandbook.md` is the editable source for the PDF guide in `../output/pdf/`.
- `renders/` contains review renders used while designing; use the SVG masters for production.

## Core colors

- Tardis Indigo: `#0A00B0`
- Midnight: `#080914`
- Panel: `#14152F`
- Paper: `#F5F5FF`
- Lavender: `#A6A2FF`
- Signal Cyan: `#56C7FF`

Use indigo as the signature brand color on light surfaces and as an app-icon tile. On dark interfaces, place the white or lavender logo on a calm surface; indigo alone does not have enough contrast against the dark background.

## Type

The logo's TARDIS letters are outlined as vectors. Product interface typography uses the system sans stack `-apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif`; diagnostic output uses `SFMono-Regular, Consolas, monospace`. No remote font or image request is needed.

## Product application

The PS5 setup installer, homescreen app name, pointer page, autoloader header, and generated console icon carry the Tardis identity. Technical exploit names, payloads, queue order, logs, and firmware compatibility remain explicit and readable.

Trademark clearance was not part of this design work.
