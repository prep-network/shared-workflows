## WordPress VIP Go — Caching & Security

### Caching (PN_Cache only)
All expensive operations must use `PN_Cache::get()`/`PN_Cache::set()` — never raw
transients or `wp_cache_*` directly. Cache keys must be multisite-aware and
versioned for busting:

```php
$cache_key = sprintf(
    'pn_%s_%s_%s_v%s',
    $feature,                    // feature identifier
    $context,                    // site_id, market, etc.
    md5( serialize( $args ) ),   // hashed parameters
    self::CACHE_VERSION          // bump to invalidate
);
```

Invalidate explicitly on the CRUD operations that change the cached data — don't
rely on TTL alone for data that changes on a known event.

### Database
- Prefer custom tables over postmeta for anything queried at scale.
- Use `PN_Query` / `PN_Player_Ranking_Query_Builder` over ad-hoc `WP_Query` +
  postmeta loops (N+1 risk).
- `$wpdb->prepare()` for every query — no raw interpolation.

### Input/output
- Sanitize all input: `sanitize_text_field()`, `absint()`, `wp_kses_post()`,
  `sanitize_email()`.
- Escape all output: `esc_html()`, `esc_attr()`, `esc_url()`.
- `current_user_can()` before privileged operations; `wp_verify_nonce()` on form
  submissions.
- Use `$request->get_param()` in REST callbacks, not `$_GET`/`$_POST`.

### Entity label
The athlete entity's display name varies by brand ("Player", "Athlete", …). Never
hardcode the noun in user-facing copy (AJAX/REST responses, CLI output, emails,
admin notices) — use `(new PN_Website())->entityLabel(plural: ..., lowercase: ...)`.
Code-level identifiers (class names, meta keys, REST field names, post type slugs,
hook names) stay as `player` regardless of brand.
