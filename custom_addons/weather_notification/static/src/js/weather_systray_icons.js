/** @odoo-module **/
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { Component, useState } from "@odoo/owl";

export class WeatherSystrayIcon extends Component {
    static template = "weather_notification.systray_icon"
    setup() {
        this.state = useState({
            temp: "",
            condition: "",
            location: "",
            date:"",
            last_updated:"",
            latitude:"",
            longitude:"",
            lat_lon:"",
            open: false,
        });
        this.loadWeatherData();
    }

    async loadWeatherData() {
        const result = await rpc("/my_api/data", {});
        if (result.status === "success") {
            this.state.temp = result.temp;
            this.state.condition = result.condition;
            this.state.location = result.location;
            this.state.date = result.date;
            this.state.last_updated = result.last_updated;
            this.state.lat_lon = result.lat_lon;
            this.state.latitude = result.latitude;
            this.state.longitude = result.longitude;
        }
    }

    showWeatherDate() {
        this.state.open = !this.state.open;
    }
}

registry.category("systray").add("weather_notification.WeatherSystrayIcon", {
    Component: WeatherSystrayIcon,
});
