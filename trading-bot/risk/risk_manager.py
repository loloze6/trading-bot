import time

class RiskManager:
    def __init__(self, max_trades_per_hour=10, max_position_size: float = 0.1, stop_loss_pct: float = 0.05):
        self.max_trades_per_hour = max_trades_per_hour
        self.trade_timestamps = []

        """
        Initialize risk manager.
        
        Args:
            max_position_size: Maximum position size as fraction of portfolio (0.1 = 10%)
            stop_loss_pct: Stop loss percentage (0.05 = 5%)
        """
        self.max_position_size = max_position_size
        self.stop_loss_pct = stop_loss_pct


    def approve_trade(self, action, price):
        if action == 'hold':
            return False

        now = time.time()
        self.trade_timestamps = [t for t in self.trade_timestamps if now - t < 3600]

        if len(self.trade_timestamps) >= self.max_trades_per_hour:
            return False

        self.trade_timestamps.append(now)
        return True

    def calculate_position_size(self, account_balance: float, 
                               asset_price: float, signal_strength: float = 1.0) -> float:
        """
        Calculate position size based on risk parameters.
        
        Args:
            account_balance: Available balance in quote currency
            asset_price: Current price of the asset
            signal_strength: Strength of the trading signal (0.0-1.0)
            
        Returns:
            Quantity to buy/sell
        """
        max_amount = account_balance * self.max_position_size * signal_strength
        quantity = max_amount / asset_price
        return quantity
    
    def calculate_stop_loss(self, entry_price: float, position_type: str) -> float:
        """
        Calculate stop loss price.
        
        Args:
            entry_price: The entry price of the position
            position_type: 'LONG' or 'SHORT'
            
        Returns:
            Stop loss price
        """
        if position_type == 'LONG':
            return entry_price * (1 - self.stop_loss_pct)
        else:  # SHORT
            return entry_price * (1 + self.stop_loss_pct)