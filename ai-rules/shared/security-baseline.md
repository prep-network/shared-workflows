## Security Baseline

- Validate and sanitize every input at the boundary (HTTP request, CLI arg, webhook
  payload, scraped/external data) before it reaches business logic.
- Never build a query by string-interpolating user input — use parameterized
  queries, prepared statements, or the ORM's query builder.
- Escape all output rendered back to a user (HTML, attributes, URLs) at the point of
  output, not the point of storage.
- Check authorization (capability/permission/policy) before any privileged or
  destructive operation — don't rely on the UI hiding an action as the only guard.
- Never commit secrets, tokens, or credentials; read them from environment/config,
  never hardcode them.
