# Delta Pharma (Pvt.) Limited — Website

A responsive, single-page static website built on the Delta Pharma brand kit and premium web font kit. No build step or server required — plain HTML, CSS and JavaScript.

## Structure

```
delta-pharma-website/
├── index.html                      # All page content
├── favicon.ico                     # Browser tab icon (16, 32, 48 px)
├── css/styles.css                  # Brand colours, typography, layout
├── js/main.js                      # Mobile menu, scroll effects, contact form
├── js/products.js                  # Product category filter, search and detail popup
└── assets/images/
    ├── delta-pharma-logo.jpg       # Original supplied logo (unchanged)
    ├── delta-pharma-logo-trim.jpg  # Same artwork with outer whitespace trimmed (used on site)
    ├── delta-pharma-icon.png       # Logo mark only (512×512)
    ├── apple-touch-icon.png        # 180×180 home-screen icon
    ├── favicon.png                 # 48×48 icon (older; the site now uses /favicon.ico)
    ├── chairman-ashfaq-paracha.jpg # Chairman portrait (Leadership section)
    ├── v/d-4f7c2a.jpg              # Licence to Manufacture (shown only via footer "Document verification")
    └── products/                   # Product pack photos
```

## Products

The Products section lists all 33 registered products from the product details sheet, grouped as Tablets, Capsules, Syrup and Dry Suspension. Each product card is written into `index.html`. The details shown in the product popup (composition, pack size, registration number, M.R.P., photos) come from the `product-data` JSON block at the end of the Products section in `index.html`. When a price or pack size changes, update it in both the card and the JSON block.

Products without a photo show a "Photo coming soon" tile. To add a photo, save it in `assets/images/products/` and add its file name (without `.jpg`) to that product's `images` list in the JSON block, then replace the tile in its card with an `<img>`.

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

## Licence document

The licence image is not shown on the page. It opens only after three clicks: the small "Document verification" link in the footer, "Request document copy", then "I understand, show document". The image path appears only in `js/products.js` and is excluded from search engines in `robots.txt`. Anyone determined can still find it, so do not treat it as private.

## Contact details

Contact details (address, telephone, cell/WhatsApp, CEO) are in the Contact section and footer of `index.html`.

## Contact form

The form opens WhatsApp with the visitor's message pre-filled, sent to the number in `CONTACT_WHATSAPP` in `js/main.js`. To receive messages by email instead, put an address in `CONTACT_EMAIL` in the same file. To store submissions directly, connect a form service such as Formspree and remove the submit handler.

Review the **Products**, About and Quality wording so every claim matches what the company can verify.

## Updating the design

After changing `css/styles.css` or `js/main.js`, raise the `?v=` number on their links in `index.html` (e.g. `?v=5` → `?v=6`) so visitors' browsers load the new version instead of an old saved copy.

## Deploying

Upload the whole folder to your repository root. It works on GitHub Pages, Netlify, Vercel, cPanel hosting or any static host — `index.html` is the entry point.

To preview locally, open `index.html` in a browser, or run:

```bash
python3 -m http.server 8000
```

then visit http://localhost:8000.

## Print note

Brand HEX values are digital approximations from the raster logo. Confirm master colours from approved vector artwork before using them for print.
