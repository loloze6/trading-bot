from enum import Enum
from typing import Optional, Dict, Any
from time import time


class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"


class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"


class OrderStatus(Enum):
    OPEN = "open"
    FILLED = "filled"
    CANCELED = "canceled"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Order:
    """Represents a trading order."""

    def __init__(
        self, symbol: str, order_type: OrderType, side: OrderSide, amount: float, price: Optional[float] = None
    ):
        """
        Initialize an order.

        Args:
            symbol: Trading symbol (e.g., 'BTC/USD').
            order_type: Type of order.
            side: Buy or sell.
            amount: Amount to buy or sell.
            price: Price for limit orders (None for market orders).
        """
        self.symbol = symbol
        self.order_type = order_type
        self.side = side
        self.amount = amount
        self.price = price
        self.status = OrderStatus.OPEN
        self.created_at = time.time()
        self.executed_at = None
        self.exchange_id = None
        self.average_execution_price = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the order to a dictionary."""
        return {
            "symbol": self.symbol,
            "order_type": self.order_type.value,
            "side": self.side.value,
            "amount": self.amount,
            "price": self.price,
            "status": self.status.value,
            "created_at": self.created_at,
            "executed_at": self.executed_at,
            "exchange_id": self.exchange_id,
            "average_execution_price": self.average_execution_price,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Order":
        """Create an order from a dictionary."""
        order = cls(
            symbol=data["symbol"],
            order_type=OrderType(data["order_type"]),
            side=OrderSide(data["side"]),
            amount=data["amount"],
            price=data.get("price"),
        )
        order.status = OrderStatus(data["status"])
        order.created_at = data["created_at"]
        order.executed_at = data.get("executed_at")
        order.exchange_id = data.get("exchange_id")
        order.average_execution_price = data.get("average_execution_price")
        return order
