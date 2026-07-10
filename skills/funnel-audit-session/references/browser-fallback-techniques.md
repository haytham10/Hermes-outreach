# Browser Fallback Techniques — Funnel Walk via Browser Tools

When the Funnel Auditor CLI fails (Playwright not installed, greenlet crash, timeout), fall back to browser tools. These techniques compensate for the CLI's absence by extracting the same information manually.

## Technique 1 — Full Page Text Extraction

**Problem:** `browser_snapshot` truncates long pages (sales pages with FAQs, pricing sections, module descriptions). The snapshot summary loses the bottom half of the page, including critical data like pricing FAQs and testimonial sections.

**Solution:** Use `browser_console` with `expression` to extract the full text:

```js
document.body.innerText.substring(0, 15000)
```

This returns all visible text on the page, including:
- FAQ sections (often near the bottom with pricing Q&As)
- Testimonials
- Module descriptions
- Footer disclaimers
- Terms and pricing disclaimers

**When to use:** After navigating to a long sales/offer page and scanning the snapshot, if the page appears cut off. Always follow up a long sales page visit with a full text extraction.

**Limits:** Returns up to 15,000 chars by default. Increase to 20000 or 25000 for very long pages. Returns nothing useful if the page is behind a paywall/login gate.

## Technique 2 — Hidden Checkout / Offer URL Discovery

**Problem:** CTA buttons like "I Need This Now" or "Join Now" may scroll to another section, or their `href` isn't visible in the snapshot (rendered as `<button>` with JavaScript click handlers, not `<a>` tags). The checkout URL is embedded in the DOM but not surfaced.

**Solution:** Query the DOM for known URL patterns via `browser_console`:

```js
// Find Kajabi offer/checkout links
document.querySelector('[href*="offers"], [href*="checkout"], [href*="cart"]')
    ? document.querySelector('[href*="offers"], [href*="checkout"], [href*="cart"]').href
    : 'NOT FOUND'
```

This works for:
- **Kajabi sites**: offers are at `/offers/{id}/checkout` or `/resource_redirect/offers/{id}`
- **Teachable/Thinkific**: checkout URLs contain `/checkout` or `/enroll`
- **Shopify**: links to `/cart/` or `/checkout`
- **Custom sites**: search for `/buy`, `/purchase`, `/order`, `/checkout`, `checkout_url`

**When to use:** After visiting a sales/offer page where the CTA buttons are `<button>` elements without visible hrefs, and pricing isn't shown on the page itself.

**If blocked (Cloudflare):** Kajabi checkout pages often trigger Cloudflare bot protection. When the browser hits Cloudflare, the page title becomes "Attention Required! | Cloudflare". You can still get the checkout URL from the parent page — that's the discovery win. Record the URL in the audit as "checkout URL discovered: {url} (Cloudflare blocked direct inspection)."

## Technique 3 — Page URL Verification

**Problem:** After clicking a button, the page may scroll in-page (anchor link) rather than navigating. You need to know whether you ended up at a new URL or stayed on the same page.

**Solution:**

```js
window.location.href
```

Returns the current URL. Compare to the previous URL to detect in-page navigation vs. page transitions.

## Technique 4 — Browser Vision for Lazy-Loaded or Off-Screen Content

**Problem:** Some content (pricing, FAQ accordions, tabs) is only visible after user interaction (clicking, scrolling to a specific section).

**Solution:** Scroll to the area, then screenshot:
1. `browser_scroll(direction='down')` to reveal hidden sections
2. `browser_vision` to read what's shown (with tight prompt: "Max 80 words, 3 bullets")

**Pitfall:** Vision models are slow (~40-50s) and unreliable for reading specific prices. Prefer `browser_console` with DOM queries for pricing:

```js
// Find price text on various page areas
document.querySelector('[class*="price"], [class*="pricing"], [data-testid*="price"]')
    ?.textContent || 'NOT FOUND'
```

## When to Use Which

| Situation | Technique |
|---|---|
| Sales page feels truncated in snapshot | Technique 1 — Full text extraction |
| CTA looks like `<button>` not `<a>` | Technique 2 — Hidden URL discovery |
| Checkout page shows Cloudflare | Technique 2, then record as blocked |
| Need to confirm page change after click | Technique 3 — URL verification |
| Pricing not in DOM text (image-based) | Technique 4 — Vision (with tight prompt) |