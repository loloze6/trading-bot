"""
Performance Tracker
==================
Tracks and analyzes trading performance metrics.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

logger = logging.getLogger("trading_bot.performance")

class Trade:
    """Represents a completed trade with entry and exit details."""
    
    def __init__(self, symbol: str, entry_price: float, entry_time: datetime,
                 exit_price: Optional[float] = None, exit_time: Optional[datetime] = None,
                 quantity: float = 0.0, trade_id: Optional[str] = None):
        """
        Initialize a trade.
        
        Args:
            symbol: Trading pair symbol
            entry_price: Entry price
            entry_time: Entry timestamp
            exit_price: Exit price (None for open trades)
            exit_time: Exit timestamp (None for open trades)
            quantity: Quantity traded
            trade_id: Unique identifier for the trade
        """
        self.symbol = symbol
        self.entry_price = entry_price
        self.entry_time = entry_time
        self.exit_price = exit_price
        self.exit_time = exit_time
        self.quantity = quantity
        self.trade_id = trade_id or f"{symbol}-{entry_time.strftime('%Y%m%d%H%M%S')}"
        
    @property
    def is_closed(self) -> bool:
        """Check if the trade is closed."""
        return self.exit_price is not None and self.exit_time is not None
    
    @property
    def duration(self) -> Optional[float]:
        """Calculate trade duration in seconds."""
        if not self.is_closed:
            return None
        return (self.exit_time - self.entry_time).total_seconds()
    
    @property
    def profit_loss(self) -> Optional[float]:
        """Calculate profit/loss in quote currency."""
        if not self.is_closed:
            return None
        return (self.exit_price - self.entry_price) * self.quantity
    
    @property
    def profit_loss_percent(self) -> Optional[float]:
        """Calculate profit/loss percentage."""
        if not self.is_closed:
            return None
        return ((self.exit_price / self.entry_price) - 1) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert trade to dictionary."""
        return {
            'trade_id': self.trade_id,
            'symbol': self.symbol,
            'entry_price': self.entry_price,
            'entry_time': self.entry_time.isoformat(),
            'exit_price': self.exit_price,
            'exit_time': self.exit_time.isoformat() if self.exit_time else None,
            'quantity': self.quantity,
            'is_closed': self.is_closed,
            'duration': self.duration,
            'profit_loss': self.profit_loss,
            'profit_loss_percent': self.profit_loss_percent
        }

