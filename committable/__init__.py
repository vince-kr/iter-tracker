from .committable import (
    persistence_dir_path,
    live_iteration_path,
    test_iteration_path,
    count_path,
    Iteration,
)
from .persistence import Persistence


def live_iteration_exists() -> bool:
    return Persistence.file_exists(live_iteration_path)


def get_context(template_fields: tuple, testing: bool = False) -> dict:
    if testing:
        persistence_path = test_iteration_path
    else:
        persistence_path = live_iteration_path
    iteration_data = Persistence.read(persistence_path)
    iteration = Iteration(**iteration_data)
    return {field_name: iteration[field_name] for field_name in template_fields}


def record_study_session(session_data: dict, testing: bool = False) -> str:
    if testing:
        persistence_path = test_iteration_path
    else:
        persistence_path = live_iteration_path
    iteration_data = Persistence.read(persistence_path)
    iteration = Iteration(**iteration_data)
    if iteration.session_out_of_daterange(session_data):
        return "Session date is out of range for this iteration"
    iteration_data["study_sessions"].append(session_data)
    error = Persistence.write(live_iteration_path, iteration_data)
    return error


def start_new_iteration(start_and_goals: dict) -> str:
    iteration_data = {
        "count": Persistence.get_count(persistence_dir_path),
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
    error = Persistence.write(live_iteration_path, iteration_data)
    return error


def _get_target_time(target_time: str) -> int:
    hrs, mins = target_time.split(":")
    return int(hrs) * 60 + int(mins)


def close_current_iteration(review_data: dict) -> tuple[str, str, str]:
    current_iteration = Persistence.read(live_iteration_path)
    current_iteration["review"] = review_data
    new_path = live_iteration_path.replace("live", str(current_iteration["count"]))
    error_update_count = Persistence.update_count(
        persistence_dir_path, str(current_iteration["count"])
    )
    error_remove_current = Persistence.remove(live_iteration_path)
    error_write_new = Persistence.write(new_path, current_iteration)
    return error_update_count, error_remove_current, error_write_new
