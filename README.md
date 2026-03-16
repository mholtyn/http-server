# HTTP Server

HTTP server in Python from scratch: TCP listen, parse HTTP/1.1 requests (request line, headers, body), build responses, simple routing and basic file serving, multiple concurrent persistent connections.

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

**Scope**

- **Networking**
  - Bind to TCP port `9999`, listen on `localhost`
  - Accept incoming connections and handle each connection in a separate thread
  - Support **persistent connections** for HTTP/1.1 (multiple request/response cycles on a single TCP connection)
  - Handle `Connection: close` on requests and mirror it in responses, then close the TCP connection

- **HTTP parsing**
  - Parse request line (`method path protocol`)
  - Parse headers into a case-insensitive dictionary (keys stored in lowercase)
  - Parse optional request body (simple approach: decode as UTF‑8, handle small payloads with `Content-Length`)

- **Routing & behaviour**
  - `GET /` → simple text `"Hello, world"`
  - `GET /echo/<text>` → echo the `<text>` segment in the body with correct `Content-Length`
  - `GET /user-agent` → return the value of the `User-Agent` header
  - `GET /files/<filename>` → return file contents from the directory passed via `--directory`
    - guard against escaping the base directory (`..`, extra `/`)
    - handle errors with appropriate status codes: `404 Not Found`, `403 Forbidden`, `500 Internal Server Error`
  - `POST /files/<filename>` → write the request body to a file under `--directory`, return `201 Created`

- **Responses**
  - Manually built HTTP/1.1 responses (status line + headers + empty line + body)
  - `Content-Length` for responses with a body (echo, user-agent, files)
  - For files, responses are sent as `bytes` with `Content-Type: application/octet-stream`

Requires Python 3.14+ (see `.python-version`).
