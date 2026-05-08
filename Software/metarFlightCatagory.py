import requests
from requests.models import Response
from datetime import datetime, timezone

def getMetarFlightCategory(airportCode : str) -> str:

    zuluTime : str = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')
    zuluTimeReadable : str = datetime.now(timezone.utc).strftime('%B %d, %Y %H:%M UTC')

    print(zuluTime)
    print(zuluTimeReadable)
    
    url : str = "https://aviationweather.gov/api/data/metar"
    params : dict[str, str] = {
        "ids": airportCode,
        "format": "json",
        "taf": "false",
        "hours": "2.0",
        "date": zuluTime,
    }
    
    try:
        request : Response = requests.get(
            url,
            params=params,
            timeout=10,
            headers={"Accept": "application/json"},
        )
        request.raise_for_status()
    except Exception as e:
        print("Error fetching METAR data: " + str(e))
        return "Unknown"

    if not request.text.strip():
        print(f"Empty METAR response for {airportCode}")
        return "Unknown"

    try:
        data = request.json()
    except ValueError:
        print(f"Invalid JSON METAR response for {airportCode}: status={request.status_code}")
        print(request.text[:200])
        return "Unknown"

    try:
        if isinstance(data, list) and len(data) > 0:
            flightCategory : str = data[0].get('fltCat', 'Unknown')
            return flightCategory if flightCategory else "Unknown"

        if isinstance(data, dict):
            flightCategory : str = data.get('fltCat', 'Unknown')
            return flightCategory if flightCategory else "Unknown"

        print(f"Unexpected METAR response format for {airportCode}: {type(data).__name__}")
        return "Unknown"

    except Exception as e:
        print("Error parsing METAR data: " + str(e))
        return "Unknown"

# for testing
print(getMetarFlightCategory("KJFK"))