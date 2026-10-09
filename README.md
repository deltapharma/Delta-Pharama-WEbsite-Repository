# Delta Pharma (Pvt.) Limited — Website

A responsive, single-page static website built on the Delta Pharma brand kit and premium web font kit. No build step or server required — plain HTML, CSS and JavaScript.

## Structure

```
delta-pharma-website/
├── index.html                      # All page content
├── css/styles.css                  # Brand colours, typography, layout
├── js/main.js                      # Mobile menu, scroll effects, contact form
└── assets/images/
    ├── delta-pharma-logo.jpg       # Original supplied logo (unchanged)
    ├── delta-pharma-logo-trim.jpg  # Same artwork with outer whitespace trimmed (used on site)
    ├── delta-pharma-icon.png       # Logo mark only (512×512)
    ├── apple-touch-icon.png        # 180×180 home-screen icon
    └── favicon.png                 # 48×48 browser tab icon
```

## Brand system applied

| Token | Value | Used for |
|---|---|---|
| Primary Navy | `#102F67` | Headings, navigation, "Why Delta" band |
| Pharma Blue | `#087FBD` | Links, buttons, section markers |
| Clinical Teal | `#12A6A0` | Icons and restrained accents |
| Bright Cyan | `#20B6D2` | Subtle background glow only |
| Slate Grey | `#687784` | Captions, secondary text |
| Mist Grey | `#F3F7FA` | Panels, alternating sections, footer |
| Ink | `#1E2B39` | Body text |

- **Headings, navigation, buttons:** Montserrat 600/700
- **Body text, captions:** Open Sans 400/600 (16 px minimum)
- Fonts load from Google Fonts with Arial/Helvetica fallbacks.
- The logo artwork is used as supplied — never recreated with typed text.

## Contact details

Contact details (address, telephone, cell/WhatsApp, CEO) are in the Contact section and footer of `index.html`.

## Contact form

The form opens WhatsApp with the visitor's message pre-filled, sent to the number in `CONTACT_WHATSAPP` in `js/main.js`. To receive messages by email instead, put an address in `CONTACT_EMAIL` in the same file. To store submissions directly, connect a form service such as Formspree and remove the submit handler.

Review the **Products**, About and Quality wording so every claim matches what the company can verify.

## Deploying

Upload the whole folder to your repository root. It works on GitHub Pages, Netlify, Vercel, cPanel hosting or any static host — `index.html` is the entry point.

To preview locally, open `index.html` in a browser, or run:

```bash
python3 -m http.server 8000
```

then visit http://localhost:8000.

## Print note

Brand HEX values are digital approximations from the raster logo. Confirm master colours from approved vector artwork before using them for print.
