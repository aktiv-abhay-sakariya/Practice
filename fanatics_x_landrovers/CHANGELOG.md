# Fanatics - LandRovers Customization


# Changelog

### Version 18.0.47.0.0

#### **Business Requirement**
The customer had an existing customization that automatically generated **Internal Reference** and **Barcode** when products were created manually.  
However, this logic did not execute when products were imported via **CSV/XLS** files.

#### **Enhancement Implemented**
- Extended the existing logic to trigger during **product creation via import**.
- Ensured **Internal Reference** and **Barcode** are automatically generated for imported products.
- Maintained consistent behavior between manual and imported product creation.
- Added validation to prevent duplicate Internal References or Barcodes.
- Verified full compatibility with Odoo’s standard import process.

#### **Outcome**
- Automatic generation of Internal Reference and Barcode now works for both manual and imported records.
- Improved **data consistency** and reduced **manual intervention** during bulk imports.
- Enhanced **user experience** and **process reliability**.

### Version 18.0.47.0.1
- Add Project Filter on Shop Floor Search Bar

### Version 18.0.47.0.2
- Updated filter sequence to display Project and Work Center at the top in search results.

### Version 18.0.47.0.3
- Updated XPath to use the move position instead of replace.

### Version 18.0.47.0.4
- shopfloor search view project search was not working in production(staging it was working)
- make modification into the fanatics_x_landrovers/views/mrp_production_views.xml file

### Version 18.0.47.0.5
- previous fix did not worked on the production so added alternative fix
- make modification into the fanatics_x_landrovers/views/mrp_production_views.xml file

### Version 18.0.47.0.6
- previous fix did not worked on the production so added alternative fix
- make modification into the fanatics_x_landrovers/views/mrp_production_views.xml file

### Version 18.0.47.0.7
- fix bug, now when you change project name then analytic account and document folder name will also change

### Version 18.0.47.0.8
- fix bug, now when you change project name then it will be identical for all the activated languages

### Version 18.0.47.0.9
- added surname nickname changes as per user story 16

### Version 18.0.47.1.9
- added changes related to US#20

### Version 18.0.47.1.10
- added changes related to US#20, point no 2.4

### Version 18.0.47.2.10
- US#20
- version : 1.2

### Version 18.0.47.3.10
- US#21 : implemented feature of user story

### Version 18.0.47.4.10
- US#21 :
- added smart button on the project to view Won Opportunity
- other fixes in code after QA's comment

### Version 18.0.47.4.11
- US#16 CR
- when update nickname into the contact then also update the same into the project also
- added chananges related to US#20

### Version 18.0.47.5.11
- US#21 :
- For the donor vehicle, change the icon in the project dashboard and in the project form view.
Won Opportunity: rename it to customer and add a user icon to it, in both the project dashboard and the project form view.
Check why the contact is not passing to the lead form when we create a project from the won opportunity.
There are 2 customer IDs on the project, so also pass it in both and write logic such that when one is changed, it also reflects in the other.

### Version 18.0.47.5.12
- US#21 :
- fix sequence issue for the built slot number

### Version 18.0.47.5.13
- fix access issue on the donor smart button on the project dashboard