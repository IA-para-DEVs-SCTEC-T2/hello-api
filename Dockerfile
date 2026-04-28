# ─── Base Image ───────────────────────────────────────────────────────────────
FROM python:3.13-slim

# ─── Environment ──────────────────────────────────────────────────────────────
WORKDIR /app

# ─── Dependencies ─────────────────────────────────────────────────────────────
RUN pip install uv

COPY pyproject.toml uv.lock* ./

RUN uv pip install --system \
    fastapi \
    "uvicorn[standard]" \
    "python-jose[cryptography]" \
    "passlib[bcrypt]" \
    python-dotenv

# ─── Application ──────────────────────────────────────────────────────────────
COPY main.py .
COPY .env.example .env

# ─── Runtime ──────────────────────────────────────────────────────────────────
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
