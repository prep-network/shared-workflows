## Code Hygiene

- Prefer early returns over nested conditionals.
- Remove debug output (`var_dump`, `dd`, `console.log`, ad-hoc `error_log`/`Log::debug`
  calls) before committing.
- Don't create documentation files, README files, or verification/scratch scripts
  unless explicitly requested — prove correctness with tests instead.
- Don't add or upgrade a dependency without approval; removing one doesn't need it.
- Match existing conventions in sibling files (naming, structure, patterns) before
  introducing a new one.
