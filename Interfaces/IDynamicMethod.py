from abc import ABC


class IDynamicMethod(ABC):
    def update(self, list_of_geometry_obstacles):
        raise NotImplementedError

    def get_updated_path(self):
        raise NotImplementedError
