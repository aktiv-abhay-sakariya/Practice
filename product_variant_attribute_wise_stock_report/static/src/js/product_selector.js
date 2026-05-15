/** @odoo-module */
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class ProductSelector extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            products: [],
            categories: [],
            selectedProductId: null,
            selectedCategoryId: null
        });

        onWillStart(async () => {
            // In Odoo 19, 'is_storable' replaces older product type fields
            this.state.products = await this.orm.searchRead(
                "product.template",
                [["is_storable", "=", true]],
                ["id", "display_name"]
            );
            this.state.categories = await this.orm.searchRead(
                "product.category",
                [],
                ["id", "display_name"]
            );
        });
    }

    async onSelectionChange(ev) {
        const changedElement = ev.target.name;
        const selectedValue = ev.target.value ? parseInt(ev.target.value, 10) : null;

        if (changedElement === "product") {
            this.state.selectedProductId = selectedValue;
        } else if (changedElement === "category") {
            this.state.selectedCategoryId = selectedValue;
        }

        if (selectedValue) {
            await this.orm.call(
                "product.template",
                "select_product_template",
                [],
                {
                    product: this.state.selectedProductId,
                    category: this.state.selectedCategoryId,
                }
            );
        }
    }
}

ProductSelector.template = "product_variant_attribute_wise_stock_report.ProductSelectorTemplate";
registry.category("actions").add("product_variant_attribute_wise_stock_report.ProductSelectorTemplate", ProductSelector);
