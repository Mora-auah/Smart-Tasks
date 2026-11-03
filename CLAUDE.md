# Smart Tasks: project rules

Spec: docs/spec.docx. Prototype: docs/prototype/task-ai-prototype.html (UI reference only; its logic is mocked).

## Non-negotiables
- The model never mutates data. It reads via `search_tasks` and proposes via structured output; the user approves; the client calls the normal REST API.
- All text going to OpenAI passes through `backend/app/services/masking.py` (mask outbound, unmask inbound). No bypass path. Build/keep this before any OpenAI call.
- `store: false` on every Responses API call; do not use `previous_response_id`. History is re-sent from `chat_messages`.
- Server binds 127.0.0.1 only. `OPENAI_API_KEY` only in `.env` (git-ignored), never in client code. Technical logs contain masked text only.
- `ai_actions` rows are an audit log: never delete or edit, only the proposed -> approved/rejected/failed transition.
- UI is Hebrew RTL, desktop-only (min width 1280px). The chat panel stays outside the router.
- Use placeholder text (foo/bar/baz, Lorem ipsum) in examples, tests and fixtures.

## Commands
- `make install`, `make test`, `make lint`, `make dev-backend`, `make dev-frontend`, `make run`.
