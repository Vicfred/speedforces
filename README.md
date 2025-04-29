# Codeforces Contest Analyzer

This repository contains two Python scripts for analyzing Codeforces contest standings:

- **`problem_distribution.py`**: Fetches contest standings and plots a histogram of problems solved per contestant, annotated with percentages.
- **`number_of_problems_distribution.py`**: Fetches contest standings and plots a bar chart of how many users solved each problem, annotated with bin percentages.

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

- **Plot problems solved distribution per contestant**

  ```bash
  python problem_distribution.py <contestId>
  ```

  Example:

  ```bash
  python problem_distribution.py 1552
  ```

  This will generate `contest_<contestId>_histogram.png` in the current directory.

- **Plot solvers per problem**

  ```bash
  python number_of_problems_distribution.py <contestId>
  ```

  Example:

  ```bash
  python number_of_problems_distribution.py 1552
  ```

  This will generate `contest_<contestId>_solves_per_problem.png` in the current directory.

## License

This project is licensed under the BSD License. Feel free to modify and distribute.
