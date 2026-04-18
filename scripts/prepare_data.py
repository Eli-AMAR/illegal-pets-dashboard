from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_CSV = ROOT / 'data' / 'raw' / 'Illegal_Animal.csv'
RAW_GEOJSON = ROOT / 'data' / 'raw' / 'nyc-zip-code-tabulation-areas-polygons.geojson'
OUT_COMPLAINTS = ROOT / 'public' / 'illegal-animal-complaints.json'
OUT_GEOJSON = ROOT / 'public' / 'nyc-zip-boundaries.geojson'


def main() -> None:
    df = pd.read_csv(RAW_CSV)
    df['created'] = pd.to_datetime(df['Created Date'], format='%Y %b %d %I:%M:%S %p', errors='coerce')
    df['closed'] = pd.to_datetime(df['Closed Date'], format='%Y %b %d %I:%M:%S %p', errors='coerce')
    reference_date = df['created'].max()
    df['case_age_days'] = ((df['closed'].fillna(reference_date) - df['created']).dt.total_seconds() / 86400).fillna(0)

    complaints = []
    for _, row in df.iterrows():
        zip_code = None
        if pd.notna(row['Incident Zip']):
            try:
                candidate = int(row['Incident Zip'])
                if 10000 <= candidate <= 11697:
                    zip_code = f'{candidate:05d}'
            except ValueError:
                pass

        complaints.append(
            {
                'id': str(row['Unique Key']),
                'created': row['created'].isoformat() if pd.notna(row['created']) else None,
                'closed': row['closed'].isoformat() if pd.notna(row['closed']) else None,
                'complaintType': row['Problem (formerly Complaint Type)'],
                'animalDetail': row['Problem Detail (formerly Descriptor)'],
                'locationType': row['Location Type'],
                'zip': zip_code,
                'borough': str(row['Borough']).title() if pd.notna(row['Borough']) else None,
                'status': row['Status'],
                'caseAgeDays': round(float(row['case_age_days']), 2),
            }
        )

    OUT_COMPLAINTS.write_text(json.dumps(complaints, separators=(',', ':')))

    geojson = json.loads(RAW_GEOJSON.read_text())
    valid_zips = {item['zip'] for item in complaints if item['zip']}
    trimmed = {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'properties': {
                    'zip': feature['properties']['postalCode'],
                    'borough': feature['properties'].get('borough'),
                    'placeName': feature['properties'].get('PO_NAME'),
                },
                'geometry': feature['geometry'],
            }
            for feature in geojson['features']
            if feature['properties'].get('postalCode') in valid_zips
        ],
    }
    OUT_GEOJSON.write_text(json.dumps(trimmed, separators=(',', ':')))


if __name__ == '__main__':
    main()
