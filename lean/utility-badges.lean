// general purpose product badges snippet
// credit: robert julian fronzo 2025

capture sale_badge:
  if product and product.compare_at_price > product.price:
    <span class="badge badge--sale">sale</span>
  end
end

capture new_badge:
  if product and product.tags contains 'new':
    <span class="badge badge--new">new</span>
  end
end

<div class="product-badges">
  = sale_badge
  = new_badge
</div>
