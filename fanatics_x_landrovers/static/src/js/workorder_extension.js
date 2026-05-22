/** @odoo-module **/

import { MrpWorksheet } from '@mrp_workorder/mrp_display/mrp_record_line/mrp_worksheet';
import { useState, onWillStart } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { fetchOperationNote } from "@mrp_workorder/mrp_display/mrp_record_line/mrp_workorder";
import { MrpWorksheetDialog } from "@mrp_workorder/mrp_display/dialog/mrp_worksheet_dialog";


patch(MrpWorksheet.prototype, {
    async clicked() {
        console.log("clicked here!!!!!");
        let worksheetData = false;
        if (this.props.record.data.worksheet) {
            console.log("CLICKED PROPS", this.props.record.data);
            const sheet = await this.props.record.model.orm.read(
                "mrp.workorder",
                [this.props.record.resId],
                ["worksheet"]
            );
            worksheetData = {
                resModel: "mrp.workorder",
                resId: this.props.record.resId,
                resField: "worksheet",
                value: sheet[0].worksheet,
                page: 1,
            };
        } else if (this.props.record.data.worksheet_google_slide) {
            worksheetData = {
                resModel: "mrp.workorder",
                resId: this.props.record.resId,
                resField: "worksheet_google_slide",
                value: this.props.record.data.worksheet_google_slide,
                page: 1,
            };
        }
        if (!this.props.record.data.operation_note) {
            this.props.record.data.operation_note  = await fetchOperationNote(this);
        }

        let knowledgeArticleIds = null;

        if (this.props.record.data.operation_id) {
            const [operation] = await this.props.record.model.orm.read(
                "mrp.routing.workcenter",
                [this.props.record.data.operation_id[0]],
                ["knowledge_article_ids"]
            );

            // Check if the operation and the IDs exist
            if (operation && operation.knowledge_article_ids.length > 0) {
                // Just grab the array of IDs
                knowledgeArticleIds = operation.knowledge_article_ids;
            }
        }

        this.dialog.add(MrpWorksheetDialog, {
            worksheetText: this.props.record.data.operation_note,
            worksheetData,
            knowledgeArticleIds,
        });
    }
});


// The prop definition is still correct
MrpWorksheetDialog.props.knowledgeArticleIds = { type: Array, optional: true };

patch(MrpWorksheetDialog.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");

        // The state will now hold an array of article objects {id, display_name}
        this.state = useState({ articles: [] });

        onWillStart(async () => {
            const articleIds = this.props.knowledgeArticleIds;
            if (articleIds && articleIds.length > 0) {
                // Read the display_name for all received IDs
                const articlesData = await this.orm.read(
                    "knowledge.article",
                    articleIds,
                    ["display_name"]
                );
                this.state.articles = articlesData;
            }
        });
    }
});