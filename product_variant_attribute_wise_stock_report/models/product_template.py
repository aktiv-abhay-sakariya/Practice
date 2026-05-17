# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def select_product_template(self, product, category):
        domain = [('is_storable', '=', True)]

        if product:
            domain.append(('id', '=', product))
        if category:
            domain.append(('categ_id', '=', category))

        products = self.search(domain)
        filtered_products = products.filtered(lambda p: len(p.attribute_line_ids) == 2)

        report_data = []
        for prod in filtered_products:
            attr_lines = list(prod.attribute_line_ids)
            line_1 = attr_lines[0]
            line_2 = attr_lines[1]

            # Unique ordered names list for table structure loops
            values_1 = [val.name for val in line_1.value_ids]
            values_2 = [val.name for val in line_2.value_ids]

            # Build a nested coordinate lookup dictionary map: { val_1: { val_2: qty } }
            stock_matrix = {v1: {v2: 0.0 for v2 in values_2} for v1 in values_1}

            for variant in prod.product_variant_ids:
                # Resolve specific attribute values for this variant
                val_1 = variant.product_template_attribute_value_ids.filtered(
                    lambda v: v.attribute_id.id == line_1.attribute_id.id
                ).name
                
                val_2 = variant.product_template_attribute_value_ids.filtered(
                    lambda v: v.attribute_id.id == line_2.attribute_id.id
                ).name

                # Store stock value into the coordinate cross point map safely
                if val_1 in stock_matrix and val_2 in stock_matrix[val_1]:
                    stock_matrix[val_1][val_2] = variant.qty_available

            # Format the matrix dictionary map into a serializable loop list object for Owl JS
            matrix_list = []
            for row_val in values_1:
                row_cols = []
                for col_val in values_2:
                    row_cols.append({
                        'col_value': col_val,
                        'qty': stock_matrix[row_val][col_val]
                    })
                matrix_list.append({
                    'row_value': row_val,
                    'columns': row_cols
                })

            report_data.append({
                'id': prod.id,
                'name': prod.display_name,
                'category': prod.categ_id.name,
                'attribute_1': line_1.attribute_id.name,
                'values_1': values_1, # Horizontal row names list
                'attribute_2': line_2.attribute_id.name,
                'values_2': values_2, # Vertical table column names list
                'matrix': matrix_list, # Structured array for matrix lookups
            })
            
        return report_data
