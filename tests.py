import pytest
from fastapi.testclient import TestClient
from main import app
from db import SessionLocal, Base, engine
import models

# Создаем тестового клиента
client = TestClient(app)


# Настройка тестовой базы данных
def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Fixture для создания и очистки тестовой базы данных
@pytest.fixture(scope="module")
def test_db():
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)

    # Выполняем тесты
    yield

    # Удаляем все таблицы после тестов
    Base.metadata.drop_all(bind=engine)


# Тест создания автора
def test_create_author(test_db):
    author_data = {
        "first_name": "Лев",
        "last_name": "Толстой",
        "birth_date": "1828-09-09"
    }

    response = client.post("/authors", json=author_data)

    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Лев"
    assert data["last_name"] == "Толстой"
    assert "id" in data


# Тест получения списка авторов
def test_get_authors(test_db):
    # Предварительно создаем парочку авторов
    authors_data = [
        {"first_name": "Федор", "last_name": "Достоевский", "birth_date": "1821-11-11"},
        {"first_name": "Антон", "last_name": "Чехов", "birth_date": "1860-01-29"}
    ]

    for author in authors_data:
        client.post("/authors", json=author)

    response = client.get("/authors")

    assert response.status_code == 200
    authors = response.json()
    assert len(authors) >= 2


# Тест создания книги
def test_create_book(test_db):
    # Сначала создадим автора
    author_response = client.post("/authors", json={
        "first_name": "Александр",
        "last_name": "Пушкин",
        "birth_date": "1799-06-06"
    })
    author_id = author_response.json()["id"]

    book_data = {
        "title": "Капитанская дочка",
        "description": "Историческая повесть",
        "available_copies": 5,
        "author_id": author_id
    }

    response = client.post("/books", json=book_data)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Капитанская дочка"
    assert data["available_copies"] == 5


# Тест создания выдачи книги
def test_create_borrow(test_db):
    # Создаем автора
    author_response = client.post("/authors", json={
        "first_name": "Михаил",
        "last_name": "Булгаков",
        "birth_date": "1891-05-15"
    })
    author_id = author_response.json()["id"]

    # Создаем книгу
    book_response = client.post("/books", json={
        "title": "Мастер и Маргарита",
        "description": "Роман",
        "available_copies": 3,
        "author_id": author_id
    })
    book_id = book_response.json()["id"]

    # Создаем выдачу
    borrow_data = {
        "book_id": book_id,
        "reader_name": "Иван Иванов"
    }

    response = client.post("/borrows", json=borrow_data)

    assert response.status_code == 200
    data = response.json()
    assert data["reader_name"] == "Иван Иванов"
    assert data["book_id"] == book_id


# Тест возврата книги
def test_return_book(test_db):
    # Создаем автора
    author_response = client.post("/authors", json={
        "first_name": "Николай",
        "last_name": "Гоголь",
        "birth_date": "1809-04-01"
    })
    author_id = author_response.json()["id"]

    # Создаем книгу
    book_response = client.post("/books", json={
        "title": "Мертвые души",
        "description": "Поэма",
        "available_copies": 2,
        "author_id": author_id
    })
    book_id = book_response.json()["id"]

    # Создаем выдачу
    borrow_response = client.post("/borrows", json={
        "book_id": book_id,
        "reader_name": "Петр Петров"
    })
    borrow_id = borrow_response.json()["id"]

    # Возвращаем книгу
    return_response = client.patch(f"/borrows/{borrow_id}/return")

    assert return_response.status_code == 200
    data = return_response.json()
    assert data["return_date"] is not None