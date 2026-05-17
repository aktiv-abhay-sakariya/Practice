/** @odoo-module */
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class ProductSelector extends Component {
    setup() {
        this.orm = useService("orm");
        
        // Define reactive state variables accessible by the XML view
        this.state = useState({
            products: [],          // Populates the Product dropdown
            categories: [],        // Populates the Category dropdown
            selectedProductId: null,
            selectedCategoryId: null,
            reportRecords: [],     // Stores the 2D matrix structure returned from Python
        });

        // Lifecycle hook triggered before component mounts/displays
        onWillStart(async () => {
            // Fetch product options
            this.state.products = await this.orm.searchRead(
                "product.template",
                [["is_storable", "=", true]],
                ["id", "display_name"]
            );
            
            // Fetch category options
            this.state.categories = await this.orm.searchRead(
                "product.category",
                [],
                ["id", "display_name"]
            );

            // Fetch initial matrix layout data (loads all products on start)
            await this.updateStockReport();
        });
    }

    /**
     * Executes the custom backend Python calculation method 
     * and maps results directly into the reactive UI state.
     */
    async updateStockReport() {
        try {
            const result = await this.orm.call(
                "product.template",
                "select_product_template",
                [],
                {
                    product: this.state.selectedProductId,
                    category: this.state.selectedCategoryId,
                }
            );

            // Directly assigns the matrix layout to your XML loop context
            this.state.reportRecords = result;
        } catch (error) {
            console.error("Failed to load variant matrix stock data:", error);
        }
    }

    /**
     * Event listener callback triggered when any filtering dropdown choice switches.
     */
    async onSelectionChange(ev) {
        const changedElement = ev.target.name;
        const rawValue = ev.target.value;

        // Clean value: "all" or empty states become 'null', passing None/False to Python
        const selectedValue = (rawValue === "all" || !rawValue) ? null : parseInt(rawValue, 10);

        if (changedElement === "product") {
            this.state.selectedProductId = selectedValue;
        } else if (changedElement === "category") {
            this.state.selectedCategoryId = selectedValue;
        }

        // Re-run the matrix layout process with the new values
        await this.updateStockReport();
    }
}

// Map the template string key identification reference
ProductSelector.template = "product_variant_attribute_wise_stock_report.ProductSelectorTemplate";

// Add component to Odoo's web client action management registry pipeline
registry.category("actions").add("product_variant_attribute_wise_stock_report.ProductSelectorTemplate", ProductSelector);
