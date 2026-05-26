# 📚 Bookshelf API

A simple REST API for managing a book collection, built with **Python Flask**.

## Endpoints

| Method | Path              | Description                        |
|--------|-------------------|------------------------------------|
| GET    | `/`               | Service info                       |
| GET    | `/health`         | Health check                       |
| GET    | `/books`          | List all books                     |
| GET    | `/books?available=true` | List only available books   |
| GET    | `/books/<id>`     | Get a specific book                |
| POST   | `/books`          | Add a new book                     |

## Running Locally

```bash
pip install -r requirements.txt
python app/app.py
```

The API will be available at `http://localhost:5000`.

## Running Tests

```bash
pytest tests/ -v --cov=app
```

---
*This app is used as the sample project for the Jenkins CI/CD practice lab.*
