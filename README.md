# Codeforces Contest Analyzer

This repository contains four Python scripts for interacting with and analyzing Codeforces data:

- **`problem_distribution.py`**  
  Fetches contest standings and plots a histogram of problems solved per contestant, annotated with percentages.

- **`number_of_problems_distribution.py`**  
  Fetches contest standings and plots a bar chart of how many users solved each problem, annotated with bin percentages.

- **`fetch_cf_users.py`**  
  Fetches **all** Codeforces users who have ever participated in a rated contest (including inactive/retired) and saves them to a timestamped JSON file.

- **`filter_contest_users.py`**  
  Reads a users JSON dump (from `fetch_cf_users.py`) and filters contest participants by country, printing country rank, global rank, number of problems solved, and profile URLs for each user in the specified contest.

---

## Prerequisites

- **Python 3.8+**  
- **Git**

## Setup

1. **Clone the repository**

   ```bash
   git clone git@github.com:Vicfred/speedforces.git
   cd speedforces
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` should include:

   ```text
   requests
   matplotlib
   ```

## Usage

### 1. Plot problems solved distribution per contestant

```bash
python problem_distribution.py <contestId>
```

- **Example:**

  ```bash
  python problem_distribution.py 1552
  ```

- **Output:**  
  `contest_<contestId>_histogram.png` (a histogram of solves per contestant).

---

### 2. Plot number of solvers per problem

```bash
python number_of_problems_distribution.py <contestId>
```

- **Example:**

  ```bash
  python number_of_problems_distribution.py 1552
  ```

- **Output:**  
  `contest_<contestId>_solves_per_problem.png` (a bar chart of solver counts per problem).

---

### 3. Fetch and save all rated Codeforces users

```bash
python fetch_cf_users.py
```

- **What it does:**  
  Calls the Codeforces API method `user.ratedList?activeOnly=false&includeRetired=true` to retrieve every user who’s ever participated in a rated contest, then writes the full list to a JSON file.

- **Output file:**  
  `users_<YYYY-MM-DD>.json`  
  e.g. `users_2025-04-29.json`

---

### 4. Filter contest participants by country

```bash
python filter_contest_users.py --users-file users_<YYYY-MM-DD>.json --contest-id <contestId> --country "<Country Name>"
```

- **What it does:**  
  Reads the JSON dump created by `fetch_cf_users.py`, fetches contest standings with `showUnofficial=true`, and prints a tab-delimited list of users from the specified country in that contest.

- **Output format (tab-separated):**
  ```
  <country_rank>    <global_rank>    <problems_solved>    <profile_url>
  ```

- **Example:**

  ```bash
  python filter_contest_users.py --users-file users_2025-04-29.json --contest-id 1552 --country "United States"
  ```

---

## License

This project is licensed under the BSD License. Feel free to modify and distribute.
