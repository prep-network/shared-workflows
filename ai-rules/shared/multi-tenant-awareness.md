## Multi-Site / Multi-Tenant Awareness

Both platforms serve multiple sites/brands from shared infrastructure — never
assume a single-tenant default:

- Cache keys must include the site/tenant identifier whenever the cached value
  could differ per site.
- When one lookup can match multiple sites (e.g. several brands sharing a
  domain, or a multisite network), resolve and expose the *collection* of
  matches, not just the first — code that assumes "first match" silently drops
  sibling tenants from anything cross-tenant (filtering, ranking, notifications).
- Never hardcode a site/tenant ID; always resolve it from context.
