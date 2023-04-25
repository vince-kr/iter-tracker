import os

# Set up local persistence
persistence_dir_path = os.path.join(os.path.dirname(__file__), os.pardir, "persistence")
try:
    os.mkdir(persistence_dir_path)
except OSError:
    pass

# Ensure persistence/live.json exists
current_iteration_path = os.path.join(persistence_dir_path, "live.json")

# Ensure tests/test_live.json is referenced
test_iteration_path = os.path.join(
    os.path.dirname(__file__), os.pardir, "tests", "test_live.json"
)
