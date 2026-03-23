from app.repositories.repository_interface import IRepository


class IFakeRepository(IRepository):
    def __init__(self, model_class):
        self.model = model_class
