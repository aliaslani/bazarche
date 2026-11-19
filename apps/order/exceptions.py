from apps.core.exceptions import ApplicationError


class OrderError(ApplicationError):
    "Base Class for order-domain erros"

class EmptyOrderError(OrderError):
    pass

class OrderStatusError(OrderError):
    pass