## Testing

- Every behavior change ships with a new or updated test proving it — programmatic
  tests, not manual verification scripts or tinker sessions, when the framework's
  test tools can cover the same ground.
- Run the narrowest set of tests that covers the change (a filtered/targeted run),
  re-running after each fix; ask before running — or ask the user to run — the full
  suite once the targeted tests pass.
- Flaky tests are bugs, not noise: never hardcode a wait/timeout to paper over
  non-determinism. Wait on the actual condition (network, DOM state, DB write) and
  fix the root cause before moving on.
- Never delete or weaken an existing test to make a change pass without approval.
