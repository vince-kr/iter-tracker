from . import iteration
import os

# Set up local persistence
path_to_persistence_dir = os.path.join(
    os.path.dirname(__file__), os.pardir, "persistence"
)
try:
    os.mkdir(path_to_persistence_dir)
except OSError:
    pass

get_context = iteration.get_context
