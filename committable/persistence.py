import os
import json


class Persistence:
    def file_exists(file_path: str) -> bool:
        return os.path.exists(file_path)

    def get_next_count(dir_path: str) -> int:
        current_files = os.listdir(dir_path)
        highest = 0
        for file in current_files:
            count = int(file.split(".")[0])
            if count > highest:
                highest = count
        return highest + 1

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
