## Pull Requests

- Every PR description includes an Asana task link (or an explicit note that none
  applies) and a "What changed" summary.
- Keep PRs scoped to one change; split unrelated fixes into separate PRs.

### AI code review scope

When an AI reviews a PR (e.g. Copilot, Claude), it should:

**Flag:**
- Logic errors and incorrect behavior
- Security issues (injection, auth/authorization gaps, unsafe input handling, secrets in code)
- Data loss or data-corruption risks (destructive migrations, unguarded mass updates/deletes)
- Performance problems with real impact (N+1 queries, unbounded loops over large datasets, missing indexes)
- Broken or missing error handling on operations that can fail (external API calls, DB writes, queue jobs)

**Never flag:**
- Code style/formatting — the linter (Pint / PHPCS) owns this, not review comments
- Naming preferences, casing, or alphabetical ordering
- Missing or stylistic PHPDoc / comments
- Subjective "consider refactoring" suggestions with no functional impact
- Test coverage suggestions unless a change clearly breaks an existing test

**Severity bar:** only comment if a competent senior engineer would consider it
worth blocking or fixing before merge. When in doubt, stay silent — a human
reviewer owns final approval. Don't re-raise concerns about unmodified code, and
don't repeat a concern already addressed elsewhere in the diff.
