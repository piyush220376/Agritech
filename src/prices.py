"""
prices.py  –  Fetch mandi (crop market) prices via the data.gov.in REST API.

API dataset  : Current daily price of various commodities from various markets (Mandi)
Resource ID  : 9ef84268-d588-465a-a308-a864a43d0070
Docs         : https://data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070

How to get a free API key:
  1. Register at https://data.gov.in/
  2. Open the dataset page → "Data API" tab → copy your key.
  3. Set the environment variable  DATA_GOV_API_KEY=<your-key>
     OR place it in a .env file next to main.py.
"""

import os
import requests

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
# Resource ID for "Current daily price of various commodities from various markets (Mandi)"
_RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
_BASE_URL = f"https://api.data.gov.in/resource/{_RESOURCE_ID}"

# Load API key from environment (set via .env or shell export)
_API_KEY = os.getenv("DATA_GOV_API_KEY", "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b")

# State fixed to Madhya Pradesh for this project
MP_STATE_NAME = "Madhya Pradesh"

# ---------------------------------------------------------------------------
# DROPDOWN INDEX  (for UI combo boxes)
# ---------------------------------------------------------------------------
def build_mp_slug_index(force=False, timeout=30):
    """
    Static lookup for UI drop-downs.
    Keys are slugs / display names used both in UI and as API filter values.
    """
    markets = {
        "Indore": "Indore",
        "Bhopal": "Bhopal",
        "Ujjain": "Ujjain",
        "Gwalior": "Gwalior",
        "Jabalpur": "Jabalpur",
    }

    commodities = {
        "Wheat": "Wheat",
        "Rice": "Rice",
        "Soyabean": "Soyabean",
        "Cotton": "Cotton",
        "Tomato": "Tomato",
        "Onion": "Onion",
        "Potato": "Potato",
    }

    return {
        "state": {"name": MP_STATE_NAME},
        "markets": markets,
        "commodities": commodities,
    }


# ---------------------------------------------------------------------------
# MAIN FETCH  (data.gov.in REST API → JSON)
# ---------------------------------------------------------------------------
def fetch_commodityonline_precise(commodity, state, market, timeout=20, limit=10):
    """
    Fetch mandi prices from data.gov.in for the given commodity/state/market.

    Returns:
        list[dict]  – normalised price rows on success
        [{'error': str}]  – on failure
    """
    params = {
        "api-key": _API_KEY,
        "format": "json",
        "limit": limit,
        "offset": 0,
        "filters[State]": state or MP_STATE_NAME,
        "filters[Market]": market,
        "filters[Commodity]": commodity,
    }

    headers = {"User-Agent": "AI-Farmer-ChatBot/1.0"}

    try:
        resp = requests.get(_BASE_URL, params=params, headers=headers, timeout=timeout)

        if resp.status_code == 401:
            return [{"error": "Invalid API key – set DATA_GOV_API_KEY in your .env file."}]

        if resp.status_code != 200:
            return [{"error": f"API error {resp.status_code}: {resp.text[:200]}"}]

        data = resp.json()

        records = data.get("records", [])
        if not records:
            return [{"error": f"No price data found for {commodity} in {market} ({state})."}]

        rows = []
        for rec in records:
            rows.append({
                "commodity": rec.get("commodity", commodity),
                "market":    rec.get("market",    market),
                "state":     rec.get("state",     state),
                "min":       rec.get("min_price", "-"),
                "modal":     rec.get("modal_price", "-"),
                "max":       rec.get("max_price", "-"),
                "date":      rec.get("arrival_date", "-"),
                "grade":     rec.get("grade", "-"),
            })
        return rows

    except requests.ConnectionError:
        return [{"error": "No internet connection. Cannot fetch live prices."}]
    except requests.Timeout:
        return [{"error": "Request timed out. Please try again."}]
    except Exception as exc:
        return [{"error": f"Unexpected error: {exc}"}]
