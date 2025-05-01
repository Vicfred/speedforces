#!/usr/bin/env python3
import argparse
import sys
import requests
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


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
        description="Fetch Codeforces contest standings and plot histogram with annotations."
    )
    parser.add_argument(
        "contestId", type=int, help="ID of the Codeforces contest (e.g. 1552)"
    )
    args = parser.parse_args()

    # Fetch data and compute solved counts
    data = fetch_contest_standings(args.contestId)
    solved_counts = [
        sum(1 for p in row.get("problemResults", []) if p.get("points", 0) > 0)
        for row in data["result"]["rows"]
    ]

    # Histogram parameters
    total = len(solved_counts)
    max_solved = max(solved_counts, default=0)
    bins = range(max_solved + 2)

    plt.figure(figsize=(12, 7))
    counts, edges, patches = plt.hist(
        solved_counts, bins=bins, align="left", edgecolor="black", rwidth=0.8
    )

    # Add headroom for annotations
    max_height = max(counts, default=0)
    plt.ylim(0, max_height * 1.25)
    plt.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)

    # Precompute reverse cumulative sums
    rev_cumul = []
    running = 0
    for c in reversed(counts):
        running += c
        rev_cumul.append(running)
    rev_cumul = list(reversed(rev_cumul))

    # Offsets for annotations
    off_bin = max_height * 0.02
    off_cum = max_height * 0.06
    off_rev = max_height * 0.10

    cumulative = 0
    for i, (count, patch) in enumerate(zip(counts, patches)):
        if count == 0:
            continue

        x = patch.get_x() + patch.get_width() / 2
        y = patch.get_height()

        # Bin percentage
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

        # Cumulative percentage
        cumulative += count
        cum_pct = cumulative / total * 100
        plt.text(
            x,
            y + off_cum,
            f"{cum_pct:.1f}%",
            ha="center",
            va="bottom",
            fontsize=10,
            color="red",
        )

        # Reverse cumulative percentage
        rev_pct = rev_cumul[i] / total * 100
        plt.text(
            x,
            y + off_rev,
            f"{rev_pct:.1f}%",
            ha="center",
            va="bottom",
            fontsize=10,
            color="blue",
        )

    # Legend box using matplotlib patches, moved to upper right
    handles = [
        mpatches.Patch(color="black", label="Bin %"),
        mpatches.Patch(color="red", label="Cumulative %"),
        mpatches.Patch(color="blue", label="Reverse cumulative %"),
    ]
    plt.legend(
        handles=handles,
        loc="upper right",
        frameon=True,
        fontsize=10,
        title="Percentages",
    )

    # Labels and title
    plt.xlabel("Number of Problems Solved", fontsize=12)
    plt.ylabel("Number of Contestants", fontsize=12)
    plt.title(f"Contest {args.contestId} — Problems Solved Distribution", fontsize=14)
    plt.xticks(bins[:-1], fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()

    # Save figure
    out_file = f"img/contest_{args.contestId}_histogram.png"
    plt.savefig(out_file)
    print(f"Contest histogram saved to {out_file}")
