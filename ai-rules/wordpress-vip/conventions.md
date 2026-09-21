## WordPress VIP Go — Conventions

Multisite WordPress VIP Go platform. Sage 10 theme (Blade + Tailwind + Alpine.js)
plus a core plugin architecture (`plugins/prepnetwork-functionality/` and friends).

### File & class naming
- Class files: `class-pn-[section]-[type].php`; static class pattern with an
  `init()` method that registers hooks.
- REST endpoint classes live under `includes/rest-api/`, coordinated by
  `PN_Rest_Api::init()`, under the `pn/v1` namespace — never register custom
  routes under `wp/v2`.

### Frontend
- Alpine.js for interactivity, not jQuery.
- Tailwind utility classes only — no custom CSS frameworks, no inline styles.
- Extract a Blade component only once a pattern repeats 3+ times.

### Multisite
- Always consider blog/site context; use `get_current_blog_id()` in cache keys and
  multisite-aware functions instead of hardcoded site IDs.

### Documentation
- Consult the relevant `docs/*.md` file before implementing (querying, caching,
  integrations, users, markets, schools, CLI, etc.) — don't reinvent an existing
  pattern or helper.
- Update the relevant `docs/*.md` file in the **same PR** as the code change; add
  new doc files to `docs/index.md`.

### VIP Go platform constraints
- No filesystem writes in production paths.
- No raw `curl`/`file_get_contents` for outbound HTTP — use VIP-approved HTTP
  clients (`vip_safe_wp_remote_get`, etc.).
- Custom cron uses Action Scheduler, not raw `wp_schedule_event`, for anything
  performance-sensitive.
- Database schema changes need VIP coordination.
