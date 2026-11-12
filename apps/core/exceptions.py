class ApplicationError(Exception):
    def __init__(self, message:str, extra:dict | None = None):
        super().__init__(message)
        self.message = message
        self.extra = extra

class OutOfStockError(ApplicationError):
    pass

class EmptyOrderError(ApplicationError):
    pass

class InsufficientStockError(ApplicationError):
    def __init__(self, product_name:str, available: int):
        self.product_name = product_name
        self.available = available
        super().__init__(f"Only {self.avaialable} of {self.product_name} left in stock.")





