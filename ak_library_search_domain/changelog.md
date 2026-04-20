# Changelog
All notable changes to this project will be documented in this file.

[19.0.1.0.0] :
- Initial release of the library management search domain module.
- Added new menu and window action of that menu.
- Override the name_search method of author.author model and search by name 
and reference numbers.
- Added new filter in library.book model.

[19.0.1.1.0] :
- Updated active author action add view_ids of main author views.

[19.0.1.1.1] :
- Updated and use search_count instead of search for count the total book
products.

[19.0.1.2.0] :
- Added two button Add book and edit line in sale.order form view.
- Added wizard for add book product and edit them in current sale.order record.

[19.0.1.2.1] :
- Updated and marged a add and edit button method for call wizard.
- Added _description in wizard models.

[19.0.1.3.0] :
- Added new 'book.reservation' model with list and form views.
- Override name_search method in 'library.book' and _compute_display_name
method in 'res.partner'.
- Added smart button in 'res.partner' model form view

[19.0.1.4.0] :
- inherited 'mail.thread' and 'mail.activity.mixin' in library.book model.
- Added py constraint in library.book for prevent duplcate record.
- Added new user_id M2O field with res.users model also add in form view in 
author.author model.
- Override create method in library.book model for add log note and create 
activity and notification.

[19.0.1.5.0] :
- Added New three groups 1.library staff, 2.librarian and 3.library manager.
- Added access rights and record rule of that groups.
- inherited book.edition menu for the set their visibility.
- Added odoo magic field in book.reservation form view and only see by manager.

[19.0.1.6.0] :
- Added server action in book.reservation model for cancel the overdue reservation.
- Added automation rule for add log note when book reservation state change to reserved only.
- Added two schedule action or cron job:
    1. for book.reservstion model for run on a daily basis to monitor the status of book reservation records.
    2. for author.author model for run on a daily basis to monitor the status of author records.
- Added one more depends 'base_automation' for create automation rule.

[19.0.1.7.0] : 
- Added new email template for library.book model.
- Added new button for sent a email to author in library.book model form view and it visible when author are selected.

[19.0.1.7.1] : 
- Updated email_from as per the Odoo base configuration.
- Update the button color should be primary, and after the email is sent for the first time, change the Send Mail button color to secondary.
- Added lang field in the email template.
- Added raise_if_not_found for check the email template exist or not.
- Added author name in log note after the mail was sent.

[19.0.1.8.0] : 
- Added new email template for book.reservation model.
- Added new button for sent a email to customer it can see only when book 
reservation state is 'reserved'. click it then open the mail composer with 
created email template.

[19.0.1.9.0] : 
- Added new report layout for author.author model.
- Added new report action for author.author model to print PDF document of the author records and call the created new layout.