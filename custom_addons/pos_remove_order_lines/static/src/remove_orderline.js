import {PartnerList} from "../../../../addons/point_of_sale/static/src/app/screens/partner_list/partner_list";

export class PosStore extends WithLazyGetterTrap {

    async selectPartner(currentOrder = this.getOrder()) {
        // FIXME, find order to refund when we are in the ticketscreen.
        if (!currentOrder) {
            return false;
        }
        const currentPartner = currentOrder.getPartner();
        if (currentPartner && currentOrder.getHasRefundLines()) {
            this.dialog.add(AlertDialog, {
                title: _t("Can't change customer"),
                body: _t(
                    "This order already has refund lines for %s. We can't change the customer associated to it. Create a new order for the new customer.",
                    currentPartner.name
                ),
            });
            return currentPartner;
        }
        const payload = await makeAwaitable(this.dialog, PartnerList, {
            partner: currentPartner,
        });

        this.setPartnerToCurrentOrder(payload || false);

        return payload;
    }
}