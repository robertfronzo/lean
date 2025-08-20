# lean → liquid

a tiny experimental syntax for writing [shopify liquid](https://shopify.dev/docs/api/liquid) with less noise.

credit: robert julian fronzo 2025

## why

- reduce boilerplate when writing liquid.
- favor readable, indentation-friendly patterns for common constructs.
- keep deployment simple: compile locally, upload plain `.liquid` to your theme.

## features (v0)

- `= expr` → `{{ expr }}` output shorthand  
- `name := value` → `{% assign name = value %}`  
- control flow: `if/elsif/else: … end`, `for x in xs: … end`, `case/when`, `capture name: … end`  
- `render 'snippet', a:b, c:d` → `{% render 'snippet', a: b, c: d %}`  
- filter sugar: `|>` becomes `|` (e.g., `title |> escape`)  
- raw html/text passes through  
- schema passthrough: a `schema:` … `endschema` block becomes `{% schema %} … {% endschema %}`

## install

no runtime install is required. the transpiler is a single python file.

requirements:
- python 3.8+

clone or copy the repo contents anywhere on your machine.

## quick start

```bash
# transpile a single file
python3 scripts/lean2liquid.py lean/promo-banner.lean > compiled/promo-banner.liquid

# transpile all demo files
for f in lean/*.lean; do python3 scripts/lean2liquid.py "$f" > "compiled/$(basename "${f%.lean}.liquid")"; done
```

upload the generated `.liquid` files to your theme:
- section files → `sections/`
- snippet files → `snippets/`

## editor workflow (optional)

use a file watcher to auto-compile on save. for example with `watchexec`:

```bash
watchexec -e lean 'for f in lean/*.lean; do python3 scripts/lean2liquid.py "$f" > "compiled/$(basename "${f%.lean}.liquid")"; done'
```

## language guide

**output**
```
= product.title |> escape
```
becomes
```
{{ product.title | escape }}
```

**assign**
```
price_text := product.price | money
```
becomes
```
{% assign price_text = product.price | money %}
```

**if / elsif / else**
```
if product.available:
  <span>in stock</span>
elsif product.tags contains 'backorder':
  <span>backorder</span>
else:
  <span>sold out</span>
end
```

**for**
```
for p in collection.products:
  <li>= p.title |> escape</li>
end
```

**capture**
```
capture blurb:
  <p>= section.settings.blurb |> escape</p>
end
```

**render**
```
render 'price', product:product, show_compare:true
```

**schema passthrough**
```
schema:
{
  "name": "promo banner",
  "settings": [{ "type":"text", "id":"message", "label":"message" }]
}
endschema
```

## demo files

- `lean/promo-banner.lean` → section with a simple text message field (compiles to `compiled/promo-banner.liquid`)
- `lean/collection-grid.lean` → generic collection product grid (compiles to `compiled/collection-grid.liquid`)
- `lean/utility-badges.lean` → snippet rendering “sale” and “new” badges (compiles to `compiled/utility-badges.liquid`)

## limitations

- the transpiler is intentionally minimal. it does not validate indentation or syntax beyond simple patterns.
- no in-theme compilation: shopify themes only execute liquid. compile locally, then upload.
- avoid mixing tabs/spaces; stick to consistent indentation.

## license / credit

this demo is public-domain style for your convenience. attribution is appreciated:  
**credit: robert julian fronzo 2025**
