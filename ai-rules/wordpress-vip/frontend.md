## WordPress VIP Go — Frontend (Sage + Tailwind + Alpine)

### Tailwind
- No dark mode — never use `dark:` prefixes or dark-mode config.
- Component classes (`.btn-primary`, etc.) only once a utility combination
  repeats 3+ times; otherwise use utilities inline.

### Alpine.js
- Guard against undefined with `x && x.length`, not optional chaining, for
  broader browser support in Alpine expressions.
- Debounce user input (`@input.debounce.300ms`) instead of firing on every
  keystroke.
- Avoid global JS variables; if one is unavoidable, prefix it `pn*`.

### Entity label in Blade
`$website` is available on every Blade view via `App\View\Composers\App`
(`'*'` wildcard) — use `$website->entityLabel(plural: ..., lowercase: ...)` for
any user-facing noun (see the backend entity-label rule for the API). Only
substitute text a human reads as English copy — leave URL slugs, post type
slugs, CSS classes, HTML `id`s, Cypress `data-cy` selectors, Alpine state
values, and ACF field names as `player`/`players`. When a substituted phrase
reads awkwardly, restructure the copy rather than force it.

### Accessibility (required, not optional)
Semantic HTML, ARIA labels where native semantics don't cover it, full keyboard
navigation, and WCAG-compliant color contrast — for every new component, not
just flagship pages.
