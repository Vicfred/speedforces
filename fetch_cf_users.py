#!/usr/bin/env python3
import requests
import json
import sys
from datetime import date

API_URL = "https://codeforces.com/api/user.ratedList"

def fetch_all_users(active_only: bool = False, include_retired: bool = True):
    """
    Fetch the list of all users who have ever participated in a rated contest.
    """
    params = {
        'activeOnly': str(active_only).lower(),
        'includeRetired': str(include_retired).lower(),
    }
    resp = requests.get(API_URL, params=params)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        print(f"HTTP error: {e}", file=sys.stderr)
        sys.exit(1)

    payload = resp.json()
    if payload.get('status') != 'OK':
        print(f"API error: {payload.get('comment', '<no comment>')}", file=sys.stderr)
        sys.exit(1)

    return payload['result']

def save_to_file(data, filename: str):
    """
    Save the JSON-serializable data to a file with pretty formatting.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(data)} users to '{filename}'")

def main():
    users = fetch_all_users(active_only=False, include_retired=True)
    today = date.today().isoformat()              # e.g. '2025-04-29'
    filename = f"users_{today}.json"
    save_to_file(users, filename)

if __name__ == '__main__':
    main()
