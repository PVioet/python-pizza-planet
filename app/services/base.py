from typing import Tuple
from flask import jsonify, request


class BaseService:
    def __init__(self, controller):
        self.controller = controller
        self.writers = ('create', 'update')
        self.readers = ('get_by_id', 'get_all', 'generate')

    def __getattr__(self, method_name):
        def wrapper(*args, **kwargs):
            if method_name in self.readers:
                query, error = getattr(self.controller, method_name)(*args, **kwargs)
                return self.read_service(query, error)
            elif method_name in self.writers:
                query, error = getattr(self.controller, method_name)(request.json)
                return self.write_service(query, error)
            else:
                return jsonify({'error': 'Method not found'}), 404
        return wrapper

    @staticmethod
    def read_service(query, error) -> Tuple[dict, int]:
        response = query if not error else {'error': error}
        status_code = 200 if query else 404 if not error else 400
        return jsonify(response), status_code

    @staticmethod
    def write_service(query, error) -> Tuple[dict, int]:
        response = query if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code
