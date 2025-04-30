#!/usr/bin/env python3
"""
Script to list Codeforces contest participants from a specific country, ordered by contest standing,
with rankings and problem counts appended in the format:

<country_rank>\t<global_rank>\t<problems_solved>\t<profile_url>

Usage:
    python filter_contest_users.py --users-file users_YYYY-MM-DD.json \
                                  --contest-id 1552 \
                                  --country "United States"

This will read the provided users JSON (dumped by fetch_cf_users.py), fetch contest standings
with showUnofficial=true, filter participants by the specified country in the order they appear
in the standings (i.e., by rank), and print each participant’s country-specific rank, global rank,
the number of problems they solved in that contest, and their Codeforces profile URL, tab-separated.
"""
import argparse
import json
import sys
import requests
import re

API_URL = "https://codeforces.com/api/contest.standings"
PROFILE_URL = "https://codeforces.com/profile/{handle}"


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "List Codeforces contest participants from a specific country, "
            "ordered by standing with country/global ranks and solved counts"
        )
    )
    parser.add_argument(
        '--users-file', '-u',
        required=True,
        help='Path to the JSON file with all rated users (from fetch_cf_users.py)'
    )
    parser.add_argument(
        '--contest-id', '-c',
        type=int,
        required=True,
        help='Codeforces contest ID to query'
    )
    parser.add_argument(
        '--country', '-C',
        required=True,
        help='Country name to filter users by (case-insensitive)'
    )
    return parser.parse_args()


def load_users_by_country(users_file: str, country: str):
    """
    Load users from JSON and return a set of handles for the given country.
    Matching is case-insensitive and ignores whitespace.
    """
    try:
        with open(users_file, 'r', encoding='utf-8') as f:
            users = json.load(f)
    except Exception as e:
        print(f"Error reading users file: {e}", file=sys.stderr)
        sys.exit(1)

    country_norm = re.sub(r'\s+', ' ', country.strip().lower())
    return {
        u['handle']
        for u in users
        if u.get('country')
           and re.sub(r'\s+', ' ', u['country'].strip().lower()) == country_norm
    }


def fetch_contest_standings(contest_id: int):
    """
    Fetch full contest standings with showUnofficial=true.
    """
    params = {
        'contestId': contest_id,
        'showUnofficial': 'true',
        'count': 1000000,
    }
    try:
        resp = requests.get(API_URL, params=params)
        resp.raise_for_status()
    except requests.HTTPError as e:
        print(f"HTTP error fetching standings: {e}", file=sys.stderr)
        sys.exit(1)

    data = resp.json()
    if data.get('status') != 'OK':
        print(f"API error: {data.get('comment', '<no comment>')}", file=sys.stderr)
        sys.exit(1)

    return data['result']['rows']


def print_profiles_with_ranks(rows, country_handles):
    """
    Iterate through contest standings rows in order, and for each participant whose handle
    is in country_handles, print (tab-separated):
      country_rank   global_rank   problems_solved   profile_url

    Returns True if any lines were printed, False otherwise.
    """
    printed = set()
    country_rank = 1
    for row in rows:
        overall_rank = row.get('rank')
        # Count solved problems: points>0 in problemResults
        solved = sum(1 for pr in row.get('problemResults', []) if pr.get('points', 0) > 0)
        party = row.get('party', {})
        for member in party.get('members', []):
            handle = member.get('handle')
            if handle in country_handles and handle not in printed:
                url = PROFILE_URL.format(handle=handle)
                # country_rank, global_rank, solved, url
                print(f"{country_rank}\t{overall_rank}\t{solved}\t{url}")
                printed.add(handle)
                country_rank += 1
    return bool(printed)


def main():
    args = parse_args()
    country_handles = load_users_by_country(args.users_file, args.country)
    if not country_handles:
        print(f"No users found in country '{args.country}'", file=sys.stderr)
        sys.exit(1)

    rows = fetch_contest_standings(args.contest_id)
    success = print_profiles_with_ranks(rows, country_handles)
    if not success:
        print(
            f"No participants from '{args.country}' in contest {args.contest_id}",
            file=sys.stderr
        )
        sys.exit(0)

if __name__ == '__main__':
    main()

