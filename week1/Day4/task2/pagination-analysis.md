# Pagination analysis — https://api.github.com/users/octocat/repos?page=1&per_page=5

Summary
- Endpoint uses offset-style pagination with `page` and `per_page` query parameters.
- `page` (integer) selects which page; `per_page` (integer) sets items per page (GitHub max usually 100).
- The canonical way to discover next/prev pages is the HTTP `Link` header returned by the API — do not rely solely on incrementing `page`.

Typical Link header
- Example:
  Link: <https://api.github.com/users/octocat/repos?page=2&per_page=5>; rel="next", <https://api.github.com/users/octocat/repos?page=20&per_page=5>; rel="last"
- rel values commonly present: `next`, `prev`, `first`, `last`.
- Use the `rel="next"` URL to fetch the next page reliably.

How to detect and follow pages
- Inspect response headers (not just body). With curl:
  - curl -i 'https://api.github.com/users/octocat/repos?page=1&per_page=5'
- Parse the `Link` header and follow the URL with rel="next".
- If `Link` is absent, the response is a single-page result (or last page).

Determining total items
- REST responses typically do not include a total-count header for this endpoint.
- Infer total pages from the `last` link's `page` parameter when present.

Edge cases and correctness
- Data can change between requests: additions/deletions may cause overlap or missing items if you paginate by numeric pages. For strictly-consistent pagination across changing data sets consider cursor-based APIs (GraphQL) or timestamps.
- If you must use page numbers, prefer stable ordering via supported query params (e.g., `sort` and `direction`) to reduce item churn.

Performance & limits
- Keep `per_page` reasonable (up to 100) to reduce number of requests while avoiding very large responses.
- Observe GitHub rate limits (check `X-RateLimit-*` headers). Use conditional requests (ETag / If-None-Match) to save quota when content hasn't changed.

Best practices
- Always follow `Link` header rel URLs instead of assuming page math.
- Use full, absolute URLs returned in `Link`.
- Respect rate-limit headers; back off and retry after `X-RateLimit-Reset` if needed.
- Prefer GraphQL cursor pagination for large result sets or for transactional consistency.
- Log request URLs and Link headers during debugging to verify correct navigation.

Example minimal follow-next pseudo-steps (shell)
- Request page 1, read `Link` header → extract rel="next" URL → request that URL → repeat until no `next`.

Notes specific to the provided URL
- `page=1&per_page=5` will return the first 5 repositories for user `octocat`. Check response headers for `Link` to see whether more pages exist and which page number is last.
- If logs or automation relying on this endpoint are failing, ensure you parse headers, handle 403/429 rate-limit responses, and include authentication if higher rate limits are