class Geo:
    'Describing geographic location'

    def __init__(self, name, latitude, longitude, timezone):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone

    def getLocation(self):
        return [self.name, self.latitude, self.longitude, self.timezone]

    def displayLocation(self):
        [city, lat, lon, tz] = self.getLocation()
        print("City:", city)
        print(f"Latitude: {lat:5.2f} Longitude: {lon:5.2f}")
        print("Timezone:", tz)
        print(6*'--')
        return "ok"

print("Creating a location")
tornio   = Geo("Tornio", 65.85, 24.18, 2.0)
helsinki = Geo("Helsinki", 60.16, 24.96, 2.0)
stockholm = Geo("Stockholm", 59.33, 18.07, 1.0)
cities = [tornio, helsinki, stockholm]

print("Display location data")
for location in cities:
    location.displayLocation()


