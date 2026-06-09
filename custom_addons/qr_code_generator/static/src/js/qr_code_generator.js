/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState, useRef } from "@odoo/owl";

export class QRSystrayIcon extends Component {
    static template = "qr_code_generator.systray_icon";

    setup() {
        this.state = useState({
            open: false,
        });
        this.qrContainerRef = useRef("qrContainer");
    }

    openQRData() {
        this.state.open = !this.state.open;
    }

    onInputChange(ev) {
        this.state.text = ev.target.value;
    }

    clearQRData() {
        const container = this.qrContainerRef.el;
        container.innerHTML = "";
        this.state.text = "";
    }

    generateQRData() {
        const container = this.qrContainerRef.el;

        if (this.state.text){
            container.innerHTML = "";
            new QRCode(container, {
                text: this.state.text,
                width: 180,
                height: 180,
            });
        }
    }
}

registry.category("systray").add("qr_code_generator.QRSystrayIcon", {
    Component: QRSystrayIcon,
});

