# ReadMe — Semantic HTML

This document summarizes key learnings about semantic HTML tags and how to use them effectively.

## Purpose
- Convey meaning to browsers, developers, and assistive technologies.
- Improve accessibility, SEO, and code maintainability.

## Common semantic elements
- header — site or section header (branding, headings, global nav).
- nav — primary navigation links.
- main — primary page content (one per page).
- article — self-contained content (blog post, news item).
- section — thematic grouping within content (use with heading).
- aside — tangential content (sidebars, related links).
- footer — footer for a section or page (copyright, links).
- figure / figcaption — images with captions.
- details / summary — disclosure widgets.
- address — contact information.
- time, mark — temporal data and highlighted text.

## Best practices
- Use elements for semantics, not just styling.
- Only one <main> per page.
- Keep heading order logical (h1 → h2 → h3).
- Use landmarks to aid screen reader navigation.
- Add ARIA only when native semantics are insufficient.
