# Personal Blog API

A full-stack blog application with REST API backend (FastAPI + PostgreSQL) and vanilla JavaScript frontend.

## Features

- ✅ Create, Read, Update, Delete articles
- ✅ Filter by author and tags
- ✅ Pagination support
- ✅ RESTful API design
- ✅ Auto-generated API documentation (Swagger)

## Tech Stack

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Pydantic (Validation)

**Frontend:**
- HTML5
- CSS3
- Vanilla JavaScript

---

## Prerequisites

- Python 3.8+
- Docker (for PostgreSQL)
- Git

---

## Quick Setup

### 1. Clone Repository
```bash
git clone https://github.com/yahyoHakimov/blog-post
cd blog-api
```

### 2. Setup Database (Docker)
```bash
# Start PostgreSQL container
docker run --name blog-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=blog_db \
  -p 5432:5432 \
  -d postgres

# Verify container is running
docker ps
```

### 3. Setup Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
pip freeze > requirements.txt
```

### 4. Configure Environment

Create `.env` file in project root:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/blog_db
```

### 5. Run Application
```bash
uvicorn app.main:app --reload
```

### 6. Access Application

- **Frontend:** http://127.0.0.1:8000
- **API Docs (Swagger):** http://127.0.0.1:8000/docs
- **API Docs (ReDoc):** http://127.0.0.1:8000/redoc

---

## Docker Setup (Alternative - Full Containerization)

### Option 1: Docker Compose (Recommended)

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: blog-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: blog_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: .
    container_name: blog-api
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/blog_db
    depends_on:
      - db
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  postgres_data:
```

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `.dockerignore`:
```
venv/
__pycache__/
*.pyc
.env
.git/
```

**Run with Docker Compose:**
```bash
# Build and start containers
docker-compose up --build

# Run in background
docker-compose up -d

# Stop containers
docker-compose down

# Stop and remove volumes (deletes data)
docker-compose down -v
```

### Option 2: Docker Only (Database)
```bash
# Start PostgreSQL
docker run --name blog-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=blog_db \
  -p 5432:5432 \
  -d postgres

# Stop container
docker stop blog-postgres

# Start existing container
docker start blog-postgres

# Remove container
docker rm blog-postgres

# View logs
docker logs blog-postgres
```

---

## Project Structure
```
blog-api/
├── app/
│   ├── __init__.py          # Package marker
│   ├── main.py              # FastAPI app & routes
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # Database connection
│   └── crud.py              # CRUD operations
├── frontend/
│   └── index.html           # Frontend UI
├── .env                     # Environment variables
├── .gitignore
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image config
├── docker-compose.yml       # Multi-container setup
└── README.md
```

---

## Database Management

### Access PostgreSQL
```bash
# Using Docker
docker exec -it blog-postgres psql -U postgres -d blog_db

# SQL Commands
SELECT * FROM articles;
\dt              # List tables
\d articles      # Describe table
\q               # Quit
```

### Reset Database
```bash
# Stop and remove container with data
docker stop blog-postgres
docker rm blog-postgres

# Start fresh container
docker run --name blog-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=blog_db \
  -p 5432:5432 \
  -d postgres
```

---

## Development

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Update Dependencies
```bash
pip freeze > requirements.txt
```

---

## Troubleshooting

### Port Already in Use
```bash
# Windows - Find process on port 5432
netstat -ano | findstr :5432
taskkill /PID <process_id> /F

# Linux/Mac
lsof -ti:5432 | xargs kill -9
```

### Database Connection Error

1. Check PostgreSQL is running:
```bash
docker ps
```

2. Check `.env` file exists with correct DATABASE_URL

3. Restart containers:
```bash
docker-compose restart
```

---

## Deployment

### Environment Variables

For production, update `.env`:
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
ENVIRONMENT=production
```
