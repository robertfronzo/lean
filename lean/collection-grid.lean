// simple collection grid
// credit: robert julian fronzo 2025

if collection:
  <div class="grid grid--2-col">
    for p in collection.products:
      <article class="card">
        <a href="{{ p.url }}">
          <h3 class="card__title">= p.title |> escape</h3>
          <div class="card__price">{{ p.price | money }}</div>
        </a>
      </article>
    end
  </div>
else:
  <p>no collection context found.</p>
end
