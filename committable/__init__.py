from .committable import current_iteration_path, test_iteration_path, Iteration
from .persistence import Persistence


def get_context(template_fields: tuple, testing=False) -> dict:
    if testing:
        persistence_path = test_iteration_path
    else:
        persistence_path = current_iteration_path
    iteration_data = Persistence.read(persistence_path)
    if not iteration_data:
        return {}
    iteration = Iteration(**iteration_data)
    return {field_name: iteration[field_name] for field_name in template_fields}


def record_study_session(session_data: dict) -> str:
    current_iteration = Persistence.read(current_iteration_path)
    current_iteration["study_sessions"].append(session_data)
    error = Persistence.write(current_iteration_path, current_iteration)
    return error


def open_new_iteration(iteration_data: dict) -> None:
    pass


def close_current_iteration(review_data: dict) -> tuple[str, str]:
    current_iteration = Persistence.read(current_iteration_path)
    current_iteration["review"] = review_data
    new_path = current_iteration_path.replace("live", str(current_iteration["count"]))
    error_remove_current = Persistence.remove(current_iteration_path)
    error_write_new = Persistence.write(new_path, current_iteration)
    return error_remove_current, error_write_new
