## Code Hygiene

- Prefer early returns over nested conditionals.
- Remove debug output (`var_dump`, `dd`, `console.log`, ad-hoc `error_log`/`Log::debug`
  calls) before committing.
- A behavior change ships with a test and with the docs that explain it: update
  the existing doc, or add one when nothing covers the change.
- Don't add verification or scratch scripts unless explicitly requested — they
  are not docs and they don't run in CI.
- Don't add a docblock that only repeats typed params and returns, and don't
  narrate code line by line. Comment what the signature can't say: array shapes,
  thrown exceptions, and non-obvious constraints.
- Don't add or upgrade a dependency without approval; removing one doesn't need it.
- Match existing conventions in sibling files (naming, structure, patterns) before
  introducing a new one.
