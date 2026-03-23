from app.repositories import IRepository


class IFakeRepository(IRepository):
    def __init__(self, model_class):
        self.model = model_class
