# HTTP Server

HTTP server in Python from scratch: TCP listen, parse request (request line, headers, body), build response, handlers (GET /, GET /files/..., POST /echo), handle multiple connections concurrently.

**Run**

```bash
uv run python main.py
```

Optional directory for serving files:

```bash
uv run python main.py --directory static
```

Then from another terminal:

```bash
curl http://127.0.0.1:9999/
```

**Scope TBA**

- Bind to port, respond with HTTP 200
- Parse request (request line, headers, body via Content-Length)
- Response with body and Content-Length header
- Routing: GET `/`, GET `/files/<path>`, POST `/echo`
- Concurrent connection handling (e.g. threads)
- Optional: Keep-Alive (multiple request/response on one connection)

Requires Python 3.14+ (see `.python-version`).
