"""
weather_client.py
Simple client for fetching California weather alerts from the National Weather Service (NWS) API.

Key alert types to handle (currently active):
- Heat Advisory (moderate severity, multiple counties)
- (Future) Fire Weather Watch
- (Future) Flood Warning
- (Future) Winter Storm Alert

The client parses alert type, severity, affected areas, and guidance.
"""

import requests

NWS_ALERTS_ENDPOINT = "https://api.weather.gov/alerts/active?area=CA"


def fetch_active_alerts():
    """Fetch active alerts for California.

    Returns:
        list of dict: Each dict contains keys like 'event', 'areaDesc', 'severity', 'description'.
    """
    response = requests.get(NWS_ALERTS_ENDPOINT, headers={"User-Agent": "california-weather-monitor"})
    response.raise_for_status()
    data = response.json()
    return data.get('features', [])


def parse_alert(alert_feature):
    """Extract relevant fields from an alert feature.

    Args:
        alert_feature (dict): A single feature from the NWS API response.

    Returns:
        dict: Simplified alert info.
    """
    props = alert_feature.get('properties', {})
    return {
        "event": props.get('event'),
        "severity": props.get('severity'),
        "areas": props.get('areaDesc'),
        "description": props.get('description'),
        "instruction": props.get('instruction'),
    }


def get_heat_advisories():
    """Convenience helper to return only heat advisory alerts."""
    alerts = fetch_active_alerts()
    heat = [parse_alert(a) for a in alerts if a.get('properties', {}).get('event') == 'Heat Advisory']
    return heat

if __name__ == "__main__":
    for advisory in get_heat_advisories():
        print(f"{advisory['event']} in {advisory['areas']} – Severity: {advisory['severity']}")
