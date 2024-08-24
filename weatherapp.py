import folium
from geopy.geocoders import Nominatim

# Create a map centered around a specific location
map_center = [0, 0]  # Default center
my_map = folium.Map(location=map_center, zoom_start=2)

# Function to generate Street View link
def generate_street_view_link(lat, lon):
    street_view_url = f'https://www.google.com/maps?q=&layer=c&cbll={lat},{lon}'
    return f'<a href="{street_view_url}" target="_blank">Street View</a>'

# Function to handle user clicks on the map
def on_map_click(event):
    lat, lon = event.latlng  # Get the latitude and longitude of the clicked point

    # Reverse geocode to get the address
    geolocator = Nominatim(user_agent="map_app")
    location = geolocator.reverse((lat, lon))
    address = location.address

    # Generate a Google Street View link
    street_view_link = generate_street_view_link(lat, lon)

    # Create a popup with the address, latitude, longitude, and Street View link
    popup_content = f'Address: {address}<br>Latitude: {lat}<br>Longitude: {lon}<br>Street View: {street_view_link}'

    # Create a marker with the popup
    marker = folium.Marker(location=[lat, lon], popup=popup_content)
    marker.add_to(my_map)

# Add click event listener to the map
my_map.add_child(folium.ClickForMarker(popup='Click here to pinpoint'))

# Save the map to an HTML file
my_map.save('pinpoint_map.html')

# Open the map in a web browser
import webbrowser
webbrowser.open('pinpoint_map.html')
