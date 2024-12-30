#import packages
import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import googlemaps

# using unique Google Maps API Key
GOOGLE_MAPS_API_KEY = "insert your Google Maps API Key "
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

# Backend API  Base URL
BACKEND_URL = "http://backend:8800"  # Replace with your backend URL

# Fetch  all thelocations from the backend
def fetch_locations():
    response = requests.get(f"{BACKEND_URL}/locations")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error,Failed to fetch locations from the backend")
        return []

# Add a new location
def add_location(name, description, latitude, longitude):
    data = {"name": name, "description": description, "latitude": latitude, "longitude": longitude}
    response = requests.post(f"{BACKEND_URL}/locations", json=data)
    if response.status_code == 200:
        st.success("Location added successfully!")
    else:
        st.error("Eror,Failed to add location")

# Delete a location
def delete_location(location_id):
    response = requests.delete(f"{BACKEND_URL}/locations/{location_id}")
    if response.status_code == 200:
        st.success("Location deleted successfully!")
    else:
        st.error("Error,Failed to delete location")

# Update a location
def update_location(location_id, name, description, latitude, longitude):
    data = {"name": name, "description": description, "latitude": latitude, "longitude": longitude}
    response = requests.put(f"{BACKEND_URL}/locations/{location_id}", json=data)
    if response.status_code == 200:
        st.success("Location updated successfully!")
    else:
        st.error("Error,Failed to update location")

# Streamlit app
def main():
    st.title("Cool Places App with Google Maps")
    
    # Search for a place
    st.header("Search for a Place")
    place = st.text_input("Enter a location")
    if st.button("Search"):
        if place:
            result = gmaps.geocode(place)
            if result:
                location = result[0]["geometry"]["location"]
                st.success(f"Found: {result[0]['formatted_address']}")
                st.write(f"Latitude: {location['lat']}, Longitude: {location['lng']}")
                st.session_state["search_result"] = location  # Store the result for reuse
            else:
                st.error("No results found")
    
    # Add a new location
    st.header("Add a New Location")
    name = st.text_input("Name", key="add_name")
    description = st.text_input("Description", key="add_description")
    latitude = st.number_input("Latitude", format="%.6f", key="add_latitude", value=st.session_state.get("search_result", {}).get("lat", 0.0))
    longitude = st.number_input("Longitude", format="%.6f", key="add_longitude", value=st.session_state.get("search_result", {}).get("lng", 0.0))
    if st.button("Add Location"):
        add_location(name, description, latitude, longitude)
    
    # Fetch and display locations
    st.header("Existing Locations")
    locations = fetch_locations()
    if locations:
        for location in locations:
            st.write(f"{location['id']}: {location['name']} ({location['latitude']}, {location['longitude']})")
    
    # Update a location
    st.header("Update a Location")
    location_id = st.number_input("Location ID to Update", min_value=1, key="update_location_id")
    name = st.text_input("New Name", key="update_name")
    description = st.text_input("New Description", key="update_description")
    latitude = st.number_input("New Latitude", format="%.6f", key="update_latitude")
    longitude = st.number_input("New Longitude", format="%.6f", key="update_longitude")
    if st.button("Update Location"):
        update_location(location_id, name, description, latitude, longitude)
    
    # Delete a location
    st.header("Delete a Location")
    delete_id = st.number_input("Location ID to Delete", min_value=1, key="delete_id")
    if st.button("Delete Location"):
        delete_location(delete_id)
    
    # Map with locations marked
    st.header("Map")
    if locations:
        CoolMap = folium.Map(location=[locations[0]["latitude"], locations[0]["longitude"]], zoom_start=5)
        for loc in locations:
            folium.Marker(
                [loc["latitude"], loc["longitude"]],
                popUp=f"{loc['name']}: {loc['description']}"
            ).add_to(CoolMap)
        st_folium(m, width=700, height=500)

if __name__ == "__main__":
    main()
