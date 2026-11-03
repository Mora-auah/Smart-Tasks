.PHONY: install dev-backend dev-frontend build run test lint

install:
	cd backend && python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
	cd frontend && npm install

dev-backend:
	cd backend && .venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

dev-frontend:
	cd frontend && npm run dev

build:
	cd frontend && npm run build

# Single-command local run: serves the built client from the API server
run: build
	cd backend && .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000

test:
	cd backend && .venv/bin/pytest -q

lint:
	cd backend && .venv/bin/ruff check .
	cd frontend && npm run typecheck
