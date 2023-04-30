from .committable import persistence_dir_path, current_iteration_path, test_iteration_path, Iteration
from .persistence import Persistence


def live_iteration_exists() -> bool:
    return Persistence.file_exists(current_iteration_path)


def get_context(template_fields: tuple, testing=False) -> dict:
    if testing:
        persistence_path = test_iteration_path
    else:
        persistence_path = current_iteration_path
    iteration_data = Persistence.read(persistence_path)
    iteration = Iteration(**iteration_data)
    return {field_name: iteration[field_name] for field_name in template_fields}


def record_study_session(session_data: dict) -> str:
    current_iteration = Persistence.read(current_iteration_path)
    current_iteration["study_sessions"].append(session_data)
    error = Persistence.write(current_iteration_path, current_iteration)
    return error


def start_new_iteration(start_and_goals: dict) -> str:
    iteration_data = {
        "count": Persistence.get_next_count(persistence_dir_path),
        "start_date": start_and_goals["start_date"],
        "learning": {
            "description": start_and_goals["learning_desc"],
            "target_in_minutes": _get_target_time(start_and_goals["learning_target"]),
        },
        "building": {
            "description": start_and_goals["building_desc"],
            "target_in_minutes": _get_target_time(start_and_goals["building_target"]),
        },
        "study_sessions": [],
    }
    error = Persistence.write(current_iteration_path, iteration_data)
    return error


def _get_target_time(target_time: str) -> int:
    hrs, mins = target_time.split(":")
    return int(hrs) * 60 + int(mins)


def close_current_iteration(review_data: dict) -> tuple[str, str]:
    current_iteration = Persistence.read(current_iteration_path)
    current_iteration["review"] = review_data
    new_path = current_iteration_path.replace("live", str(current_iteration["count"]))
    error_remove_current = Persistence.remove(current_iteration_path)
    error_write_new = Persistence.write(new_path, current_iteration)
    return error_remove_current, error_write_new
