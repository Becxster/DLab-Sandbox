# data_loader.py
# Reads CSV inputs and returns sets + parameter dictionaries
# YOU SHOULD NOT NEED TO EDIT THIS FILE.

import csv
from typing import Dict, List, Tuple


def load_event_data(
    events_csv_path: str,
    conflicts_csv_path: str = None,
):
    """
    Reads:
      - events.csv with columns: name,category,cost,hours,benefit
      - conflicts.csv with columns: event1,event2   (optional)

    Returns a tuple:
      I: List[str]                         # event names
      C: List[str]                         # categories
      category: Dict[str, str]             # category[i]
      cost: Dict[str, int]                 # cost[i]
      hours: Dict[str, int]                # hours[i]
      benefit: Dict[str, int]              # benefit[i]
      conflicts: List[Tuple[str, str]]     # (i,j) pairs with x[i] + x[j] <= 1
    """

    # --- Read events.csv ---
    I: List[str] = []
    category: Dict[str, str] = {}
    cost: Dict[str, int] = {}
    hours: Dict[str, int] = {}
    benefit: Dict[str, int] = {}

    with open(events_csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Basic check
        required = {"name", "category", "cost", "hours", "benefit"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(
                f"events.csv must contain columns {sorted(required)}. "
                f"Found {reader.fieldnames}."
            )

        for row in reader:
            name = row["name"].strip()
            if not name:
                raise ValueError("Found an event with an empty name.")

            if name in category:
                raise ValueError(f"Duplicate event name found in events.csv: {name}")

            cat = row["category"].strip()
            if not cat:
                raise ValueError(f"Event '{name}' has an empty category.")

            try:
                c = int(row["cost"])
                h = int(row["hours"])
                b = int(row["benefit"])
            except ValueError:
                raise ValueError(f"Non-integer value in row for event '{name}': {row}")

            if c < 0 or h < 0 or b < 0:
                raise ValueError(f"Negative value in row for event '{name}': {row}")

            I.append(name)
            category[name] = cat
            cost[name] = c
            hours[name] = h
            benefit[name] = b

    # --- Build category set C ---
    C = sorted(set(category[i] for i in I))

    # --- Read conflicts.csv (optional) ---
    conflicts: List[Tuple[str, str]] = []
    if conflicts_csv_path is not None:
        with open(conflicts_csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            required = {"event1", "event2"}
            if not required.issubset(set(reader.fieldnames or [])):
                raise ValueError(
                    f"conflicts.csv must contain columns {sorted(required)}. "
                    f"Found {reader.fieldnames}."
                )

            for row in reader:
                e1 = row["event1"].strip()
                e2 = row["event2"].strip()

                if e1 not in category:
                    raise ValueError(f"Conflict references unknown event: {e1}")
                if e2 not in category:
                    raise ValueError(f"Conflict references unknown event: {e2}")
                if e1 == e2:
                    raise ValueError(f"Conflict has same event twice: {e1}")

                conflicts.append((e1, e2))

    return I, C, category, cost, hours, benefit, conflicts


def load_constraints_config():
    """
    Beginner-friendly alternative to JSON:
    Just return constants from one place.

    If you want, you can edit these values slightly to see how your solution changes 
    (this is often called 'sensitivity analysis').
    """
    BUDGET = 2500
    HOURS_CAP = 90
    MAX_EVENTS = 6
    MIN_PER_CATEGORY = 1
    return BUDGET, HOURS_CAP, MAX_EVENTS, MIN_PER_CATEGORY