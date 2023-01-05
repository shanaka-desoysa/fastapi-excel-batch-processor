from fastapi import FastAPI, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import geocoder

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add a sample Excel file to the documentation
sample_file_path = 'sample.xlsx'

description = f"""
Expects an excel file with columns: UN/LOCODE, City, State, ZIP Code <a href="/static/example_input.xlsx">Example Input</a>.<br>
Returns a modified excel file with columns: UN/LOCODE, City, State, ZIP Code, Latitude, Longitude, Google Maps URL <a href="/static/example_output.xlsx">Example Output</a>
"""


@app.post("/batch/", description=description, response_description="Modified Excel file")
async def batch_process(file: bytes = File(...)):
    # Read the Excel file into a Pandas DataFrame
    df = pd.read_excel(file)
    
    # Geocode the cities and add the latitude, longitude, and Google Maps URL columns to the DataFrame
    latitudes = []
    longitudes = []
    google_maps_urls = []
    for city, state, zip_code in df[['City', 'State', 'ZIP Code']].values:
        address = f"{city}, {state} {zip_code}"
        g = geocoder.arcgis(address)
        latitudes.append(g.latlng[0])
        longitudes.append(g.latlng[1])
        google_maps_url = f"https://maps.google.com?q={g.latlng[0]},{g.latlng[1]}"
        google_maps_urls.append(google_maps_url)
    df['Latitude'] = latitudes
    df['Longitude'] = longitudes
    df['Google Maps URL'] = google_maps_urls
    
    # Create a temporary file to store the modified DataFrame
    temp_file = '/tmp/modified.xlsx'
    df.to_excel(temp_file, index=False)
    
    # Return the modified DataFrame as an Excel file response
    headers = {
        "Content-Disposition": "attachment; filename=modified.xlsx"
    }
    return FileResponse(temp_file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)
