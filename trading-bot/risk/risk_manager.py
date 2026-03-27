import time
import logging
from typing import Any, Dict, List, Optional, Union, Tuple

logger = logging.getLogger("trading_bot")

"""
Risk Management Module
======================
Controls position sizing, allocation limits, and trade approval.

Classes:
    - RiskManager: Live risk management with trade frequency limits
    - MockRiskManager: Simplified risk checks for backtesting
"""

class RiskManager:
    """
    Risk manager for live trading.
    
    Features:
        - Limits position sizes as % of portfolio
        - Enforces max trades per hour
        - Calculates dynamic stop losses
        - Validates allocation changes
    """

    def __init__(self, max_trades_per_hour=10, max_position_size: float = 0.1, stop_loss_pct: float = 0.05):
        self.max_trades_per_hour = max_trades_per_hour
        self.trade_timestamps = []

        """
        Initialize risk manager.
        
        Args:
            max_position_size: Maximum position size as fraction of portfolio (0.1 = 10%)
            stop_loss_pct: Stop loss percentage (0.05 = 5%)
        """
        self.max_position_size = max_position_size #10%
        self.stop_loss_pct = stop_loss_pct
        self.max_total_exposure = 1  # 100% max total exposure

    def approve_allocation_change(self, symbol: str, allocation_change: float, data: Dict) -> bool:
        """
        Approve or reject allocation changes based on risk parameters.
        
        Args:
            symbol: Trading symbol
            allocation_change: Proposed allocation change
            data: Market data
            
        Returns:
            True if approved, False if rejected
        """
        # Check if new allocation exceeds maximum position size
        if abs(allocation_change) > self.max_position_size:
            logger.warning(f"RISK MANANGER - Allocation change {allocation_change:.3f} exceeds max position size "
                         f"{self.max_position_size} for {symbol}")
            return False
        
        # Add more risk checks here (volatility, correlation, etc.)
        
        return True

    def approve_trade(self, action, data):
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
        

class MockRiskManager:
    """
    Simplified risk manager for backtesting.
    
    Approves all trades but enforces position size limits.
    """
    
    def __init__(self, max_position_size: float = 0.1, stop_loss_pct: float = 0.05):
        """
        Initialize the mock risk manager.
        
        Args:
            max_position_size: Maximum position size as fraction of account balance
            stop_loss_pct: Stop loss percentage
        """
        self.max_position_size = max_position_size
        self.stop_loss_pct = stop_loss_pct

    def approve_allocation_change(self, symbol: str, allocation_change: float, data: Dict) -> bool:
        """
        Approve or reject allocation changes based on risk parameters.
        
        Args:
            symbol: Trading symbol
            allocation_change: Proposed allocation change
            data: Market data
            
        Returns:
            True if approved, False if rejected
        """
        # Check if new allocation exceeds maximum position size
        if abs(allocation_change) > self.max_position_size:
            logger.warning(f"RISK MANANGER - Allocation change {allocation_change:.3f} exceeds max position size "
                         f"{self.max_position_size} for {symbol}")
            return False
        
        # Add more risk checks here (volatility, correlation, etc.)
        
        return True
    

    def approve_trade(self, action: str, price: float) -> bool:
        """
        Approve or reject a trade.
        
        Args:
            action: Trade action ('BUY' or 'CLOSE')
            price: Current price
            
        Returns:
            True if trade is approved, False otherwise
        """
        # In backtesting, we approve all trades
        return True
    
    # def calculate_position_size(self, available_balance: float, price: float) -> float:
    #     """
    #     Calculate position size for a trade.
        
    #     Args:
    #         available_balance: Available balance
    #         price: Current price
            
    #     Returns:
    #         Position size
    #     """
    #     return (available_balance * self.max_position_size) / price

    def calculate_position_size(self, available_balance: float, price: float, 
                              target_allocation: float) -> float:
        """Calculate position size based on target allocation."""
        target_value = available_balance * abs(target_allocation)
        return target_value / price    
    
    # def calculate_stop_loss(self, price: float, position_type: str) -> float:
    #     """
    #     Calculate stop loss price.
        
    #     Args:
    #         price: Entry price
    #         position_type: 'LONG' or 'SHORT'
            
    #     Returns:
    #         Stop loss price
    #     """
    #     if position_type == 'LONG':
    #         return price * (1 - self.stop_loss_pct)
    #     else:
    #         return price * (1 + self.stop_loss_pct)

    def calculate_stop_loss(self, price: float, position_type: str, 
                          allocation: float) -> float:
        """Calculate stop loss based on allocation size."""
        # Tighter stops for larger allocations
        stop_distance = 0.02 + (abs(allocation) * 0.03)  # 2-5% based on allocation
        
        if position_type == 'LONG':
            return price * (1 - stop_distance)
        else:  # SHORT
            return price * (1 + stop_distance)