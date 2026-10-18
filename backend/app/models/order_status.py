from enum import StrEnum


class OrderStatus(StrEnum):
    PENDING   = "pending"
    READY     = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    def can_transition_to(self, target: "OrderStatus") -> bool:
        _transitions = {
            OrderStatus.PENDING: {OrderStatus.READY, OrderStatus.CANCELLED},
            OrderStatus.READY: {OrderStatus.COMPLETED, OrderStatus.CANCELLED},
            OrderStatus.COMPLETED: set(),
            OrderStatus.CANCELLED: set(),
        }
        allowed = _transitions.get(self, set())
        return target in allowed