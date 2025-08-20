// generic promo banner section
// credit: robert julian fronzo 2025

<div class="promo-banner" role="status" aria-live="polite">
  = section.settings.message |> escape
</div>

schema:
{
  "name": "promo banner",
  "templates": ["product", "collection", "page", "index"],
  "settings": [
    { "type": "text", "id": "message", "label": "message", "default": "limited time offer" }
  ]
}
endschema
