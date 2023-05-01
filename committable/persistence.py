import os
import json


class Persistence:
    def file_exists(file_path: str) -> bool:
        return os.path.exists(file_path)

    def get_count(count_path: str) -> int:
        try:
            with open(count_path) as nc:
                return int(nc.read())
        except OSError:
            return 1

    def update_count(count_path: str, new_count: str) -> str:
        error = ""
        try:
            with open(count_path, "w") as nc:
                nc.write(new_count)
        except OSError as ex:
            error += str(ex)
        return error

    def read(db_path: str) -> dict:
        try:
            with open(db_path) as iteration_storage:
                iteration_data = json.load(iteration_storage)
        except:
            iteration_data = None
        return iteration_data

    def write(db_path: str, iteration_data: dict) -> str:
        error = ""
        try:
            with open(db_path, "w") as iteration_storage:
                json.dump(iteration_data, iteration_storage, indent=2)
        except Exception as ex:
            error += str(ex)
        return error

    def remove(db_path: str) -> str:
        error = ""
        try:
            os.remove(db_path)
        except Exception as ex:
            error += str(ex)
        return error
