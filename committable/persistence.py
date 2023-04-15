import json


class Persistence:
    def read(db_path: str) -> dict:
        with open(db_path) as iteration_storage:
            iteration_data = json.load(iteration_storage)
        return iteration_data

    def write(db_path: str, iteration_data: dict) -> str:
        error = ""
        try:
            with open(db_path, "w") as iteration_storage:
                json.dump(iteration_data, iteration_storage, indent=2)
        except Exception as ex:
            error += ex
        return error
