from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database" of books
BOOKS = [
    {"id": 1, "title": "The Pragmatic Programmer", "author": "David Thomas", "available": True},
    {"id": 2, "title": "Clean Code",               "author": "Robert C. Martin", "available": True},
    {"id": 3, "title": "The Phoenix Project",       "author": "Gene Kim",         "available": False},
]

@app.route("/")
def index():
    return jsonify({
        "service": "Bookshelf API",
        "version": "1.0.0",
        "status": "running"
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/books", methods=["GET"])
def get_books():
    available_only = request.args.get("available", "false").lower() == "true"
    result = [b for b in BOOKS if b["available"]] if available_only else BOOKS
    return jsonify(result), 200

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book), 200

@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()
    if not data or "title" not in data or "author" not in data:
        return jsonify({"error": "title and author are required"}), 400
    new_book = {
        "id": max(b["id"] for b in BOOKS) + 1,
        "title": data["title"],
        "author": data["author"],
        "available": data.get("available", True),
    }
    BOOKS.append(new_book)
    return jsonify(new_book), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
