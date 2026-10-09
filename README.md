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

## Before going live — replace placeholders

Search `index.html` for text in **[square brackets]**:

1. **Address, phone, email** in the Contact section (and the `tel:` / `mailto:` links).
2. In `js/main.js`, set `CONTACT_EMAIL` to the address that should receive enquiries.
3. Review the **Products** section — the four product areas are general examples; update them to match the actual portfolio.
4. Review About / Quality wording so every claim matches what the company can verify (add licences or certifications only if they apply).

## Contact form

By default the form opens the visitor's email app with the message pre-filled (works on any static host). To receive submissions directly instead, connect a form service such as Formspree or Netlify Forms and remove the submit handler in `js/main.js`.

## Deploying

Upload the whole folder to your repository root. It works on GitHub Pages, Netlify, Vercel, cPanel hosting or any static host — `index.html` is the entry point.

To preview locally, open `index.html` in a browser, or run:

```bash
python3 -m http.server 8000
```

then visit http://localhost:8000.

## Print note

Brand HEX values are digital approximations from the raster logo. Confirm master colours from approved vector artwork before using them for print.
