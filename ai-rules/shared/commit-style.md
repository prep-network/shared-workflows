## Commit Style

Use Conventional Commits: `feat(scope):`, `fix(scope):`, `refactor(scope):`,
`perf(scope):`, `docs(scope):`, `chore(scope):`, `ci(scope):`.

- Explain WHY the change was needed, not just what changed.
- Include before/after numbers when the change has measurable performance impact.
- Reference the related Asana task or issue when one exists.
- Call out breaking changes explicitly.

Example:
```
fix(rankings): guard against null school on player ranking query

Prevents a fatal error when a player's school reference is stale.
Fixes a 500 seen on /rankings for ~30 players after the July school merge.
```
