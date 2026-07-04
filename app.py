""" This file contains flask app routes to handle GET and POST requests. """
import os
from datetime import datetime
from flask import Flask, request, render_template
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)

# One tine creation of tables from data_models classes
# with app.app_context():
#     db.create_all()

@app.route('/add_author', methods=['GET','POST'])
def add_author():
    """ Add an author to the database."""
    if request.method == 'POST':
        try:
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

            message = f'{author.name} added successfully!'

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
