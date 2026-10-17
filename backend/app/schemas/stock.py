from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: int
    stock: int
    soldout: bool
