# What's that?
It is a study project API where I practise (or at least try to practise) REST principles. Here I have models for text sentiment analysis and summarization. It is sort of a backend for a site that never existed :(

# How to deploy?
Install repository
```
git clone https://github.com/hate-red/verityai
cd verityai
```

Create `.env` file in the project directory and fill it like this
```
DB_HOST=localhost
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=my_super_passowrd
DB_PORT=5432
SECRET_KEY=gV64m9aIzFG4qpgVphvQbPQrtAO0nM-7YwwOvu0XPt5KJOjAy4AfgLkqJXYEt
ALGORITHM=HS256
```

In `docker-compose.yml` file change this fields: 
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB
- ports

accordingly to the values you filled in the `.env` file.

Set up docker container for databases
```
docker-compose up -d
```

For `pip`.

```
pip install -r requirements.txt
```

For `uv`

```
uv sync
```

```
source .venv/bin/activate
alembic revision --autogenerate -m "Initial revision"
alembic upgrade head
uv run app/run.py
```

Setup complete!