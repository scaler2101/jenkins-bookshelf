import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# --- Health & Root ---

def test_root_returns_service_info(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["service"] == "Bookshelf API"
    assert data["status"] == "running"

def test_health_check_returns_healthy(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


# --- GET /books ---

def test_get_all_books_returns_list(client):
    response = client.get("/books")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 3

def test_get_available_books_filter(client):
    response = client.get("/books?available=true")
    assert response.status_code == 200
    books = response.get_json()
    for book in books:
        assert book["available"] is True


# --- GET /books/<id> ---

def test_get_existing_book_by_id(client):
    response = client.get("/books/1")
    assert response.status_code == 200
    book = response.get_json()
    assert book["id"] == 1
    assert "title" in book
    assert "author" in book

def test_get_nonexistent_book_returns_404(client):
    response = client.get("/books/9999")
    assert response.status_code == 404
    assert "error" in response.get_json()


# --- POST /books ---

def test_add_valid_book(client):
    payload = {"title": "DevOps Handbook", "author": "Gene Kim"}
    response = client.post("/books", json=payload)
    assert response.status_code == 201
    book = response.get_json()
    assert book["title"] == "DevOps Handbook"
    assert book["available"] is True

def test_add_book_missing_title_returns_400(client):
    response = client.post("/books", json={"author": "Someone"})
    assert response.status_code == 400

def test_add_book_missing_author_returns_400(client):
    response = client.post("/books", json={"title": "No Author Book"})
    assert response.status_code == 400

def test_add_book_empty_body_returns_400(client):
    response = client.post("/books", json={})
    assert response.status_code == 400
