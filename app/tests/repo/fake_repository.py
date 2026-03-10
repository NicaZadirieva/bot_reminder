from app.domain.interfaces import IRepository


class IFakeRepository(IRepository):
    def __init__(self, model_class):
        self.model = model_class
