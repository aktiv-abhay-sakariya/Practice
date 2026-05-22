/** @odoo-module **/

import { Composer } from "@mail/core/common/composer";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { toRaw } from "@odoo/owl";

patch(Composer.prototype, {
    async sendMessage() {
        const composer = toRaw(this.props.composer);

        // If we are editing a message, let it proceed without confirmation.
        if (composer.message) {
            this.editMessage();
            return;
        }

        // The original logic for sending a message.
        const proceed = async () => {
            await this.processMessage(async (value) => {
                await this._sendMessage(value, this.postData, this.extraData);
            });
        };

        // If it's a log note, send it directly without the pop-up.
        if (!this.props.type || this.props.type === "note") {
            return proceed();
        }

        // If it's a message (email sending), show confirmation popup
        if (this.props.type === "message") {
            this.env.services.dialog.add(ConfirmationDialog, {
                body: _t("You're about to send an email to all followers. This may include customers or vendors! Check the follower list before sending, and remove the unwanted recipients."),
                confirm: proceed,
                cancel: () => {},
                title: _t("Confirm Sending Mail"),
            });
        }
    }
});