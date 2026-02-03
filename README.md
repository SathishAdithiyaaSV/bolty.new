# Bolty Website Generator

This repo provides a small, automated workflow to generate a static website from a JSON specification. It is intended as a starting point for integrating with an existing website or API that defines your site content.

## Quick Start

1. Create a JSON spec (or copy the example).
2. Run the CLI to generate `index.html`.

```bash
python -m site_builder.cli --spec spec.example.json --output dist
```

The generated site will live in `dist/index.html`.

## JSON Specification

```json
{
  "title": "Acme Studios",
  "tagline": "We build delightful digital products.",
  "sections": [
    {
      "heading": "Services",
      "content": "Brand strategy, product design, and engineering."
    },
    {
      "heading": "Contact",
      "content": "hello@acmestudios.example"
    }
  ]
}
```

## Next Steps

- Replace the JSON spec with data pulled from your website or API.
- Add more templates for multi-page output.
- Extend the CLI to accept remote content sources.
