# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import requests
from datetime import date


class WeatherApi(http.Controller):

    @http.route('/my_api/data', type='jsonrpc', auth = 'user')
    def fetch_api_data(self):
        api_key = "b7af15afbe6b4a9e93b43427260406"
        if request.env.user.is_lan_long and request.env.user.latitude and request.env.user.longitude:
            latitude = request.env.user.latitude
            longitude = request.env.user.longitude

            lat_lon_api_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={latitude},{longitude}"

            lat_lon_response = requests.get(lat_lon_api_url)
            lat_lon_api_data = lat_lon_response.json()

            return {
                'status': 'success',
                'temp': lat_lon_api_data.get('current', {}).get('temp_c'),
                'condition': lat_lon_api_data.get('current', {}).get('condition', {}).get('text'),
                'date': date.today(),
                'last_updated': lat_lon_api_data.get('current', {}).get('last_updated'),
                'latitude': latitude,
                'longitude': longitude,
                'lat_lon': True,
            }

        else:
            if request.env.user.state_id:
                place_name = request.env.user.state_id.name
            else:
                place_name = request.env.user.country_id.name

            api_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={place_name}"

            response = requests.get(api_url)
            api_data = response.json()

            return {
                'status': 'success',
                'temp': api_data.get('current', {}).get('temp_c'),
                'condition': api_data.get('current', {}).get('condition', {}).get('text'),
                'location': place_name,
                'date': date.today(),
                'last_updated': api_data.get('current', {}).get('last_updated'),
                'lat_lon': False,
            }
