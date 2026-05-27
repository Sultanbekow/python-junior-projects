"""
Wetter-App für Pythonista 3 auf dem iPhone
API-Key holen: https://home.openweathermap.org/users/sign_up
"""

API_KEY = "DEIN_API_KEY_HIER_EINTRAGEN"  # <-- AUF DEM iPHONE ÄNDERN!

import requests, ui, json
from datetime import datetime

def get_weather_data(city):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "de"}
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json() if r.status_code == 200 else None
    except:
        return None

class WeatherApp(ui.View):
    def __init__(self):
        self.setup_ui()
    
    def setup_ui(self):
        self.name = "🌤️ Wetter"
        self.background_color = "white"
        
        title = ui.Label(frame=(0, 20, self.width, 40))
        title.text = "Wetter-App"
        title.font = ("Helvetica-Bold", 24)
        title.alignment = ui.ALIGN_CENTER
        title.flex = "W"
        self.add_subview(title)
        
        self.city_input = ui.TextField(frame=(20, 70, self.width-120, 40))
        self.city_input.placeholder = "Stadt eingeben"
        self.city_input.flex = "W"
        self.city_input.border_style = ui.BORDER_ROUNDED
        self.add_subview(self.city_input)
        
        search_btn = ui.Button(frame=(self.width-90, 70, 80, 40))
        search_btn.title = "Suchen"
        search_btn.background_color = "#007AFF"
        search_btn.tint_color = "white"
        search_btn.corner_radius = 8
        search_btn.flex = "L"
        search_btn.action = self.search
        self.add_subview(search_btn)
        
        self.result = ui.TextView(frame=(20, 125, self.width-40, self.height-160))
        self.result.editable = False
        self.result.font = ("Menlo", 14)
        self.result.flex = "WH"
        self.result.text = "☀️ Gib eine Stadt ein und tippe auf Suchen"
        self.add_subview(self.result)
    
    def search(self, sender):
        city = self.city_input.text.strip()
        if not city:
            self.result.text = "⚠️ Bitte Stadt eingeben"
            return
        self.result.text = f"⏳ Lade {city} ..."
        import threading
        threading.Thread(target=self.fetch, args=(city,)).start()
    
    def fetch(self, city):
        data = get_weather_data(city)
        def update():
            if data and data.get("cod") == 200:
                t = data["main"]
                w = data["weather"][0]
                self.result.text = f"""
📍 {data['name']}, {data['sys']['country']}
{'─'*25}
🌡️ {t['temp']:.1f}°C (gefühlt {t['feels_like']:.1f}°C)
💧 Luftfeuchtigkeit: {t['humidity']}%
💨 Wind: {data['wind']['speed']} m/s
☁️ {w['description'].capitalize()}
🕐 {datetime.now().strftime('%H:%M:%S')}
"""
            else:
                self.result.text = f"❌ Stadt '{city}' nicht gefunden"
        ui.in_background(update)

if __name__ == "__main__":
    WeatherApp().present(style="fullscreen")
