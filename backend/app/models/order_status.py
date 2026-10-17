from enum import StrEnum


class OrderStatus(StrEnum):
    PENDING   = "pending"
    READY     = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"