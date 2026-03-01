import pulp as pl
from utils.data_loader import load_event_data, load_constraints_config

# Load data
I, C, category, cost, hours, benefit, conflicts = load_event_data(
    "data/events.csv",
    "data/conflicts.csv"
)

# Load constraint constants (no JSON)
BUDGET, HOURS_CAP, MAX_EVENTS, MIN_PER_CATEGORY = load_constraints_config()

# Your code here...
# ...
# ...