from typing import Tuple
from flask import jsonify, request


class BaseService:
    def __init__(self, controller):
        self.controller = controller

    def create(self) -> Tuple[dict, int]:
        query, error = self.controller.create(request.json)
        return self.service(query, error, is_read=False)

    def update(self) -> Tuple[dict, int]:
        query, error = self.controller.update(request.json)
        return self.service(query, error, is_read=False)

    def get_by_id(self, _id: int) -> Tuple[dict, int]:
        query, error = self.controller.get_by_id(_id)
        return self.service(query, error)

    def get_all(self) -> Tuple[dict, int]:
        querys, error = self.controller.get_all()
        return self.service(querys, error)

    def generate(self) -> Tuple[dict, int]:
        querys, error = self.controller.generate()
        return self.service(querys, error)

    @staticmethod
    def service(query, error, is_read: bool = True) -> Tuple[dict, int]:
        response = query if not error else {'error': error}
        if is_read:
            status_code = 200 if query else 404 if not error else 400
        else:
            status_code = 200 if not error else 400
        return jsonify(response), status_code
