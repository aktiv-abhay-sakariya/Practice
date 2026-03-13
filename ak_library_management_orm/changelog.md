# Changelog
All notable changes to this project will be documented in this file.

[19.0.1.0.0] :
- Initial release of the Library Management orm module.
- Overwrite ORM method and perform validation of user input.

[19.0.1.0.1] :
- Updated all copy methods.
- Updated the UserError string and logic.
- Removed unnecessary code and comment lines.

[19.0.1.1.0] :
- Added two sequence 1)library.book, 2)author.author.
- Updated author form view: set new field in left-top with h1 teg.
- Updated book form view: make isbn field to readonly.

[19.0.1.1.2] :
- Updated code the sequence in vals before calling super method.

[19.0.1.1.3] :
- Updated field Add copy=false in isbn and author_ref felds.

[19.0.1.2.0] :
- inherit product.template and product.category model and their form view.
- Added header button in library.book model that create record in
product.template model.
- Added some smart button in library.book, book.category, product.category and
product.template model and set visibility of that button.
