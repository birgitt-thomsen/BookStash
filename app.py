""" This file contains flask app routes to handle GET and POST requests to
show the homepage, add an author, add and delete a book from the database. """
import os
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from data_models import db, Author, Book

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"sqlite:///{os.path.join(basedir,'data/library.sqlite')}"

db.init_app(app)

# One tine creation of tables from data_models classes
# with app.app_context():
#     db.create_all()

def get_authors():
    """ Get all authors from the database."""
    authors = db.session.scalars(
        db.select(Author).order_by(Author.name)
    ).all()
    return authors


def apply_sorting(query, sort):
    """ Apply sorting to query and return the query with sorted results."""
    if sort == "author":
        sort_order = query.order_by(Author.name)
    elif sort == "year":
        sort_order = query.order_by(Book.publication_year)
    else:
        sort_order = query.order_by(Book.title)
    return sort_order


def get_books(sort="title"):
    """ Get all books, linked to author, from the database."""
    query = (
        db.select(Book, Author)
        .join(Author, Book.author_id == Author.id)
    )

    return db.session.execute(
        apply_sorting(query, sort)
    ).all()


def search_books(keyword, sort="title"):
    """ Return a list of books matching the given keyword."""
    query = (
        db.select(Book, Author)
        .join(Author, Book.author_id == Author.id)
        .where(
            or_(
                Book.title.ilike(f"%{keyword}%"),
                Author.name.ilike(f"%{keyword}%")
            )
        )
    )

    return db.session.execute(
        apply_sorting(query, sort)
    ).all()

@app.route('/', methods=['GET'])
def index():
    """ Display the main page with sorting and search selections."""
    search = request.args.get("search")
    sort = request.args.get("sort", "title")

    if search:
        books = search_books(search, sort)
    else:
        books = get_books(sort)

    return render_template(
        "home.html",
        books=books,
        search=search,
        sort=sort
    )

@app.route('/add_author', methods=['GET','POST'])
def add_author():
    """ Add an author to the database. Return message when author already
    exists in database, date entry is invalid or an error occurred."""
    if request.method == 'POST':
        try:
            # Check if author already exists in database
            existing = db.session.scalar(
                db.select(Author).where(Author.name == request.form["name"])
            )

            if existing:
                return render_template(
                    "add_author.html",
                    message=f"{request.form["name"]} already exists in "
                            f"database."
                )

            death_date = request.form["date_of_death"]

            author = Author(
                name=request.form["name"],
                birth_date=datetime.strptime(
                    request.form["birthdate"], "%Y-%m-%d"
                ).date(),
                date_of_death=(
                    datetime.strptime(death_date, "%Y-%m-%d").date()
                    if death_date else None
                )
            )

            db.session.add(author)
            db.session.commit()

            message = f'{author.name} was added successfully!'

        except ValueError:
            message = "Please enter valid dates."

        except SQLAlchemyError:
            db.session.rollback()
            message = "An error occurred while saving the author."

        return render_template(
            "add_author.html",
            message=message
        )

    return render_template("add_author.html")

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Add a book to the database. Return message when ISBN already
    exists, publication year is invalid or an error occurred."""
    authors = get_authors()

    if request.method == 'POST':
        try:
            # Check if ISBN already exists
            existing_book = db.session.scalar(
                db.select(Book).where(Book.isbn == request.form["isbn"])
            )

            if existing_book:
                return render_template(
                    "add_book.html",
                    authors=authors,
                    message="A book with that ISBN already exists."
                )

            # Check if year is valid
            year = int(request.form["year"])

            if year < 0 or year > datetime.now().year:
                raise ValueError

            isbn = request.form["isbn"].strip() or None

            book = Book(
                author_id=int(request.form["author_id"]),
                title=request.form["title"].strip(),
                isbn=isbn,
                publication_year=int(request.form["year"])
            )

            db.session.add(book)
            db.session.commit()

            message = f"{book.title} was added successfully!"

        except ValueError:
            message = "Please enter a valid publication year."

        except SQLAlchemyError:
            db.session.rollback()
            message = "An error occurred while saving the book."

        return render_template(
            "add_book.html",
            authors=authors,
            message=message
        )

    return render_template(
        "add_book.html",
        authors=authors
    )

@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """ Delete a book from the database when user clicks button on homepage."""
    book = db.session.get(Book, book_id)

    if book is None:
        return "Book not found", 404

    title = book.title
    author_id = book.author_id

    # Delete the book
    db.session.delete(book)
    db.session.commit()

    # Check if the author has any books left
    remaining_books = db.session.scalar(
        db.select(db.func.count())
        .select_from(Book)
        .where(Book.author_id == author_id)
    )

    if remaining_books == 0:
        author = db.session.get(Author, author_id)
        db.session.delete(author)
        db.session.commit()

    return redirect(
        url_for("index", message=f'"{title}" was deleted successfully!'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
