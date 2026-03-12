# Changelog
All notable changes to this project will be documented in this file.

[19.0.1.0.0] :
- Initial release of the Library Management module.
- Added two models: 1)library.book 2)book.category
- Added list, form and search views on book's window.
- Added list and form(default) view on category's window.

[19.0.1.1.0] :
- Added three models: 1)book.edition 2)author.book 3)author.author
- Added list, form (default) views on book edition's window.
- Added list and form view on author's window.
- Added relations :
    1. Many2one :  book.category-book.category, library.book-book.category,
                    author.book-library.book
    2. Many2many : library.book-book.edition
    3. One2many : author.author-author.book

[19.0.1.1.1] :
- Updated module follow standard Odoo version format.
- Renamed model class name.
- Added Header comments.
- Created separate XML view files and make some form views.
- Remove unnecessary fields (book_ids) in book.editions model.

[19.0.1.1.2] :
- Added widget in XML views files.
- Added search views for Author, Category and Edition models.
- Removed _res_name attribute because topic was covered in session.
- Renamed the XML view files using or following Odoo standards.

[19.0.1.1.3] :
- Added quantity, book_price fields in book.edition model.
- Added total_books, total_sales_amout fields in library.book model.
- Added Compute method in library.book model to calculate total no of books
and total sales amount base on selected edition(book.edition).
- Added Onchange method in author.book model to auto-populate isbn,
publication_date, price fetch from selected book(library.book).

[19.0.1.1.4] :
- Followed Coding Standards.
- Added editable="bottom" to allow inline record creation and editing
in the Odoo form view. in author_author_views file.
- Added _rec_name attribute in the book.category model.

[19.0.1.2.0] :
- Added readonly attribute in book_ids in author form view.
- Added author_id field in library.book model.
- Added compute method for automatically create or update record in author.book model.

[19.0.1.2.1] :
- Added attribute ondelete='cascade' in author_id in author.book model.

[19.0.1.2.2] :
- Used special command instead of ORM method.
- Added else condition when author remove from the book from view corresponding 
book line remove in the author.author model.

[19.0.1.3.0] :
- Updated Form views of all the models.