class PerformanceTracker:
    """Tracks and analyzes trading performance."""
    
    def __init__(self, log_file: str = 'trades.json'):
        """
        Initialize the performance tracker.
        
        Args:
            log_file: Path to the trade log file
        """
        self.log_file = log_file
        self.trades: List[Trade] = []
        self.open_trades: Dict[str, Trade] = {}  # Symbol -> Trade mapping
        
        # Load existing trades if log file exists
        if os.path.exists(log_file):
            self.load_trades()
    
    def record_entry(self, symbol: str, price: float, quantity: float) -> str:
        """
        Record a trade entry.
        
        Args:
            symbol: Trading pair symbol
            price: Entry price
            quantity: Quantity traded
            
        Returns:
            Trade ID
        """
        trade = Trade(
            symbol=symbol,
            entry_price=price,
            entry_time=datetime.now(),
            quantity=quantity
        )
        
        # Add to open trades
        self.open_trades[symbol] = trade
        logger.info(f"Recorded entry for {symbol}: {quantity} at {price}")
        
        return trade.trade_id
    
    def record_exit(self, symbol: str, price: float) -> Optional[Trade]:
        """
        Record a trade exit.
        
        Args:
            symbol: Trading pair symbol
            price: Exit price
            
        Returns:
            Completed trade or None if no open trade for the symbol
        """
        if symbol not in self.open_trades:
            logger.warning(f"No open trade found for {symbol}")
            return None
        
        # Get the open trade
        trade = self.open_trades[symbol]
        
        # Complete the trade
        trade.exit_price = price
        trade.exit_time = datetime.now()
        
        # Move from open trades to completed trades
        del self.open_trades[symbol]
        self.trades.append(trade)
        
        # Log trade details
        logger.info(f"Recorded exit for {symbol} at {price}")
        logger.info(f"Trade result: {trade.profit_loss_percent:.2f}% profit/loss")
        
        # Save trades to log
        self.save_trades()
        
        return trade
    
    def load_trades(self) -> None:
        """Load trades from log file."""
        try:
            with open(self.log_file, 'r') as f:
                trade_dicts = json.load(f)
            
            for trade_dict in trade_dicts:
                trade = Trade(
                    symbol=trade_dict['symbol'],
                    entry_price=trade_dict['entry_price'],
                    entry_time=datetime.fromisoformat(trade_dict['entry_time']),
                    exit_price=trade_dict.get('exit_price'),
                    exit_time=datetime.fromisoformat(trade_dict['exit_time']) if trade_dict.get('exit_time') else None,
                    quantity=trade_dict['quantity'],
                    trade_id=trade_dict['trade_id']
                )
                
                if trade.is_closed:
                    self.trades.append(trade)
                else:
                    self.open_trades[trade.symbol] = trade
            
            logger.info(f"Loaded {len(self.trades)} completed trades and {len(self.open_trades)} open trades")
        
        except Exception as e:
            logger.error(f"Error loading trades: {e}")
    
    def save_trades(self) -> None:
        """Save trades to log file."""
        try:
            all_trades = self.trades + list(self.open_trades.values())
            trade_dicts = [trade.to_dict() for trade in all_trades]
            
            with open(self.log_file, 'w') as f:
                json.dump(trade_dicts, f, indent=4)
            
            logger.info(f"Saved {len(trade_dicts)} trades to {self.log_file}")
        
        except Exception as e:
            logger.error(f"Error saving trades: {e}")
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Calculate performance metrics for closed trades.
        
        Returns:
            Dictionary of performance metrics
        """
        # Return early if no closed trades
        if not self.trades:
            return {
                'total_trades': 0,
                'profitable_trades': 0,
                'win_rate': 0.0,
                'avg_profit_loss': 0.0,
                'max_profit': 0.0,
                'max_loss': 0.0,
                'total_profit_loss': 0.0,
                'sharpe_ratio': 0.0,
                'avg_trade_duration': 0.0
            }
        
        # Get profit/loss values
        profits = [trade.profit_loss for trade in self.trades]
        profit_percentages = [trade.profit_loss_percent for trade in self.trades]
        durations = [trade.duration for trade in self.trades]
        
        # Count profitable trades
        profitable_trades = sum(1 for p in profits if p > 0)
        
        # Calculate metrics
        metrics = {
            'total_trades': len(self.trades),
            'profitable_trades': profitable_trades,
            'win_rate': profitable_trades / len(self.trades) * 100,
            'avg_profit_loss': sum(profit_percentages) / len(profit_percentages),
            'max_profit': max(profit_percentages),
            'max_loss': min(profit_percentages),
            'total_profit_loss': sum(profit_percentages),
            'sharpe_ratio': self._calculate_sharpe_ratio(profit_percentages),
            'avg_trade_duration': sum(durations) / len(durations) if durations else 0
        }
        
        return metrics
    
    def _calculate_sharpe_ratio(self, returns: List[float], risk_free_rate: float = 0.0) -> float:
        """
        Calculate the Sharpe ratio.
        
        Args:
            returns: List of percentage returns
            risk_free_rate: Risk-free rate of return
            
        Returns:
            Sharpe ratio
        """
        if not returns:
            return 0.0
        
        mean_return = sum(returns) / len(returns)
        std_dev = (sum((r - mean_return) ** 2 for r in returns) / len(returns)) ** 0.5
        
        if std_dev == 0:
            return 0.0
        
        return (mean_return - risk_free_rate) / std_dev
    
    def get_equity_curve(self) -> pd.DataFrame:
        """
        Generate equity curve data.
        
        Returns:
            DataFrame with equity curve data
        """
        if not self.trades:
            return pd.DataFrame(columns=['timestamp', 'equity'])
        
        # Sort trades by exit time
        sorted_trades = sorted(self.trades, key=lambda t: t.exit_time)
        
        # Generate equity curve
        curve_data = []
        cumulative_return = 100.0  # Start with 100 units
        
        for trade in sorted_trades:
            # Apply the trade profit/loss to the equity
            cumulative_return *= (1 + trade.profit_loss_percent / 100)
            curve_data.append({
                'timestamp': trade.exit_time,
                'equity': cumulative_return
            })
        
        return pd.DataFrame(curve_data)
    
    def generate_report(self, output_file: str = 'performance_report.html') -> None:
        """
        Generate a performance report.
        
        Args:
            output_file: Path to save the HTML report
        """
        try:
            # Get metrics
            metrics = self.get_performance_metrics()
            equity_curve = self.get_equity_curve()
            
            # Create HTML report
            html = """
            <html>
            <head>
                <title>Trading Bot Performance Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    .container { max-width: 1200px; margin: 0 auto; }
                    .metrics { display: flex; flex-wrap: wrap; }
                    .metric-card { 
                        background-color: #f9f9f9; 
                        border-radius: 8px; 
                        padding: 15px; 
                        margin: 10px; 
                        width: 200px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }
                    .metric-value { font-size: 24px; font-weight: bold; }
                    .metric-label { color: #666; }
                    h1, h2 { color: #333; }
                    table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                    th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
                    th { background-color: #f2f2f2; }
                    tr:hover { background-color: #f5f5f5; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Trading Bot Performance Report</h1>
                    <p>Generated on {date}</p>
                    
                    <h2>Performance Metrics</h2>
                    <div class="metrics">
                        <div class="metric-card">
                            <div class="metric-value">{total_trades}</div>
                            <div class="metric-label">Total Trades</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{win_rate:.2f}%</div>
                            <div class="metric-label">Win Rate</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{avg_profit:.2f}%</div>
                            <div class="metric-label">Avg. Profit/Loss</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{total_profit:.2f}%</div>
                            <div class="metric-label">Total Profit/Loss</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{sharpe:.2f}</div>
                            <div class="metric-label">Sharpe Ratio</div>
                        </div>
                    </div>
                    
                    <h2>Recent Trades</h2>
                    <table>
                        <tr>
                            <th>Symbol</th>
                            <th>Entry Time</th>
                            <th>Exit Time</th>
                            <th>Entry Price</th>
                            <th>Exit Price</th>
                            <th>Quantity</th>
                            <th>P/L %</th>
                        </tr>
                        {trade_rows}
                    </table>
                </div>
            </body>
            </html>
            """.format(
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                total_trades=metrics['total_trades'],
                win_rate=metrics['win_rate'],
                avg_profit=metrics['avg_profit_loss'],
                total_profit=metrics['total_profit_loss'],
                sharpe=metrics['sharpe_ratio'],
                trade_rows=self._generate_trade_table_rows()
            )
            
            # Save to file
            with open(output_file, 'w') as f:
                f.write(html)
            
            logger.info(f"Performance report saved to {output_file}")
        
        except Exception as e:
            logger.error(f"Error generating performance report: {e}")
    
    def _generate_trade_table_rows(self) -> str:
        """Generate HTML table rows for trades."""
        rows = []
        
        # Get the 10 most recent trades
        recent_trades = sorted(self.trades, key=lambda t: t.exit_time, reverse=True)[:10]
        
        for trade in recent_trades:
            row = f"""
            <tr>
                <td>{trade.symbol}</td>
                <td>{trade.entry_time.strftime("%Y-%m-%d %H:%M")}</td>
                <td>{trade.exit_time.strftime("%Y-%m-%d %H:%M")}</td>
                <td>{trade.entry_price:.2f}</td>
                <td>{trade.exit_price:.2f}</td>
                <td>{trade.quantity:.4f}</td>
                <td>{trade.profit_loss_percent:.2f}%</td>
            </tr>
            """
            rows.append(row)
        
        return "".join(rows)