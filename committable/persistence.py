import os
import json


class Persistence:
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
