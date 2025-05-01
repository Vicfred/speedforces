#!/usr/bin/env python3
import argparse
import sys
import requests
import json
import matplotlib.pyplot as plt


def fetch_contest_standings(contest_id: int):
    """
    Query the Codeforces API for contest standings.

    :param contest_id: Numeric ID of the contest
    :return: Parsed JSON response
    """
    url = "https://codeforces.com/api/contest.standings"
    params = {
        "contestId": contest_id,
        "showUnofficial": "false",
        "participantTypes": "CONTESTANT",
    }

    response = requests.get(url, params=params)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        sys.exit(f"HTTP error: {e}")

    data = response.json()
    if data.get("status") != "OK":
        sys.exit(f"API error: {data.get('comment', 'Unknown error')}")

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch Codeforces contest standings and plot solvers per problem with bin % annotations."
    )
    parser.add_argument(
        "contestId", type=int, help="ID of the Codeforces contest (e.g. 1552)"
    )
    args = parser.parse_args()

    # Fetch standings
    data = fetch_contest_standings(args.contestId)
    problems = data["result"]["problems"]
    rows = data["result"]["rows"]

    # Compute number of solvers for each problem
    solves_per_problem = []
    for i in range(len(problems)):
        count = sum(
            1 for row in rows if row.get("problemResults", [])[i].get("points", 0) > 0
        )
        solves_per_problem.append(count)

    total = len(rows)
    labels = [p["index"] for p in problems]

    # Plot bar chart
    plt.figure(figsize=(12, 7))
    bars = plt.bar(labels, solves_per_problem, edgecolor="black", width=0.6)

    # Add headroom and grid
    max_height = max(solves_per_problem, default=0)
    plt.ylim(0, max_height * 1.10)
    plt.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)

    # Offset for bin % annotation
    off_bin = max_height * 0.02

    # Annotate bars with bin % only
    for count, bar in zip(solves_per_problem, bars):
        if count == 0:
            continue
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height()
        pct = count / total * 100
        plt.text(
            x,
            y + off_bin,
            f"{pct:.1f}%",
            ha="center",
            va="bottom",
            fontsize=10,
            color="black",
        )

    # Legend for bin %
    plt.legend(
        [bar],
        ["Bin %"],
        loc="upper right",
        frameon=True,
        fontsize=10,
        title="Annotation",
    )

    # Labels and title
    plt.xlabel("Problem", fontsize=12)
    plt.ylabel("Number of Solvers", fontsize=12)
    plt.title(f"Contest {args.contestId} — Solvers per Problem", fontsize=14)
    plt.tight_layout()

    # Save output
    out_file = f"img/contest_{args.contestId}_solves_per_problem.png"
    plt.savefig(out_file)
    print(f"Solvers per problem chart with bin % annotations saved to {out_file}")
