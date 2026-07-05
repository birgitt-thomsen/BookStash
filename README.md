# BookStash 📚

BookStash is a simple Flask web application for managing a personal library. It allows users to keep track of books and authors, search the library, and display book cover images using the Open Library Covers API.

## Features

* Add new authors
* Add new books
* Search books by title or author
* Sort library by title, author or publication year
* Delete books
* Automatically remove authors with no remaining books
* Display book cover images using ISBNs

## Technologies

* Python
* Flask
* Flask-SQLAlchemy
* SQLite
* HTML
* CSS

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```bash
   cd BookStash
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python app.py
   ```

5. Open your browser and visit:

   ```
   http://127.0.0.1:5002
   ```

## Project Structure

```
BookStash/
├── app.py
├── data_models.py
├── static/
    ├── images
        └── no_cover.png
│   └── style.css
├── templates/
│   ├── home.html
│   ├── add_book.html
│   └── add_author.html
└── data/
    └── library.sqlite
```

## Future Improvements

* Edit existing books and authors
* Delete authors
* Dedicated book page with additional information from external APIs
* Suggest a book to read
* Book ratings