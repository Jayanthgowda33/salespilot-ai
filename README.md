# SalesPilot AI — Project Guide

This is a starter version of the product you described: a multi-tenant
sales platform where an AI scores leads, summarizes meetings, and tells
sales reps who to talk to next. It is not a toy — the auth, multi-tenancy,
and database structure are built the way a real SaaS is built. The AI
features work end to end (they call the Claude API for real). What's
NOT built yet, on purpose, is explained at the bottom, so you know what
to build next.

## 1. How the project is organized

```
salespilot-ai/
├── backend/                 FastAPI + PostgreSQL
│   ├── app/
│   │   ├── main.py          starts the API, wires all routes together
│   │   ├── config.py        reads settings from .env
│   │   ├── database.py      database connection setup
│   │   ├── models/          one file per database table
│   │   ├── schemas/         request/response shapes (Pydantic)
│   │   ├── api/routes/      the actual endpoints (auth, leads, ai, dashboard)
│   │   ├── core/security.py password hashing + JWT tokens
│   │   ├── services/ai_service.py   ALL the AI logic lives here
│   │   ├── celery_app.py    background job setup
│   │   └── tasks.py         example background job (bulk re-scoring)
│   ├── alembic/              database migrations
│   ├── requirements.txt
│   └── .env.example          copy this to .env and fill in real values
│
├── frontend/                 React + TypeScript + Tailwind
│   └── src/
│       ├── main.tsx           app entry point
│       ├── App.tsx            page routing
│       ├── pages/              Login, Signup, Dashboard, Leads
│       ├── components/         Navbar, shared UI pieces
│       ├── context/AuthContext.tsx   handles login state everywhere
│       └── api/client.ts        talks to the backend
│
└── docker-compose.yml         runs Postgres + Redis + backend + worker together
```

The idea: **backend/** is a completely separate project from **frontend/**.
They only talk to each other over HTTP (the frontend calls
`http://localhost:8000/api/...`). This is exactly how real companies
split the work between backend and frontend engineers.

## 2. What you need installed before you start

- Python 3.11+ (check with `python3 --version`)
- Node.js 18+ (check with `node --version`)
- PostgreSQL (or just use Docker for this — see step 5)
- Git (optional but recommended)
- VS Code, with these extensions: Python, Pylance, ES7+ React snippets, Tailwind CSS IntelliSense

## 3. Running the backend (do this first)

Open a terminal in VS Code (Terminal → New Terminal), then:

```bash
cd salespilot-ai/backend

# create a virtual environment so packages don't pollute your system Python
python3 -m venv venv

# activate it
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# install everything the backend needs
pip install -r requirements.txt

# create your real config file
cp .env.example .env
```

Now open `.env` in VS Code and fill in:
- `DATABASE_URL` — if you're running Postgres locally, something like
  `postgresql://youruser:yourpassword@localhost:5432/salespilot`
- `SECRET_KEY` — any long random string, e.g. run `python3 -c "import secrets; print(secrets.token_hex(32))"`
  and paste the result
- `ANTHROPIC_API_KEY` — get this from https://console.anthropic.com (needed for the AI features to actually work; the rest of the app runs fine without it)

If you don't have Postgres installed locally, skip to step 5 (Docker) —
it's genuinely the easier path.

Then start the server:

```bash
uvicorn app.main:app --reload
```

Visit **http://localhost:8000/docs** — this is FastAPI's auto-generated
API tester. You can try every endpoint (signup, login, create a lead,
score a lead) right there before the frontend even exists. This is the
single most useful page while you're building.

## 4. Running the frontend

Open a second terminal (keep the backend running in the first one):

```bash
cd salespilot-ai/frontend
npm install
npm run dev
```

Visit **http://localhost:5173**. You should see the login screen.
Click "Sign up", create an account, and you'll land on the dashboard.

## 5. Easier alternative: run everything with Docker

If installing Postgres and Redis locally feels like a hassle, do this
instead from the project root (`salespilot-ai/`):

```bash
cp backend/.env.example backend/.env
# edit backend/.env — at minimum set SECRET_KEY and ANTHROPIC_API_KEY

docker compose up --build
```

This starts Postgres, Redis, the FastAPI backend, and a Celery worker,
all networked together. The backend will be on http://localhost:8000
exactly like before. You'd still run the frontend separately with
`npm run dev` since it's not in docker-compose (keeps hot-reload fast).

## 6. Trying the AI features

1. Sign up, then go to the Leads page and add a lead.
2. Click "Run AI Score" next to it.
3. This calls `POST /api/ai/score-lead/{id}`, which sends the lead's
   details to Claude and asks for a score, a summary, a deal
   probability, and a next best action — then saves all four onto the
   lead. Refresh and you'll see them.
4. You can also log an activity (an email or call note) against a
   lead directly from `/docs`, then call
   `POST /api/ai/summarize-activity/{id}` to see sentiment analysis
   in action.

If you don't have an Anthropic API key yet, everything except the AI
endpoints will work normally — signup, login, adding leads, the
dashboard.

## 7. How multi-tenancy actually works here

Every table that holds customer data (`leads`, `activities`, `deals`)
has a `company_id` column. Every single database query in
`app/api/routes/*.py` filters by `current_user.company_id`. That's the
whole trick — it's not magic, it's just discipline. If you add a new
route later, copy this pattern every time or Company A will be able to
see Company B's leads, which would be a serious bug in a real product.

## 8. What's deliberately left as a next step

This is a solid, working foundation — but a few things are stubbed out
so you can build them yourself (or ask for help building them next):

- **Google OAuth** — the login flow is scaffolded in `auth.py` with a
  clear TODO. It needs a Google Cloud project, which only you can create.
- **RAG / pgvector** — right now the AI just reads the lead's recent
  activities directly. A real RAG setup would embed all activities into
  pgvector and pull only the most relevant ones for very active leads.
- **LangGraph** — the AI service currently makes single, direct calls
  to Claude. LangGraph would let you build a multi-step agent (e.g.
  "check the lead's history, decide if more info is needed, then score
  it") instead of one-shot prompts.
- **Password reset** — needs an email-sending service (like Resend or
  SES) to send the reset link, which needs its own account/API key.
- **Celery beat schedule** — the nightly "re-score every lead" job
  exists in `tasks.py` but isn't scheduled yet; you'd add
  `celery beat` config to run it automatically every night.
- **Alembic migrations** — right now tables are created automatically
  on startup (`Base.metadata.create_all`), which is fine for
  development. Before deploying for real, run
  `alembic revision --autogenerate -m "initial"` and
  `alembic upgrade head` instead, so schema changes are tracked properly.

## 9. Suggested order to build in

1. Get backend + frontend running locally (steps 3–4 above).
2. Sign up, add a few leads, log some activities, run AI scoring —
   get comfortable with what already works.
3. Add the Deal model UI (backend already supports it) so the revenue
   and pipeline dashboard numbers have real data.
4. Wire up Google OAuth.
5. Move from `create_all` to real Alembic migrations.
6. Add RAG with pgvector once you have enough activity data to make
   it worth it.
7. Deploy: backend + Postgres + Redis to something like Railway or
   Render, frontend to Vercel or Netlify.

Each of these is its own focused task — good luck, and come back any
time you want to build the next piece.
