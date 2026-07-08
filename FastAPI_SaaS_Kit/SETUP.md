# FastAPI SaaS Kit — Quick Start

Get running in 5 minutes.

## Prerequisites

- Python 3.12+
- Docker & Docker Compose (for Postgres + Redis)
- Stripe account (test mode)

## Setup

```bash
# 1. Clone and enter
cd fastapi-saas-kit

# 2. Copy env and fill in your keys
cp .env.example .env
# Edit .env: set SECRET_KEY, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET

# 3. Start services (Postgres + Redis + App)
make dev

# 4. Run migrations (in another terminal)
make migrate

# 5. Open API docs
open http://localhost:8000/docs
```

## Development without Docker

```bash
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## Testing

```bash
make test
```

## Project Structure

```
app/
├── api/          # Route handlers (auth, users, billing, health)
├── middleware/   # CORS, rate limiting
├── models/       # SQLAlchemy models
├── schemas/      # Pydantic schemas
├── services/     # Business logic (auth, stripe, email)
├── config.py     # Settings from env
├── database.py   # Async SQLAlchemy engine
└── main.py       # FastAPI entrypoint
```

## Key Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/v1/auth/register | Create account |
| POST | /api/v1/auth/login | Get JWT tokens |
| POST | /api/v1/auth/refresh | Refresh access token |
| POST | /api/v1/auth/password-reset | Request reset email |
| GET | /api/v1/users/me | Current user profile |
| PATCH | /api/v1/users/me | Update profile |
| DELETE | /api/v1/users/me | Soft delete account |
| POST | /api/v1/billing/checkout | Stripe checkout session |
| POST | /api/v1/billing/portal | Stripe customer portal |
| POST | /api/v1/billing/webhook | Stripe webhook handler |
| GET | /health | Health check |

## Stripe Setup

1. Create a product + price in Stripe Dashboard (test mode)
2. Set `STRIPE_PRICE_ID_MONTHLY` in `.env`
3. For webhooks locally: `stripe listen --forward-to localhost:8000/api/v1/billing/webhook`
4. Copy the webhook signing secret to `STRIPE_WEBHOOK_SECRET`
