## Caching

- Every cache write needs a known invalidation path: know which write/update
  operation should clear it, and clear it there — don't rely on TTL alone for
  data that changes on a predictable event.
- Scope cache keys precisely to what they represent. When caching per-item
  results in a loop/batch, write each result under its own key as it's computed
  — never reuse a key or loop variable left over from a previous iteration; it
  silently overwrites or misattributes an earlier entry.
