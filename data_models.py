""" This module contains the database models for the authors and books
tables. """
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey

db = SQLAlchemy()

class Author(db.Model):
    """ This class models the authors table. """
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_date = Column(Date)
    date_of_death = Column(Date)

    def __str__(self):
        died = self.date_of_death or ""
        return f"{self.name} ({self.birth_date}–{died})"

    def __repr__(self):
        return (f"Author(id={self.id}, "
                f"name={self.name}, "
                f"birth_date={self.birth_date}, "
                f"date_of_death={self.date_of_death}) ")


class Book(db.Model):
    """ This class models the books table. """
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    isbn = Column(String)
    title = Column(String)
    publication_year = Column(Integer)

    def __str__(self):
        return f"{self.title} ({self.publication_year}) - ISBN: {self.isbn}"

    def __repr__(self):
        return (f"Book(id={self.id}, "
                f"author_id={self.author_id}, "
                f"isbn={self.isbn}, "
                f"title={self.title}, "
                f"publication_year={self.publication_year}) ")
