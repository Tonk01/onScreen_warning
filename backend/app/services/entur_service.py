import httpx 

import xml.etree.ElementTree as ET
from backend.app.models.alert import Alert, Affects

ENTUR_ALERTS_URL = "https://api.entur.io/realtime/v1/rest/sx"

async def get_service_alerts():
    params = {
        "datasetId": "SKY"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            ENTUR_ALERTS_URL,
            params = params       
        )

        response.raise_for_status()

    root = ET.fromstring(response.text)

    alerts = []

    for situation in root.findall(".//{*}PtSituationElement"):

        situation_number = get_text(
            situation,
            "{*}SituationNumber"
        )

        creation_time = get_text(
            situation,
            "{*}CreationTime"
        )

        progress = get_text(
            situation,
            "{*}Progress"
        )

        severity = get_text(
            situation,
            "{*}Severity"
        )

        summary = get_text(
            situation,
            "{*}Summary"
        )

        description = get_text(
            situation,
            "{*}Description"
        )

        start_time = get_text(
            situation,
            ".//{*}ValidityPeriod/{*}StartTime"
        )

        end_time = get_text(
            situation,
            ".//{*}ValidityPeriod/{*}EndTime"
        )

        affects = parse_affects(situation)

        alert = Alert(
            id = situation_number,
            creation_time = creation_time,
            status = progress,
            severity = severity,
            start_time = start_time,
            end_time = end_time,
            summary = summary,
            description = description,
            affects = affects,
        )
        alerts.append(alert)

    return alerts

def get_text(element, path):
    child = element.find(path)

    if child is None:
        return None

    return child.text

def parse_affects(situation):
    lines = []
    stops = []
    journeys = []

    for line in situation.findall(".//{*}AffectedLine/{*}LineRef"):
        if line.text:
            lines.append(line.text)

    for stop in situation.findall(".//{*}AffectedStopPoint/{*}StopPointRef"):
        if stop.text:
            stops.append(stop.text)

    for journey in situation.findall(".//{*}DatedVehicleJourneyRef"):
        if journey.text:
            journeys.append(journey.text)

    return Affects(
        lines =list(dict.fromkeys(lines)),
        stops = list(dict.fromkeys(stops)),
        journeys = list(dict.fromkeys(journeys))
    )
