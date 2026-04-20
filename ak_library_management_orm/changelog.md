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
- Updated author form view: set new field in left-top with h1 tag.
- Updated book form view: make isbn field to read-only.

[19.0.1.1.2] :
- Updated code the sequence in vals before calling super method.

[19.0.1.1.3] :
- Updated field Add copy=false in isbn and author_ref fields.

[19.0.1.2.0] :
- Inherit product.template and product.category model and their form view.
- Added header button in library.book model that create record in
product.template model.
- Added some smart button in library.book, book.category, product.category and
product.template model and set visibility of that button.

[19.0.1.3.0] :
- Removed unnecessary import and print statement.
- Added total count in all the smart buttons.

[19.0.1.4.0] :
- Rearranged method by following standards.
- Updated when book product have multiple variant then smart button on the book
are redirect to the product.product table list view otherwise redirect
product.template form view.

[19.0.1.5.0] :
- Inherit add new field in res.user model.
- Inherit sale.order view and add button and set visibility.
- Added wizard and open it. when confirm button click in sale.order model.

[19.0.1.6.0] :
- Deleted wizard and add new approve_state field.
- Update if user is manager then only confirm and cancel the SO.

[19.0.1.6.1] :
- Created new method for approve button.
- Updated the action_confirm logic.