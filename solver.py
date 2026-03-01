import pulp as pl
from utils.data_loader import load_event_data, load_constraints_config

# Load data
I, C, category, cost, hours, benefit, conflicts = load_event_data(
    "data/events.csv",
    "data/conflicts.csv"
)

# Load constraint constants (no JSON)
BUDGET, HOURS_CAP, MAX_EVENTS, MIN_PER_CATEGORY = load_constraints_config()

# Model
model = pl.LpProblem("EventSelection", pl.LpMaximize)

# Decision variables
x = pl.LpVariable.dicts("x", I, lowBound=0, upBound=1, cat=pl.LpBinary)

# Objective
model += pl.lpSum((benefit[i] - cost[i]) * x[i] for i in I)

# Constraints
model += pl.lpSum(cost[i] * x[i] for i in I) <= BUDGET
model += pl.lpSum(hours[i] * x[i] for i in I) <= HOURS_CAP
model += pl.lpSum(x[i] for i in I) <= MAX_EVENTS

# Category coverage
for c in C:
    model += pl.lpSum(x[i] for i in I if category[i] == c) >= MIN_PER_CATEGORY

# Conflicts
for (i, j) in conflicts:
    model += x[i] + x[j] <= 1

# Solve
model.solve(pl.PULP_CBC_CMD(msg=False))

# Print chosen + objective
chosen = [i for i in I if pl.value(x[i]) > 0.5]
obj = pl.value(model.objective)

print("Chosen events:", chosen)
print("Total benefit (objective):", obj)