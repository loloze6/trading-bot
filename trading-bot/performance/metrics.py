"""
Performance Tracker
==================
Tracks and analyzes trading performance metrics.
"""

from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from matplotlib.figure import Figure

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import numpy as np
import json
import os
import logging
from dataclasses import dataclass
from enum import Enum
import openpyxl
from openpyxl.styles import Font, PatternFill
from openpyxl.comments import Comment

from performance.forecast_analyzer import ForecastAnalyzer


from hmmlearn.hmm import GaussianHMM
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger("trading_bot")


class PositionSide(Enum):
    LONG = "LONG"
    SHORT = "SHORT"

@dataclass
class TradeExecution:
    """Represents a single trade execution (part of a larger position)."""
    symbol: str
    price: float
    quantity: float  # Positive for long, negative for short
    timestamp: datetime
    execution_id: str
    commission_rate: float = 0.001  # Default commission rate (0.1%)
    forecast: Optional[float] = None  # Optional forecast value for the execution
    regime: Optional[str] = None  # Regime in place
    confidence: Optional[float] = None  # Confidence of forecast
    debug_info: Optional[Dict[str, Any]] = None  # Additional debug information
    total_portfolio_value: Optional[float] = None
    
    @property
    def side(self) -> PositionSide:
        return PositionSide.LONG if self.quantity > 0 else PositionSide.SHORT

    @property
    def quantity_postComm(self) -> float:
        return self.quantity * (1 - self.commission_rate)

    @property
    def abs_quantity(self) -> float:
        return abs(self.quantity_postComm)

class Position:
    """Represents an open position that can be built up over multiple executions."""
    
    def __init__(self, symbol: str, initial_execution: TradeExecution):
        self.symbol = symbol
        self.executions: List[TradeExecution] = [initial_execution]
        self.closed_trades: List['CompletedTrade'] = []
        
    @property
    def total_quantity(self) -> float:
        """Net quantity of the position (can be positive or negative)."""
        return sum(exec.quantity_postComm for exec in self.executions)
    
    @property
    def is_closed(self) -> bool:
        """Check if position is completely closed."""
        return abs(self.total_quantity) < 1e-8  # Account for floating point precision
    
    @property
    def side(self) -> Optional[PositionSide]:
        """Current position side."""
        if self.is_closed:
            return None
        return PositionSide.LONG if self.total_quantity > 0 else PositionSide.SHORT
    
    @property
    def avg_entry_price(self) -> float:
        """Calculate average entry price for current open quantity."""
        if self.is_closed:
            return 0.0
        
        # Calculate weighted average price for remaining quantity
        total_value = 0.0
        total_qty = 0.0
        
        for exec in self.executions:
            # Only count executions that contribute to current position direction
            if np.sign(exec.quantity) == np.sign(self.total_quantity):
                total_value += exec.price * exec.abs_quantity
                total_qty += exec.abs_quantity
        
        return total_value / total_qty if total_qty > 0 else 0.0
    
    def add_execution(self, execution: TradeExecution):
        """Add a new execution to the position."""
        self.executions.append(execution)

class CompletedTrade:
    """Represents a completed trade with entry and exit details."""
    
    def __init__(self, entry_exec: TradeExecution, exit_exec: TradeExecution, 
                 matched_quantity: float, trade_id: Optional[str] = None):
        self.entry_execution = entry_exec
        self.exit_execution = exit_exec
        self.matched_quantity = matched_quantity  # Always positive
        self.trade_id = trade_id or f"{entry_exec.symbol}-{entry_exec.timestamp}-{exit_exec.timestamp}"


    @property
    def symbol(self) -> str:
        return self.entry_execution.symbol
    
    @property
    def entry_price(self) -> float:
        return self.entry_execution.price
    
    @property
    def exit_price(self) -> float:
        return self.exit_execution.price
    
    @property
    def entry_time(self) -> datetime:
        return self.entry_execution.timestamp
    
    @property
    def exit_time(self) -> datetime:
        return self.exit_execution.timestamp
    
    @property
    def duration_minutes(self) -> float:
        return (self.exit_time - self.entry_time).total_seconds() / 60
    
    @property
    def side(self) -> PositionSide:
        return self.entry_execution.side
    
    @property
    def profit_loss_percent(self) -> float:
        """Calculate profit/loss percentage without commission"""
        if self.side == PositionSide.LONG:
            return ((self.exit_price / self.entry_price) - 1) * 100
        else:  # SHORT
            return ((1 - self.exit_price / self.entry_price)) * 100
            # return ((self.entry_price / self.exit_price) - 1) * 100
    
    @property
    def profit_loss_absolute(self) -> float:
        """Calculate profit/loss amount without commission"""
        if self.side == PositionSide.LONG:
            # Long position: profit when exit > entry
            pnl = (self.exit_price - self.entry_price) * self.matched_quantity
        else:  # SHORT
            # Short position: profit when entry > exit  
            pnl = (self.entry_price - self.exit_price) * self.matched_quantity
        
        return pnl

    @property
    def entry_commission(self) -> float:
        """Calculate commission amount for the trade entry"""
        # return abs(self.matched_quantity) * self.entry_price * (self.entry_execution.commission_rate / (1-self.entry_execution.commission_rate))
        rate = self.entry_execution.commission_rate
        if self.side == PositionSide.LONG:
            # Buying base asset: Binance deducts fee from received asset
            return abs(self.matched_quantity) * self.entry_price * (rate / (1 - rate))
        else:
            # Selling base asset (Short entry): Fee taken from quote asset, standard math
            return abs(self.matched_quantity) * self.entry_price * rate
        
    @property
    def exit_commission(self) -> float:
        """Calculate commission amount for the trade exit"""
        # return abs(self.matched_quantity) * self.exit_price * self.exit_execution.commission_rate
        rate = self.exit_execution.commission_rate # Fixed: Now correctly uses exit_execution
        if self.side == PositionSide.LONG:
            # Selling base asset (Long exit): Fee taken from quote asset, standard math
            return abs(self.matched_quantity) * self.exit_price * rate
        else:
            # Buying base asset (Short exit): Binance deducts fee from received asset
            return abs(self.matched_quantity) * self.exit_price * (rate / (1 - rate))
    @property
    def total_commission(self) -> float:
        """Calculate total commission amount for this trade."""
        return self.entry_commission + self.exit_commission

    @property
    def total_commission_percent(self) -> float:
        """Calculate total commission percent for this trade."""
        return (self.entry_execution.commission_rate + self.exit_execution.commission_rate)*100
        
    @property
    def net_profit_loss_absolute(self) -> float:
        """Calculate profit/loss amount with commission"""
        return self.profit_loss_absolute - self.total_commission

    @property
    def net_profit_loss_percent(self) -> float:
        """Calculate profit/loss percent with commission"""
        return self.profit_loss_percent - self.entry_execution.commission_rate*100 - self.exit_price / self.entry_price * self.exit_execution.commission_rate*100

    @property
    def net_portfolio_profit_loss_percent(self) -> float:
        """Calculate profit/loss percent on the portfolio considering this trade (with commission)"""
        return self.net_profit_loss_absolute /self.initial_portfolio_value*100
        return self.net_profit_loss_percent * self.matched_quantity * self.entry_price / self.initial_portfolio_value
    @property
    def initial_portfolio_value(self) -> float:
        """Portfolio value before entering this trade"""
        return self.entry_execution.total_portfolio_value
    
    @property
    def final_portfolio_value(self) -> float:
        """Portfolio value after exiting this trade"""
        return self.exit_execution.total_portfolio_value

    @property
    def profitable_absolute(self) -> bool:
        """Check if the trade is profitable before commissions."""
        return self.profit_loss_percent > 0
    
    @property
    def profitable_net(self) -> bool:
        """Check if the trade is profitable after commissions."""
        return self.net_profit_loss_percent > 0

    @property
    def entry_forecast(self) -> float:
        return self.entry_execution.forecast

    @property
    def entry_regime(self) -> float:
        return self.entry_execution.regime
    
    @property
    def entry_confidence(self) -> float:
        return self.entry_execution.confidence

    @property
    def exit_forecast(self) -> float:
        return self.exit_execution.forecast

    @property
    def exit_regime(self) -> float:
        return self.exit_execution.regime
    
    @property
    def exit_confidence(self) -> float:
        return self.exit_execution.confidence

    @property
    def entry_debug_info(self) -> dict:
        return self.entry_execution.debug_info
     
    @property
    def exit_debug_info(self) -> dict:
        return self.exit_execution.debug_info
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert trade to dictionary."""
        return {
            'trade_id': self.trade_id,
            'symbol': self.symbol,
            'side': self.side.value,
            'entry_price': self.entry_price,
            'exit_price': self.exit_price,
            'entry_time': self.entry_time.isoformat(),
            'exit_time': self.exit_time.isoformat(),
            'matched_quantity': self.matched_quantity,
            'duration_minutes': self.duration_minutes,
            'profit_loss_percent': self.profit_loss_percent,
            'profit_loss_absolute': self.profit_loss_absolute,
            'entry_commission': self.entry_commission,
            'exit_commission': self.exit_commission,
            'total_commission': self.total_commission,
            'total_commission_percent': self.total_commission_percent,
            'net_profit_loss_absolute': self.net_profit_loss_absolute,
            'net_profit_loss_percent': self.net_profit_loss_percent,
            'net_portfolio_profit_loss_percent': self.net_portfolio_profit_loss_percent,
            'initial_portfolio_value': self.initial_portfolio_value,
            'final_portfolio_value': self.final_portfolio_value,
            'profitable_absolute': self.profitable_absolute,
            'profitable_net': self.profitable_net,
            'entry_forecast': self.entry_execution.forecast,
            'entry_regime': self.entry_execution.regime,
            'entry_confidence': self.entry_execution.confidence,
            'exit_forecast': self.exit_execution.forecast,
            'exit_regime': self.exit_execution.regime,
            'exit_confidence': self.exit_execution.confidence,
            'entry_debug_info': self.entry_execution.debug_info,
            'exit_debug_info': self.exit_execution.debug_info
        }

class EnhancedPerformanceTracker:
    """Enhanced performance tracker supporting iterative long/short positions with LIFO matching."""
    
    def __init__(self, commission_rate: float = 0.001, log_file: str = 'results/trades.json', initial_capital: float = 1000.0):
        self.commission_rate = commission_rate
        performance_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(performance_dir)
        self.log_file = os.path.join(project_dir, log_file)
        self.positions: Dict[str, Position] = {}  # symbol -> Position
        self.completed_trades: List[CompletedTrade] = []
        self.execution_counter = 0
        self.initial_capital = initial_capital  # NEW
        self.forecast_analyzer = ForecastAnalyzer(
       output_path="results/forecast_analysis.xlsx"
       )
        self.trade_regime_agreement = {}

        # Load existing trades if log file exists
        if os.path.exists(log_file):
            self.load_trades()
    
    def record_trade(self, symbol: str, price: float, quantity: float, 
                    timestamp: Optional[datetime] = None, signal: Optional[Dict] = None, total_portfolio_value: Optional[float] = None) -> List[CompletedTrade]:
        """
        Record a trade execution and process any resulting completed trades.
        
        Args:
            symbol: Trading pair symbol
            price: Execution price
            quantity: Quantity (positive for long, negative for short)
            timestamp: Execution timestamp
            
        Returns:
            List of completed trades resulting from this execution
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        forecast = signal.forecast if signal else None
        regime = signal.regime if signal else None
        confidence = signal.confidence if signal else None
        debug_info = signal.debug_info if signal else None

        # Create execution
        self.execution_counter += 1
        execution = TradeExecution(
            symbol=symbol,
            price=price,
            quantity=quantity,
            timestamp=timestamp,
            execution_id=f"{symbol}-{self.execution_counter}",
            commission_rate=self.commission_rate,
            forecast=forecast,
            regime=regime,
            confidence=confidence,
            debug_info=debug_info,
            total_portfolio_value=total_portfolio_value
        )
        

        # Optional logging part the execution
        side = "LONG" if quantity > 0 else "SHORT"
        is_new_position = symbol not in self.positions

        # Log execution header
        logger.debug(f"┌─── EXECUTION #{self.execution_counter} ───") 
        # logger.debug(f"│ {side} {symbol} │ Qty: {abs(quantity):.6f} @ ${price:.2f} │ Forecast: {forecast if forecast else 'N/A'}")

        # Process the execution
        completed_trades = self._process_executed_trades(execution)
        
        # 1/ Save trades (throttled: full rewrite every 100 closes to avoid O(n²) I/O)
        if completed_trades and len(self.completed_trades) % 100 == 0:
            self.save_trades()
        
        # 2/ Log results based on what happened
        if is_new_position and symbol in self.positions:
            logger.debug(f"│ ✓ OPENED new {side} position")

        elif completed_trades:
            total_pnl = sum(t.net_profit_loss_percent for t in completed_trades)
            wins = sum(1 for t in completed_trades if t.profitable_net)
            losses = len(completed_trades) - wins
            logger.debug(f"│ ✓ CLOSED {len(completed_trades)} trade(s) │ W/L: {wins}/{losses} │ Net P&L: {total_pnl:+.3f}%")
                       
            for i, trade in enumerate(completed_trades, 1):
                pnl_symbol = "📈" if trade.profitable_net else "📉"
                duration_str = f"{trade.duration_minutes:.0f}m" if trade.duration_minutes < 60 else f"{trade.duration_minutes/60:.1f}h"
                logger.debug(f"│   [{i}] {pnl_symbol} {trade.side.value} │ "
                          f"{trade.entry_price:.2f}→{trade.exit_price:.2f} │ "
                          f"P&L: {trade.net_profit_loss_percent:+.3f}% │ "
                          f"Duration: {duration_str}"
                          )

        elif symbol in self.positions:
            # Added to existing position
            pos = self.positions[symbol]
            logger.debug(f"│ ✓ ADDED to {pos.side.value} position │ "
                       f"Total Qty: {abs(pos.total_quantity):.6f} │ "
                       f"Avg Entry: ${pos.avg_entry_price:.2f} │ "
                       f"Executions: {len(pos.executions)}")

        # Show current position status
        if symbol in self.positions and not self.positions[symbol].is_closed:
            pos = self.positions[symbol]
            logger.debug(f"│ POSITION: {pos.side.value if pos.side else 'CLOSED'} {abs(pos.total_quantity):.6f} @ ${pos.avg_entry_price:.2f}")
        else:
            logger.debug(f"│ POSITION: FLAT (no open position)")
        
        logger.debug(f"└{'─' * 60}")


        
        return completed_trades
    
    def _process_executed_trades(self, execution: TradeExecution) -> List[CompletedTrade]: #For record_trade
        """Process an execution and match against existing positions using LIFO."""
        symbol = execution.symbol
        completed_trades = []
        
        # Get or create position
        if symbol not in self.positions:
            self.positions[symbol] = Position(symbol, execution)
            return completed_trades
        
        position = self.positions[symbol]
        current_net_position = position.total_quantity
        new_quantity = execution.quantity 
        
        # Case 1: Same direction (adding to position) - no matching needed
        if current_net_position == 0 or np.sign(current_net_position) == np.sign(new_quantity):
            position.add_execution(execution)
            return completed_trades
        
        # Case 2: Opposite direction - need to match against existing executions using LIFO
        remaining_to_close = abs(new_quantity)  # How much we need to close

        logger.debug(f"│ → Matching LIFO │ To Close: {remaining_to_close}")

        # Process existing executions in REVERSE chronological order (LIFO - Last In First Out)
        executions_to_remove = []
        matched_count = 0  # Track quantity changes separately
        
        # Go through executions from most recent to oldest
        for existing_exec in reversed(position.executions):
            if remaining_to_close == 0:
                break  # Fully matched
            elif remaining_to_close <= 1e-8:
                logger.warning(f"│   ⚠ Remaining to close is almost zero --> {remaining_to_close}, no LIFO launched")
                break
            
            if existing_exec.side == PositionSide.SHORT: 
                available_quantity = abs(existing_exec.quantity)
            elif existing_exec.side == PositionSide.LONG:
                available_quantity = abs(existing_exec.quantity_postComm)
            else:
                logger.warning(f"│ ⚠ Unexpected execution side")
                continue
            
            # Determine how much of this execution can be closed
            quantity_to_close = min(available_quantity, remaining_to_close)
            matched_count += 1
            logger.debug(f"│   Match #{matched_count}: {quantity_to_close:.6f} from {existing_exec.execution_id}")
            
            
            # Create a completed trade for this match
            # The existing execution is the "entry", the new execution is the "exit"
            # But we need to create a proper exit execution for the matched portion
            exit_exec_for_trade = TradeExecution(
                symbol=execution.symbol,
                price=execution.price,
                quantity=-existing_exec.quantity / abs(existing_exec.quantity) * quantity_to_close,  # Opposite sign, matched quantity
                timestamp=execution.timestamp,
                execution_id=f"{execution.execution_id}-exit-{quantity_to_close}",
                commission_rate=self.commission_rate,
                forecast=execution.forecast,
                regime=execution.regime,
                confidence=execution.confidence,                
                debug_info=execution.debug_info,
                total_portfolio_value=execution.total_portfolio_value
            )
            
            # Create a copy of the entry execution to preserve original quantity in the trade record
            entry_exec_for_trade = TradeExecution(
                symbol=existing_exec.symbol,
                price=existing_exec.price,
                quantity=existing_exec.quantity,
                timestamp=existing_exec.timestamp,
                execution_id=existing_exec.execution_id,
                # commission=existing_exec.commission,
                commission_rate=self.commission_rate,
                forecast=existing_exec.forecast,
                regime=existing_exec.regime,
                confidence=existing_exec.confidence,
                debug_info=existing_exec.debug_info,
                total_portfolio_value=existing_exec.total_portfolio_value
            )

            trade = CompletedTrade(
                entry_exec=entry_exec_for_trade,
                exit_exec=exit_exec_for_trade,
                matched_quantity=quantity_to_close
            )
            
            completed_trades.append(trade)
            self.completed_trades.append(trade)
            
            # Update remaining quantities
            remaining_to_close -= quantity_to_close
            if existing_exec.side == PositionSide.SHORT: 
                existing_exec.quantity -= np.sign(existing_exec.quantity) * quantity_to_close
            if existing_exec.side == PositionSide.LONG:
                existing_exec.quantity -= np.sign(existing_exec.quantity) * quantity_to_close / (1 - self.commission_rate)

            # Mark for removal if fully consumed
            if abs(existing_exec.quantity_postComm) < 1e-8:
                executions_to_remove.append(existing_exec)
                logger.debug(f"│   ✓ Fully closed: {existing_exec.execution_id}")
        
        # Remove fully consumed executions
        for exec_to_remove in executions_to_remove:
            position.executions.remove(exec_to_remove)
        
        # Case 3: Handle remaining quantity (position reversal)
        if remaining_to_close > 1e-8:
            # This means we had more closing quantity than open position
            # Create new execution for the reversal
            logger.warning(f"│ ⚠ REVERSAL │ New {execution.side.value} position: {remaining_to_close:.6f}")
            reversal_quantity = np.sign(new_quantity) * remaining_to_close
            
            reversal_execution = TradeExecution(
                symbol=execution.symbol,
                price=execution.price,
                quantity=reversal_quantity,
                timestamp=execution.timestamp,
                execution_id=f"{execution.execution_id}-reversal",
                commission_rate=self.commission_rate,
                forecast=execution.forecast,
                regime=execution.regime,
                confidence=execution.confidence,
                debug_info=execution.debug_info
            )
            position.add_execution(reversal_execution)
        
        # Clean up closed position
        if position.is_closed:
            del self.positions[symbol]
        
        return completed_trades
    
    def get_open_positions(self) -> Dict[str, Dict[str, Any]]: #For _close_all_positions_at_end (processed end of BT)
        """Get summary of all open positions."""
        positions_summary = {}
        
        for symbol, position in self.positions.items():
            if not position.is_closed:
                positions_summary[symbol] = {
                    'symbol': symbol,
                    'quantity': position.total_quantity,
                    'side': position.side.value if position.side else 'CLOSED',
                    'avg_entry_price': position.avg_entry_price,
                    'executions_count': len(position.executions)
                }
        
        return positions_summary
    
# Below save & load features for trades + Report generation

    def save_trades(self): #Dump all completed trades into a file in JSON format 
        """Save completed trades to JSON file."""
        try:
            trades_data = [trade.to_dict() for trade in self.completed_trades]
            with open(self.log_file, 'w') as f:
                json.dump(trades_data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving trades: {e}")

    def export_trades_to_excel(self, filepath: str): #Called end of BT to transform JSON into an excel of all completed trades
        self.save_trades()  # flush final state before reading — throttle may have skipped last batch
        with open(self.log_file, 'r') as f:
            data = json.load(f)

        df = pd.DataFrame(data) 
        performance_folder = os.path.dirname(os.path.abspath(__file__))
        project_folder = os.path.dirname(performance_folder)
        metric_path = os.path.join(project_folder, filepath)
        df.to_excel(metric_path, index=False)
    
    def load_trades(self): #Load trades  at init of PerformanceTracker (opt? to keep track of all trades across multiple backtests?)
        """Load trades from JSON file."""
        try:
            with open(self.log_file, 'r') as f:
                trades_data = json.load(f)
            
            # Note: This is a simplified load - in practice you'd want to reconstruct
            # the full CompletedTrade objects and potentially the position state
            logger.debug(f"Loaded {len(trades_data)} trades from {self.log_file}")
            
        except Exception as e:
            logger.error(f"Error loading trades: {e}")

    def export_metrics_to_excel(self, filepath: str, metrics: Dict[str, Any]) -> None: #Amend the excel with a new Tab with metrics
        """Export metrics to Excel with 'Performance_Metrics' sheet."""
        try:
            performance_folder = os.path.dirname(os.path.abspath(__file__))
            project_folder = os.path.dirname(performance_folder)
            metric_path = os.path.join(project_folder, filepath)
            wb = openpyxl.load_workbook(metric_path)
            if 'Performance_Metrics' in wb.sheetnames:
                wb.remove(wb['Performance_Metrics'])
            ws = wb.create_sheet('Performance_Metrics', 0)
            
            row = 1

            # Metric explanations
            metric_comments = {
                'net_win_rate_pct': 'Percentage of trades profitable after commissions. Target: >55% for mean reversion',
                'gross_win_rate_pct': 'Percentage of trades profitable before commissions',
                'net_profit_factor': 'Ratio of gross wins to losses (after fees). >1.5 indicates strong edge (Pardo 2012)',
                'gross_profit_factor': 'Profit factor before commissions',
                'expectancy_per_trade_usd': 'Expected profit per trade. Must be positive for long-term viability (Thorp 1998)',
                'commission_efficiency_pct': 'Net PnL / Gross PnL ratio. Target: >70%. Measures transaction cost impact',
                'avg_win_usd': 'Average profit of winning trades (after commissions)',
                'avg_loss_usd': 'Average loss of losing trades (after commissions)',
                'win_loss_ratio': 'Avg Win / Avg Loss. Target: >1.5 for mean reversion strategies',
                'total_gross_pnl_usd': 'Total profit before commissions',
                'total_net_pnl_usd': 'Total profit after commissions - actual P&L',
                'total_commission_usd': 'Total fees paid to exchange',
                'avg_duration_hours': 'Average time holding each trade',
                'avg_duration_minutes': 'Average holding period in minutes',
                'ranging' : 'Q1 2025: Low trend, balanced direction, high volatility. Strategy should profit here.',
                'trending' : 'Non-Q1 periods: Strong trends, directional bias. Strategy should avoid trading here.',
                'unknown' : 'Unknown regime: Insufficient data for classification',
                'accuracy_pct' : 'Percentage of trades where detected regime matches ground truth. Target: >90%',
                'false_positives' : 'Number of trades taken in TRENDING regimes (should be 0 for pure mean reversion)',
                'total_trades_analyzed' : 'Total number of completed trades used for regime validation'
            }
            
            
            # === TABLE 1: Overall Metrics ===
            label = 'OVERALL STRATEGY'
            description = 'All trades across all regimes and directions'
            ws, row = self._create_header_line(ws, row, label, description)

            for key, value in metrics.get('overall_metrics', {}).items():
                if not isinstance(value, (list, dict)):
                    row += 1
                    metric_cell = ws.cell(row, 1, key.replace('_', ' ').title())
                    value_cell = ws.cell(row, 2, value)
                    
                    # Add comment with explanation
                    if key in metric_comments:
                        comment = Comment(metric_comments[key], 'Trading Bot')
                        metric_cell.comment = comment
            
            
            # === TABLE 2: By Ground Truth Regime ===
            row += 2
            label = 'METRICS BY GROUND TRUTH REGIME'
            description = 'Performance during empirically validated market regimes (Q1 2025 = RANGING, others = TRENDING)'
            ws, row = self._create_header_line(ws, row, label, description)

            by_gt = metrics.get('by_ground_truth', {})
            if by_gt:
                ws, row = self._create_table_from_dict(ws, row, by_gt, metric_comments)
                
            
            # === TABLE 3: By Detected Regime ===
            row += 2
            label = 'METRICS BY DETECTED REGIME'
            description = 'Performance grouped by what RegimeDetector classified at trade entry'
            ws, row = self._create_header_line(ws, row, label, description)
            
            by_regime = metrics.get('by_regime', {})
            if by_regime:
                ws, row = self._create_table_from_dict(ws, row, by_regime, metric_comments)
  
            # === TABLE 4: By Direction ===
            row += 2
            label = 'METRICS BY DIRECTION (LONG vs SHORT)'
            description = 'Identifies directional asymmetries. Both sides should be profitable in mean reversion.'
            ws, row = self._create_header_line(ws, row, label, description)
            
            by_dir = metrics.get('by_direction', {})
            if by_dir:
                ws, row = self._create_table_from_dict(ws, row, by_dir, metric_comments)
        
            # === TABLE 5: Regime Validation ===
            row += 2
            label = 'REGIME CLASSIFICATION VALIDATION'
            description = 'Validates RegimeDetector accuracy by comparing detected vs ground truth regimes'
            ws, row = self._create_header_line(ws, row, label, description)

            for key, value in metrics.get('regime_validation', {}).items():
                if not isinstance(value, (list, dict)):
                    row += 1
                    metric_cell = ws.cell(row, 1, key.replace('_', ' ').title())
                    value_cell = ws.cell(row, 2, value)
                    
                    # Add comment with explanation
                    if key in metric_comments:
                        comment = Comment(metric_comments[key], 'Trading Bot')
                        metric_cell.comment = comment

            # === TABLE 6: Confusion matrix ===
            row += 2
            label = 'CONFUSION MATRIX FOR REGIME DETECTION'
            description = 'Shows detected regime (rows) vs actual ground truth regime (columns). Diagonal = correct classifications.'
            ws, row = self._create_header_line(ws, row, label, description)
            
            # Confusion matrix
            validation = metrics.get('regime_validation', {})
            confusion = validation.get('confusion_matrix', {})
            if confusion:
                ws, row = self._create_table_from_dict(ws, row, confusion, metric_comments)
               
            
            # Set fixed column widths
            ws.column_dimensions['A'].width = 40
            ws.column_dimensions['B'].width = 22
            ws.column_dimensions['C'].width = 22
            ws.column_dimensions['D'].width = 22
            
            wb.save(metric_path)
            logger.info(f"Metrics exported to {metric_path} (Performance_Metrics sheet with explanatory comments)")
        
           # Run forecast-centric analysis
            self.forecast_analyzer.analyze(self.completed_trades)
        
        except Exception as e:
            logger.error(f"Error exporting metrics: {e}")
            import traceback
            logger.error(traceback.format_exc())

    def _create_header_line(self, ws, row, label, comment=None):
        try:
            header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
            header_font = Font(bold=True, color='FFFFFF', size=12)
            ws.cell(row, 1, label).font = header_font
            ws.cell(row, 1).fill = header_fill
            ws.merge_cells(f'A{row}:B{row}')
            row += 1

            # Add description row
            if comment is not None:
                desc_cell = ws.cell(row, 1, comment)
                desc_cell.font = Font(italic=True, size=9)
                ws.merge_cells(f'A{row}:B{row}')
                row += 2
        except Exception as e:
            logger.error(f"Error exporting metrics: {e}")
            import traceback
            logger.error(traceback.format_exc())

        return ws, row

    def _create_table_from_dict(self, ws, row, data_dict, metric_comments):
        try:
            #Create table headers
            column_header_font = Font(bold=True, size=10)            
                #Add first column header
            ws.cell(row, 1, 'Metric').font = column_header_font
            col = 2
            for metric_split in data_dict.keys():
            #Add column header per metric split
                metric_cell = ws.cell(row, col, metric_split)
                metric_cell.font = column_header_font
                # Add comment on column header 
                if (metric_split in metric_comments):
                    comment = Comment(metric_comments[metric_split], 'Trading Bot')
                    metric_cell.comment = comment
                #Iterate
                col += 1
            
            #Create table content with a line per metric
            metric_keys = list(next(iter(data_dict.values())).keys())
            for metric_key in metric_keys:
                row += 1
                metric_cell = ws.cell(row, 1, metric_key.replace('_', ' ').title())
                    
                # Add comment into line label
                if metric_key in metric_comments:
                    comment = Comment(metric_comments[metric_key], 'Trading Bot')
                    metric_cell.comment = comment
                
                # Fill values for each column
                col = 2
                for column_header in data_dict.keys():
                    ws.cell(row, col, data_dict[column_header].get(metric_key, '-'))
                    col += 1     


        except Exception as e:
            logger.error(f"Error exporting metrics: {e}")
            import traceback
            logger.error(traceback.format_exc())

        return ws, row


# Below Extraction of trades And GroundTruth calculation 

    def get_performance_metrics(self, price_data: pd.DataFrame = None) -> Dict[str, Any]:
        """
        Calculate comprehensive performance metrics with regime validation.

        Args:
        price_data: Optional full OHLCV DataFrame for objective ground truth calculation
                   If None, uses fallback static periods
    
        
        TIER 1 METRICS (Critical):
        1. Regime Classification Accuracy - Validates detector
        2. Net Profit Factor - Edge validation (Pardo 2012)
        3. Commission Efficiency - Transaction cost impact
        4. Expectancy per Trade - Expected value (Thorp 1998)
        """
        if not self.completed_trades:
            return self._get_empty_metrics() # Return a structure with empty metrics if no trade completed
        
        # Convert completed trades to DataFrame
        trades_data = []
        for trade in self.completed_trades:
            # if trade.entry_debug_info and isinstance(trade.entry_debug_info, dict):
            #     detected_regime = trade.entry_debug_info.get('regime', 'UNKNOWN')
            # else: 
            #     detected_regime = 'UNKNOWN'
            trades_data.append({
                'entry_time': trade.entry_time,
                'exit_time': trade.exit_time,
                'side': trade.side.value,
                # We keep raw trade PnL % for trade-level analysis
                'gross_pnl_pct': trade.profit_loss_percent,
                'net_pnl_pct': trade.net_profit_loss_percent,
                # Portfolio impact
                'portfolio_impact_pct': trade.net_portfolio_profit_loss_percent,
                # Friction
                'commission': trade.total_commission,
                'commission_pct': trade.total_commission_percent,

                'profitable_absolute': trade.profitable_absolute,
                'profitable_net': trade.profitable_net,
                

                # Absolute Portfolio Values for True Return Calculation
                'initial_portfolio_value': trade.initial_portfolio_value,
                'final_portfolio_value': trade.final_portfolio_value,

                'duration_minutes': trade.duration_minutes,
                'profitable_net': trade.profitable_net,
                'detected_regime': trade.entry_regime,
                'forecast': trade.entry_forecast if hasattr(trade, 'entry_forecast') else None
 

                # 'gross_pnl': trade.profit_loss_absolute,
                # 'net_pnl': trade.net_profit_loss_absolute,
                # 'profitable_gross': trade.profitable_absolute,
           })
        df = pd.DataFrame(trades_data)
        #And convert times to datetime
        df['entry_time'] = pd.to_datetime(df['entry_time'])
        df['exit_time'] = pd.to_datetime(df['exit_time'])

        
        if price_data is not None:
            full_regimes, price_index = self.classify_full_history(price_data)

            df['ground_truth_regime'] = df['entry_time'].apply(
                lambda ts: self.regime_at_timestamp(ts, full_regimes, price_index)
            )


            self.plot_regime_chart(full_regimes, price_data)
        else:
            df['ground_truth_regime'] = 'UNKNOWN'       
        
        return {
            'overall_metrics': self._calculate_standard_metrics(df),
            'by_regime': self._calculate_by_regime_metrics(df, 'detected_regime'),
            'by_ground_truth': self._calculate_by_regime_metrics(df, 'ground_truth_regime'),
            'by_direction': self._calculate_by_direction_metrics(df),
            'regime_validation': self._calculate_regime_validation_metrics(df)
        }

    def classify_full_history(self, full_price_data: pd.DataFrame) -> Tuple[List[str], pd.Series]:
        logger.debug("Starting Locally Adaptive Heuristic...")
        
        df = full_price_data.copy().reset_index(drop=True)
        df['close'] = pd.to_numeric(df['close'], errors='coerce') 
        
        # Micro window (24 hours) for immediate price action
        N = 24  
        # Macro window (14 days = 336 hours) for the local baseline
        MACRO_W = 336 
        
        # ==========================================
        # 1. MICRO FEATURES (The immediate 24h wave)
        # ==========================================
        df['log_return'] = np.log(df['close'] / df['close'].shift(1))
        df['Centered_Return'] = df['log_return'].rolling(window=2*N+1, center=True, min_periods=1).mean() * 8760
        df['Centered_Volatility'] = df['log_return'].rolling(window=2*N+1, center=True, min_periods=1).std() * np.sqrt(8760)
        
        # ==========================================
        # 2. MACRO BASELINES (The 14-day local environment)
        # ==========================================
        # This completely fixes the "January warping March" bug.
        df['Macro_Vol_Baseline'] = df['Centered_Volatility'].rolling(window=MACRO_W, center=True, min_periods=1).median()
        df['Macro_Ret_Baseline'] = df['Centered_Return'].abs().rolling(window=MACRO_W, center=True, min_periods=1).median()
        
        # ==========================================
        # 3. ADAPTIVE TAXONOMY MAPPING
        # ==========================================
        def map_adaptive_regime(row):
            if pd.isna(row['Centered_Return']) or pd.isna(row['Centered_Volatility']):
                return 'UNKNOWN'
                
            # Compare the immediate 24h action against the 14-day local baseline
            is_high_vol = row['Centered_Volatility'] > row['Macro_Vol_Baseline']
            is_strong_trend = abs(row['Centered_Return']) > row['Macro_Ret_Baseline']
            
            if is_strong_trend:
                if row['Centered_Return'] > 0:
                    return 'TRENDING'     # Moving Up fast
                else:
                    return 'BOOM_CRASH'   # Moving Down fast
            else:
                if is_high_vol:
                    return 'CHOP'         # Whipping sideways
                else:
                    return 'RANGING'      # Sleepy sideways
                    
        df['Raw_Regime'] = df.apply(map_adaptive_regime, axis=1)
        
        # ==========================================
        # 4. MACRO-SMOOTHING (The Steamroller)
        # ==========================================
        map_to_int = {'RANGING': 0, 'CHOP': 1, 'TRENDING': 2, 'BOOM_CRASH': 3, 'UNKNOWN': 4}
        map_to_str = {v: k for k, v in map_to_int.items()}
        
        df['Regime_Int'] = df['Raw_Regime'].map(map_to_int)
        
        # We use a 72-hour (3 * N) rolling mode. 
        # This completely annihilates the barcode effect. It forces the algorithm 
        # to only recognize macro-regimes that dominate a 3-day period.
        df['Smoothed_Int'] = df['Regime_Int'].rolling(window=3*N, center=True).apply(
            lambda x: pd.Series(x).mode()[0] if not pd.Series(x).mode().empty else 4,
            raw=False
        )
        
        df['Final_Regime'] = df['Smoothed_Int'].fillna(4).map(map_to_str)
        
        # Cap the edges
        df.loc[:(2*N), 'Final_Regime'] = 'UNKNOWN'
        df.loc[len(df)-(2*N):, 'Final_Regime'] = 'UNKNOWN'
        
        return df['Final_Regime'].tolist(), full_price_data['timestamp']

    def regime_at_timestamp(self, timestamp: pd.Timestamp, full_regimes = None, price_index = None) -> str:
        """
        Look up precomputed regime at the bar whose timestamp <= T and is last before/at T.
        Requires classify_full_history() to have been called.
        """
        if not full_regimes or price_index is None:
            return 'UNKNOWN'

        # position of last bar <= timestamp
        idx = price_index.searchsorted(timestamp, side='right') - 1
        if idx < 0 or idx >= len(full_regimes):
            return 'UNKNOWN'
        return full_regimes[idx]

    def plot_regime_chart(self, full_regimes: list, price_data: pd.DataFrame, 
                          title: str = "Strategy X-Ray Dashboard",
                          num_macro_snapshots: int = 4,    # Number of timeline splits (0 to disable)
                          snap_worst: int = 2,             # Number of worst trades to snapshot (0 to disable)
                          snap_best: int = 2,              # Number of best trades to snapshot (0 to disable)
                          snap_random: int = 0            # Number of random trades to snapshot (0 to disable)
                          ) -> None:
        logger.debug("Generating optimized Plotly HTML dashboard...")
        
        df_plot = price_data.copy()
        df_plot['Regime'] = full_regimes
        
        y_min, y_max = df_plot['low'].min() * 0.98, df_plot['high'].max() * 1.02
        
        # ==========================================
        # 1. FORCE 3-PANE LAYOUT
        # ==========================================
        fig = make_subplots(
            rows=3, cols=1, shared_xaxes=True,
            vertical_spacing=0.03, 
            row_heights=[0.6, 0.2, 0.2], # <-- Tweak these decimals to change panel heights (must sum to 1.0)
            subplot_titles=("Price Action & Trades", "Forecast & Calc Regime", "Tick-by-Tick Portfolio Value")
        )

        # ==========================================
        # 2. PRICE ACTION & GROUND TRUTH
        # ==========================================
        fig.add_trace(go.Candlestick(
            x=df_plot['timestamp'], open=df_plot['open'], high=df_plot['high'], 
            low=df_plot['low'], close=df_plot['close'], name='Price'
        ), row=1, col=1)

        bg_color_map = {
            'RANGING': 'rgba(52, 152, 219, 0.15)', 'CHOP': 'rgba(243, 156, 18, 0.15)',
            'TRENDING': 'rgba(46, 204, 113, 0.15)', 'BOOM_CRASH': 'rgba(231, 76, 60, 0.15)',
            'UNKNOWN': 'rgba(189, 195, 199, 0.15)'
        }
        solid_color_map = {
            'RANGING': '#3498db', 'CHOP': '#f39c12', 'TRENDING': '#2ecc71', 
            'BOOM_CRASH': '#e74c3c', 'UNKNOWN': '#bdc3c7'
        }

        # Legend Dummy Traces & Backgrounds
        present_regimes = df_plot['Regime'].unique()
        for regime, color in bg_color_map.items():
            if regime in present_regimes:
                fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(symbol='square', size=15, color=solid_color_map[regime]), name=f"Truth Bg: {regime}"), row=1, col=1)

        df_plot['block_id'] = (df_plot['Regime'] != df_plot['Regime'].shift(1)).cumsum()
        for _, group in df_plot.groupby('block_id'):
            regime = group['Regime'].iloc[0]
            fig.add_vrect(
                x0=group['timestamp'].iloc[0], x1=group['timestamp'].iloc[-1],
                fillcolor=bg_color_map.get(regime, 'rgba(255, 255, 255, 0)'),
                layer="below", line_width=0, showlegend=False, row=1, col=1
            )

        # ==========================================
        # 3. TRADES & REGIME HIGHLIGHTERS
        # ==========================================
        if self.completed_trades:
            win_x, win_y, win_text = [], [], []
            loss_x, loss_y, loss_text = [], [], []
            entry_x, entry_y, entry_symbols, entry_colors = [], [], [], []
            exit_x, exit_y = [], []
            
            hl_x, hl_y = {k: [] for k in solid_color_map.keys()}, {k: [] for k in solid_color_map.keys()}

            for i, trade in enumerate(self.completed_trades):
                calc_regime = str(trade.entry_regime).upper() if trade.entry_regime else "UNKNOWN"
                
                if calc_regime in hl_x:
                    hl_x[calc_regime].extend([trade.entry_time, trade.entry_time, None])
                    hl_y[calc_regime].extend([y_min, y_max, None])

                hover_text = (
                    f"<b>Trade {i+1} ({trade.side.value})</b><br>"
                    f"Net P&L: {trade.net_profit_loss_percent:+.2f}%<br>"
                    f"Duration: {trade.duration_minutes:.0f}m"
                )

                if trade.profitable_net:
                    win_x.extend([trade.entry_time, trade.exit_time, None]), win_y.extend([trade.entry_price, trade.exit_price, None]), win_text.extend([hover_text, hover_text, None])
                else:
                    loss_x.extend([trade.entry_time, trade.exit_time, None]), loss_y.extend([trade.entry_price, trade.exit_price, None]), loss_text.extend([hover_text, hover_text, None])

                entry_x.append(trade.entry_time), entry_y.append(trade.entry_price), entry_symbols.append('triangle-up' if trade.side.value == 'LONG' else 'triangle-down'), entry_colors.append(solid_color_map.get(calc_regime, '#ffffff'))
                exit_x.append(trade.exit_time), exit_y.append(trade.exit_price)
                
            # Draw Highlighters
            for regime, x_coords in hl_x.items():
                if x_coords: fig.add_trace(go.Scatter(x=x_coords, y=hl_y[regime], mode='lines', line=dict(color=solid_color_map[regime], width=6), opacity=0.35, hoverinfo='skip', showlegend=False), row=1, col=1)

            # Draw Lines
            fig.add_trace(go.Scatter(x=win_x, y=win_y, text=win_text, hoverinfo="text", mode='lines', line=dict(color="#2ecc71", width=2, dash='dot'), name="Winning Trade", showlegend=False), row=1, col=1)
            fig.add_trace(go.Scatter(x=loss_x, y=loss_y, text=loss_text, hoverinfo="text", mode='lines', line=dict(color="#e74c3c", width=2, dash='dot'), name="Losing Trade", showlegend=False), row=1, col=1)
            
            # Draw Exits FIRST (Large hollow circle "Halo")
            fig.add_trace(go.Scatter(x=exit_x, y=exit_y, mode='markers', hoverinfo="skip", marker=dict(symbol='circle-open', size=22, color="white", line=dict(width=2, color="white")), name="Trade Exits", showlegend=False), row=1, col=1)
            
            # Draw Entries SECOND (Smaller solid triangle sits inside the Halo if they overlap)
            fig.add_trace(go.Scatter(x=entry_x, y=entry_y, mode='markers', hoverinfo="skip", marker=dict(symbol=entry_symbols, size=14, color=entry_colors, line=dict(width=2, color="#000000")), name="Entries", showlegend=False), row=1, col=1)

        # ==========================================
        # 4. FORECAST & CALC REGIME PANE (Row 2)
        # ==========================================
        if 'forecast' in df_plot.columns and 'calc_regime' in df_plot.columns:
            bar_colors = df_plot['calc_regime'].map(lambda x: solid_color_map.get(str(x).upper(), '#bdc3c7')).tolist()
            fig.add_trace(go.Bar(x=df_plot['timestamp'], y=df_plot['forecast'], marker_color=bar_colors, name='Forecast (Colored by Calc Regime)', marker_line_width=0), row=2, col=1)
            fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, row=2, col=1)
        else:
            logger.warning("⚠ 'forecast' or 'calc_regime' missing! Row 2 will be blank.")

        # ==========================================
        # 5. EQUITY CURVE (Row 3)
        # ==========================================
        if 'portfolio_value' in df_plot.columns:
            fig.add_trace(go.Scatter(x=df_plot['timestamp'], y=df_plot['portfolio_value'], mode='lines', line=dict(color='#9b59b6', width=2), name='Portfolio Value', hoverinfo='x+y'), row=3, col=1)
            min_eq, max_eq = df_plot['portfolio_value'].min(), df_plot['portfolio_value'].max()
            padding = (max_eq - min_eq) * 0.1 if max_eq != min_eq else min_eq * 0.01
            fig.update_yaxes(range=[min_eq - padding, max_eq + padding], row=3, col=1)

        # ==========================================
        # 6. FINAL CLEANUP & EXPORT
        # ==========================================
        fig.update_layout(title=title, template="plotly_dark", hovermode="x unified", dragmode="pan", height=900, legend=dict(yanchor="top", y=1, xanchor="left", x=1.02))
        fig.update_xaxes(rangeslider_visible=False)
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="Forecast", row=2, col=1)
        fig.update_yaxes(title_text="Capital ($)", row=3, col=1)

        chart_config = {'scrollZoom': True, 'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'select2d']}
        
        output_file = "results/strategy_dashboard.html"
        performance_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(performance_dir)
        output_file_path = os.path.join(project_dir, output_file)
        fig.write_html(output_file_path, config=chart_config)
        
        logger.debug(f"Interactive dashboard successfully saved to {output_file}")

        # ==========================================
        # 7. AUTOMATED SNAPSHOTS (MACRO & MICRO)
        # ==========================================
        if num_macro_snapshots > 0 or snap_worst > 0 or snap_best > 0 or snap_random > 0:
            try:
                import random
                import shutil  

                logger.debug(f"📸 Generating snapshots ({num_macro_snapshots} macro, {snap_best} best, {snap_worst} worst, {snap_random} random)...")
                snap_dir = "results/trade_snapshots"
                snap_dir_path = os.path.join(project_dir, snap_dir)

                if os.path.exists(snap_dir_path):
                    shutil.rmtree(snap_dir_path, ignore_errors=True)
                os.makedirs(snap_dir_path, exist_ok=True)
                
                # ------------------------------------------
                # PART A: MACRO VIEW (Dynamic Time Splits)
                # ------------------------------------------
                if num_macro_snapshots > 0:
                    min_time = df_plot['timestamp'].min()
                    max_time = df_plot['timestamp'].max()
                    total_duration = max_time - min_time
                    chunk_duration = total_duration / num_macro_snapshots
                    
                    for i in range(num_macro_snapshots):
                        x_start = min_time + (i * chunk_duration)
                        x_end = min_time + ((i + 1) * chunk_duration)
                        
                        fig.update_xaxes(range=[x_start, x_end])
                        filename = f"{snap_dir_path}/Macro_Part{i+1}_of_{num_macro_snapshots}.png"
                        fig.write_image(filename, width=1920, height=1080, scale=1.5)
                    
                # ------------------------------------------
                # PART B: MICRO VIEW (Dynamic Trades)
                # ------------------------------------------
                min_zoom_pad_hour = 36
                duration_zoom_pad_factor = 2
                if self.completed_trades and (snap_best > 0 or snap_worst > 0 or snap_random > 0):
                    sorted_trades = sorted(self.completed_trades, key=lambda t: t.net_profit_loss_percent)
                    trades_to_snap = []
                    
                    # 1. Grab Worst
                    actual_worst = min(snap_worst, len(sorted_trades))
                    for i in range(actual_worst):
                        trades_to_snap.append(("Worst", i+1, sorted_trades[i]))
                    
                    # 2. Grab Best
                    actual_best = min(snap_best, len(sorted_trades) - actual_worst)
                    actual_best = max(0, actual_best) 
                    for i in range(actual_best):
                        trades_to_snap.append(("Best", i+1, sorted_trades[-(i+1)]))
                    
                    # 3. Grab Randoms
                    picked_trades = [t[2] for t in trades_to_snap]
                    remaining = [t for t in sorted_trades if t not in picked_trades]
                    
                    actual_random = min(snap_random, len(remaining))
                    if actual_random > 0:
                        random_picks = random.sample(remaining, actual_random)
                        for i in range(actual_random):
                            trades_to_snap.append(("Random", i+1, random_picks[i]))

                    # Take the trade pictures
                    for category, rank, trade in trades_to_snap:
                        duration = trade.exit_time - trade.entry_time
                        
                        # Pad calculation (Combines dynamic padding with a safe minimum)
                        dynamic_pad = duration * duration_zoom_pad_factor if duration.total_seconds() > 0 else pd.Timedelta(hours=4)
                        min_zoom_pad = pd.Timedelta(hours=min_zoom_pad_hour)
                        pad = max(dynamic_pad, min_zoom_pad)
                        
                        x_start = trade.entry_time - pad
                        x_end = trade.exit_time + pad
                        
                        # 1. Zoom X-Axis
                        fig.update_xaxes(range=[x_start, x_end])
                        
                        # 2. DYNAMIC Y-AXIS RESCALING (Fixes the flattened candles)
                        mask = (df_plot['timestamp'] >= x_start) & (df_plot['timestamp'] <= x_end)
                        local_df = df_plot[mask]
                        
                        if not local_df.empty:
                            # Rescale Price Pane
                            p_min, p_max = local_df['low'].min(), local_df['high'].max()
                            p_pad = (p_max - p_min) * 0.05 if p_max != p_min else p_max * 0.01
                            fig.update_yaxes(range=[p_min - p_pad, p_max + p_pad], row=1, col=1)
                            
                            # Rescale Forecast Pane
                            if 'forecast' in local_df.columns:
                                f_min, f_max = local_df['forecast'].min(), local_df['forecast'].max()
                                f_pad = (f_max - f_min) * 0.1 if f_max != f_min else 0.5
                                fig.update_yaxes(range=[f_min - f_pad, f_max + f_pad], row=2, col=1)
                            
                            # Rescale Equity Pane
                            if 'portfolio_value' in local_df.columns:
                                eq_min, eq_max = local_df['portfolio_value'].min(), local_df['portfolio_value'].max()
                                eq_pad = (eq_max - eq_min) * 0.1 if eq_max != eq_min else eq_min * 0.01
                                fig.update_yaxes(range=[eq_min - eq_pad, eq_max + eq_pad], row=3, col=1)

                        # 3. Save Image
                        safe_date = trade.entry_time.strftime("%Y%m%d_%H%M")
                        filename = f"{snap_dir_path}/Micro_{category}_{rank}_{trade.side.value}_{trade.net_profit_loss_percent:+.2f}pct_{safe_date}.png"
                        fig.write_image(filename, width=1920, height=1080, scale=1.5)

                # ------------------------------------------
                # PART C: RESET FOR HTML
                # ------------------------------------------
                # We must reset BOTH X and Y axes so the interactive HTML isn't locked!
                fig.update_xaxes(autorange=True) 
                fig.update_yaxes(autorange=True, row=1, col=1)
                fig.update_yaxes(autorange=True, row=2, col=1)
                fig.update_yaxes(autorange=True, row=3, col=1)
                
                logger.debug(f"✓ Successfully saved requested snapshots to /{snap_dir_path}/")
                
            except Exception as e:
                logger.warning(f"⚠ Failed to generate image snapshots: {e} (Ensure 'kaleido' is installed via pip)")
                fig.update_xaxes(autorange=True) # Ensure HTML doesn't break even if images fail

    def calculate_ground_truth_regime_hindsight(self, 
                                                timestamp: pd.Timestamp, 
                                                full_price_data: pd.DataFrame,
                                                lookback_bars: int = 250,
                                                lookahead_bars: int = 250) -> str:
        """
        Calculate ground truth regime using HINDSIGHT (centered window).
        
        CRITICAL: This uses FUTURE data - only for post-backtest validation.
        Should NEVER be called during strategy execution.
        
        Literature:
        - Ang & Timmermann (2012): "Regime Changes and Financial Markets"
        - Hamilton (1989): "A New Approach to Economic Analysis of Nonstationary Time Series"
        
        Args:
            timestamp: Point in time to classify
            full_price_data: Complete OHLCV DataFrame with columns:
                            ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            lookback_bars: Bars before timestamp (default 250 = ~10 days on 1h)
            lookahead_bars: Bars after timestamp (default 250 = ~10 days) - USES FUTURE
        
        Returns:
            'RANGING_FAVORABLE', 'TRENDING', or 'UNKNOWN'
        """
        # LOG 1: Function entry

        try:
            if full_price_data is None or len(full_price_data) == 0:
                return 'UNKNOWN'
            
            # Find index for this timestamp
            mask = full_price_data['timestamp'] <= timestamp
            if not mask.any(): #Check that timestamp of trade is within the range of price data
                logger.warning(f"Cannot classify regime. Issue with historical data storage")
                return 'UNKNOWN'
            
            # Need sufficient data on BOTH sides (past + future)                        
            idx = len(full_price_data[mask]) - 1
            if (idx < lookback_bars or # Check that there is enough bar in the past
                 idx + lookahead_bars >= len(full_price_data)): # Check that there is enough bar in the future
                return 'UNKNOWN'
            
            window = full_price_data.iloc[idx - lookback_bars:idx + lookahead_bars + 1].copy()
          
            # if len(window) < (lookback_bars + lookahead_bars):
            #     return 'UNKNOWN'

            # === CRITERION 1: Trend Strength (centered window) ===
            initial_price = window.iloc[0]['close']
            final_price = window.iloc[-1]['close']
            rolling_return = ((final_price - initial_price) / initial_price) * 100
            trend_strength = abs(rolling_return)
            
            # === CRITERION 2: Directional Balance ===
            returns = window['close'].pct_change().dropna()
            up_bars = (returns > 0).sum()
            down_bars = (returns < 0).sum()
            up_down_ratio = up_bars / down_bars if down_bars > 0 else 999
            
            # === CRITERION 3: Mean Reversion Behavior (MA Crossovers) ===
            window['ma20'] = window['close'].rolling(20, min_periods=1).mean()
            window['above_ma'] = window['close'] > window['ma20']
            # Count state changes (crossovers)
            crossovers = (window['above_ma'].diff().astype(bool) != 0).sum()
            crossover_frequency = crossovers / len(window) if len(window) > 0 else 0
            
            # === CRITERION 4: Volatility (ATR) ===
            hl = window['high'] - window['low']
            atr_pct = (hl.mean() / window['close'].mean()) * 100
            
            # Compare to historical baseline (only uses past, no look-ahead for baseline)
            hist_window = full_price_data.iloc[:idx]
            if len(hist_window) > 500:
                hist_hl = hist_window['high'] - hist_window['low']
                hist_atr_pct = (hist_hl.mean() / hist_window['close'].mean()) * 100
                atr_relative = atr_pct / hist_atr_pct if hist_atr_pct > 0 else 1.0
            else:
                atr_relative = 1.0
            
            # # === CLASSIFICATION LOGIC ===
            # ranging_conditions = [
            #     trend_strength < 3.0,              # Tighten from 8.0 to 3.0
            #     0.95 <= up_down_ratio <= 1.05,     # Tighten from 0.90-1.10 to 0.95-1.05
            #     crossover_frequency > 0.10,         # Tighten from 0.02 to 0.10 (10% of bars)
            #     atr_relative > 0.9                  # Tighten from 0.7 to 0.9
            # ]

            # if sum(ranging_conditions) >= 3:  # Require 3 of 4 (was 2 of 4)
            #     return 'RANGING_FAVORABLE'

            # # If not enough conditions, check if TRENDING
            # trending_conditions = [
            #     trend_strength > 5.0,   # Strong trend
            #     (up_down_ratio < 0.85 or up_down_ratio > 1.15),  # Directional bias
            #     crossover_frequency < 0.05  # Few MA crossovers
            # ]

            # if sum(trending_conditions) >= 2:
            #     return 'TRENDING'

            return 'UNKNOWN'
            
        except Exception as e:
            logger.error(f"Error calculating ground truth regime: {e}")
            return 'UNKNOWN'

    def _get_empty_metrics(self) -> Dict[str, Any]:
        return {
            'overall_metrics': {},
            'by_regime': {},
            'by_ground_truth': {},
            'by_direction': {},
            'regime_validation': {}
        }

# Below Calculation of metrics

    def _calculate_standard_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate Tier 1 metrics for overall composite strategy."""
        total_trades = len(df) #Metric 1: Total Trades
        if total_trades == 0:
            return {}
        
        # Win Rate
        wins_net = df['profitable_net'].sum()
        win_rate_net = (wins_net / total_trades) * 100 

        # Profit Factor (Using portfolio impact)
        net_wins_sum = df[df['profitable_net']]['portfolio_impact_pct'].sum()
        net_losses_sum = abs(df[~df['profitable_net']]['portfolio_impact_pct'].sum())
        profit_factor_net = net_wins_sum / net_losses_sum if net_losses_sum > 0 else float('inf')

        winning_trades = df[df['profitable_net']]
        losing_trades = df[~df['profitable_net']]

        avg_duration_hours = df['duration_minutes'].mean() / 60 if total_trades > 0 else 0
        avg_win_duration_hr = winning_trades['duration_minutes'].mean() / 60 if len(winning_trades) > 0 else 0
        avg_loss_duration_hr = losing_trades['duration_minutes'].mean() / 60 if len(losing_trades) > 0 else 0

        # Average Win/Loss (As % of Portfolio)
        avg_win_pct = df[df['profitable_net']]['portfolio_impact_pct'].mean() if wins_net > 0 else 0
        avg_loss_pct = df[~df['profitable_net']]['portfolio_impact_pct'].mean() if (total_trades - wins_net) > 0 else 0

        # Expectancy per Trade (Expected Portfolio Growth %)
        expectancy_pct = (win_rate_net / 100 * avg_win_pct) + ((1 - win_rate_net / 100) * avg_loss_pct)

        # Commission Drag (What % of our winning potential is eaten by fees?)
        avg_commission_pct = df['commission_pct'].mean()

        #Unprofitable due to commissions (What % of trades that were gross winners became net losers after fees?)
        net_losses = df[~df['profitable_net']]
        gross_loss = df[~df['profitable_absolute']]
        unprofitable_due_to_commission_pct = (1- len(gross_loss) / len(net_losses)) * 100 if len(net_losses) > 0 else 0

        # --- THE FIX: TRUE REALIZED PORTFOLIO RETURN ---
        starting_capital = df.sort_values('entry_time').iloc[0]['initial_portfolio_value']        
        final_capital = df.sort_values('exit_time').iloc[-1]['final_portfolio_value']
        total_return_pct = ((final_capital - starting_capital) / starting_capital) * 100

        # Ensure we have the date for grouping
        if 'exit_date' not in df.columns:
            df['exit_date'] = pd.to_datetime(df['exit_time']).dt.date

        # 1. Group by day and SUM the impacts (This perfectly solves overlapping trades)
        daily_pct_returns = df.groupby('exit_date')['portfolio_impact_pct'].sum()
        # 2. Compound the daily returns (This isolates the PnL to just this subset)
        total_return_pct_per_day = ((1 + daily_pct_returns / 100).prod() - 1) * 100

        # --- STEP 3: RISK METRICS (We will plug the logic in here next) ---
        max_dd_percent = self.calculate_max_drawdown(df)
        sharpe_ratio = self.calculate_sharpe_ratio(df)
        calmar_ratio = total_return_pct / abs(max_dd_percent) if max_dd_percent != 0 else 0

        return {
            'total_trades': total_trades,
            '[OVERALL ONLY] total_return_pct': round(total_return_pct, 3),
            'total_return_pct_per_day': round(total_return_pct_per_day, 3),
            'net_win_rate_pct': round(win_rate_net, 2),
            'expectancy_per_trade_pct': round(expectancy_pct, 4),
            'net_profit_factor': round(profit_factor_net, 3),
            'avg_commission_pct': round(avg_commission_pct, 4),
            'unprofitable_due_to_commission_pct': round(unprofitable_due_to_commission_pct, 4),
            'avg_win_pct': round(avg_win_pct, 4),
            'avg_loss_pct': round(avg_loss_pct, 4),
            'avg_duration_hours': round(avg_duration_hours, 2),
            'avg_win_duration_hr': round(avg_win_duration_hr, 2),
            'avg_loss_duration_hr': round(avg_loss_duration_hr, 2),
            'max_drawdown_pct': round(max_dd_percent, 3),
            'sharpe_ratio': round(sharpe_ratio, 3),
            'calmar_ratio': round(calmar_ratio, 3)
        }

    def calculate_max_drawdown(self, df: pd.DataFrame) -> float:
        """Calculate true max drawdown, safe for both total portfolio and subsets."""
        if len(df) == 0:
            return 0.0
            
        df_sorted = df.sort_values('exit_time').copy()
        
        # FIX: Changed 'net_portfolio_profit_loss_percent' to 'portfolio_impact_pct'
        returns = df_sorted['portfolio_impact_pct'] / 100
        equity_curve = (1 + returns).cumprod()
        
        # Fix the missing initial capital bug by inserting 1.0 at the beginning
        equity_curve = pd.concat([pd.Series([1.0]), equity_curve], ignore_index=True)
        
        # Standard drawdown math
        running_max = equity_curve.expanding().max()
        drawdown = (equity_curve - running_max) / running_max
        
        return drawdown.min() * 100

    def calculate_sharpe_ratio(self, df: pd.DataFrame, risk_free_rate: float = 0.0) -> float:
        """Calculate Annualized Sharpe Ratio, safe for both total portfolio and subsets."""
        if len(df) < 2:
            return 0.0
            
        df_sorted = df.sort_values('exit_time').copy()
        
        if 'exit_date' not in df_sorted.columns:
            df_sorted['exit_date'] = pd.to_datetime(df_sorted['exit_time']).dt.date
        
        # FIX: Changed 'net_portfolio_profit_loss_percent' to 'portfolio_impact_pct'
        daily_returns_pct = df_sorted.groupby('exit_date')['portfolio_impact_pct'].sum() / 100
        
        # 2. Create calendar from first trade to last trade
        start_date = daily_returns_pct.index.min()
        end_date = daily_returns_pct.index.max()
        
        if start_date == end_date:
            return 0.0
            
        full_calendar = pd.date_range(start=start_date, end=end_date).date
        
        # 3. Reindex to full calendar. Days with no trades get 0.0 return
        daily_returns_series = daily_returns_pct.reindex(full_calendar).fillna(0.0)
        
        std_dev = daily_returns_series.std()
        if std_dev == 0 or pd.isna(std_dev):
            return 0.0
            
        # 4. Calculate Annualized Sharpe (assuming 365 days for Crypto)
        daily_rf_rate = risk_free_rate / 365
        
        excess_daily_returns = daily_returns_series - daily_rf_rate
        annualized_sharpe = (excess_daily_returns.mean() / std_dev) * np.sqrt(365)
        
        return annualized_sharpe

    def _calculate_by_regime_metrics(self, df: pd.DataFrame, regime_col: str) -> Dict[str, Dict[str, Any]]:
        """Calculate metrics by regime (detected or ground truth)."""
        regime_metrics = {}
        
        for regime in df[regime_col].unique():
            regime_df = df[df[regime_col] == regime]
            if len(regime_df) == 0:
                continue
        
            regime_metrics[regime] = self._calculate_standard_metrics(regime_df)
        return regime_metrics
        
    def _calculate_by_direction_metrics(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Calculate metrics by LONG vs SHORT."""
        direction_metrics = {}
        
        for side in ['LONG', 'SHORT']:
            side_df = df[df['side'] == side]
            if len(side_df) == 0:
                continue
        
            direction_metrics[side] = self._calculate_standard_metrics(side_df)
        return direction_metrics

    def _calculate_regime_validation_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate regime classification accuracy with a native confusion matrix."""
        if 'detected_regime' not in df.columns or 'ground_truth_regime' not in df.columns:
            return {'error': 'Missing regime columns'}
        
        if len(df) == 0:
            return {'error': 'No trades to analyze'}

        # Normalize regimes safely (handling potential NaNs)
        detected = df['detected_regime'].fillna('UNKNOWN').astype(str).str.upper().str.replace('_', ' ')
        ground_truth = df['ground_truth_regime'].fillna('UNKNOWN').astype(str).str.upper().str.replace('_', ' ')
        
        # Calculate overall agreement
        agreements = (detected == ground_truth).sum()
        total = len(df)
        accuracy = (agreements / total * 100) if total > 0 else 0
        
        # Build confusion matrix natively using Pandas (100x faster than looping)
        confusion_df = pd.crosstab(index=detected, columns=ground_truth)
        
        # Convert it back to the exact nested dictionary structure you had:
        # { 'DETECTED_REGIME': { 'GROUND_TRUTH_REGIME': count } }
        confusion_matrix = confusion_df.to_dict(orient='index')
        
        return {
            'total_trades_analyzed': total,
            'agreements': int(agreements),
            'accuracy_pct': round(accuracy, 2),
            'confusion_matrix': confusion_matrix,
            'detected_regimes': sorted(detected.unique().tolist()),
            'ground_truth_regimes': sorted(ground_truth.unique().tolist())
        }



# Below metric logging

    def log_performance_metrics(self, metrics: Dict[str, Any]):
        

        # Log to console
        logger.debug("\n" + "="*80)
        logger.debug("TIER 1 PERFORMANCE METRICS")
        logger.debug("="*80)

        overall = metrics['overall_metrics']
        logger.debug(f"Net Profit Factor: {overall['net_profit_factor']}")
        # logger.debug(f"Expectancy per Trade: ${overall['expectancy_per_trade_usd']}")
        # # logger.debug(f"Commission Efficiency: {overall['commission_efficiency_pct']}%")
        # logger.debug(f"Net Win Rate: {overall['net_win_rate_pct']}%")
        # logger.debug(f"Max Drawdown: ${overall['max_drawdown_usd']} ({overall['max_drawdown_pct']}%)")  # NEW
        # logger.debug(f"Sharpe Ratio: {overall['sharpe_ratio']}")  # NEW
        # logger.debug(f"Calmar Ratio: {overall['calmar_ratio']}")  # NEW
        
        # logger.debug("\nREGIME VALIDATION:")
        # validation = metrics['regime_validation']
        # logger.debug(f"Classification Accuracy: {validation['accuracy_pct']}%")
        # logger.debug(f"False Positives: {validation['false_positives']}")

        # agreement_metrics = self.trade_regime_agreement
        # if 'total_trades_analyzed' in agreement_metrics and 'error' not in agreement_metrics:
        #     logger.debug(f"Total trades analyzed: {agreement_metrics['total_trades_analyzed']}")
        #     logger.debug(f"Agreement rate: {agreement_metrics['agreement_rate_pct']}%")
        #     logger.debug(f"Agreements: {agreement_metrics['agreements']} trades")
        #     logger.debug(f"Detected regimes: {agreement_metrics.get('detected_regimes', {})}")
        #     logger.debug(f"Ground truth regimes: {agreement_metrics.get('ground_truth_regimes', {})}")
        # else:
        #     logger.warning("Agreement metrics calculation returned unexpected format")
        #     logger.warning(f"Content: {agreement_metrics}")


# Below old feature


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

    def _get_return_buy_hold(self) -> float:
        """
        Calculate the return of a buy-and-hold strategy.
        """
        if not self.completed_trades:
            return 0.0
        
        # Get first entry price and last exit price
        sorted_trades = sorted(self.completed_trades, key=lambda t: t.entry_time)
        first_trade = sorted_trades[0]
        
        sorted_by_exit = sorted(self.completed_trades, key=lambda t: t.exit_time)
        last_trade = sorted_by_exit[-1]
        
        # Calculate buy and hold return percentage
        buy_hold_return = ((last_trade.exit_price / first_trade.entry_price) - 1)*100
  
        return buy_hold_return

    def _get_buy_hold_sharpe_ratio(self, risk_free_rate: float = 0.0) -> float:
        """
        Calculate the Sharpe ratio of a buy-and-hold strategy.
        Simulates actual portfolio values and calculates std dev on those.
        """
        if not self.completed_trades:
            return 0.0
        
        sorted_trades = sorted(self.completed_trades, key=lambda t: t.exit_time)
        
        if len(sorted_trades) < 2:
            return 0.0
        
        # Get initial investment amount (use first trade as reference)
        first_trade = sorted_trades[0]
        initial_investment = first_trade.entry_price * first_trade.matched_quantity
        
        # Calculate how many units we could buy with initial investment
        initial_units = initial_investment / first_trade.entry_price
        
        # Calculate portfolio values at each trade exit time
        portfolio_values = []
        for trade in sorted_trades:
            # Portfolio value = units * current_price
            portfolio_value = initial_units * trade.exit_price
            portfolio_values.append(portfolio_value)
        
        # Calculate returns from portfolio values
        returns = []
        for i in range(1, len(portfolio_values)):
            period_return = ((portfolio_values[i] / portfolio_values[i-1]) - 1) * 100
            returns.append(period_return)
        
        if len(returns) < 1:
            return 0.0
        
        # Calculate std dev of returns
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        std_dev = variance ** 0.5
        
        if std_dev == 0:
            return 0.0
        
        # Total portfolio return
        total_return = ((portfolio_values[-1] / portfolio_values[0]) - 1) * 100
        
        return (total_return - risk_free_rate) / std_dev

    def _calculate_advanced_sharpe_ratio(self, returns: List[float], risk_free_rate: float = 0.0) -> float:
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
        
        total_profit_loss = sum(returns)
        mean_return = sum(returns) / len(returns)
        std_dev = (sum((r - mean_return) ** 2 for r in returns) / len(returns)) ** 0.5
        
        if std_dev == 0:
            return 0.0
        
        return (total_profit_loss - abs(risk_free_rate)) / std_dev

    # def get_performance_summary(self) -> Dict[str, Any]:
    #     """Get overall performance summary."""
    #     if not self.completed_trades:
    #         return {'total_trades': 0}
        
    #     total_trades = len(self.completed_trades)
    #     winning_trades = [t for t in self.completed_trades if t.net_profit_loss_absolute > 0]
    #     losing_trades = [t for t in self.completed_trades if t.net_profit_loss_absolute < 0]
        
    #     total_pnl = sum(t.net_profit_loss_absolute for t in self.completed_trades)
    #     total_pnl_percent = sum(t.profit_loss_percent for t in self.completed_trades)
        
    #     win_rate = len(winning_trades) / total_trades * 100 if total_trades > 0 else 0
        
    #     avg_win = np.mean([t.net_profit_loss_absolute for t in winning_trades]) if winning_trades else 0
    #     avg_loss = np.mean([t.net_profit_loss_absolute for t in losing_trades]) if losing_trades else 0
        
    #     return {
    #         'total_trades': total_trades,
    #         'winning_trades': len(winning_trades),
    #         'losing_trades': len(losing_trades),
    #         'win_rate_percent': win_rate,
    #         'total_pnl': total_pnl,
    #         'total_pnl_percent': total_pnl_percent,
    #         'avg_win': avg_win,
    #         'avg_loss': avg_loss,
    #         'profit_factor': abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
    #     }
    
    # def print_detailed_trade_summary(tracker):
    #     """Print detailed summary of all completed trades."""
    #     logger.debug("\n" + "="*80)
    #     logger.debug("DETAILED TRADE SUMMARY")
    #     logger.debug("="*80)
        
    #     if not tracker.completed_trades:
    #         logger.debug("No completed trades.")
    #         return
        
    #     total_pnl = 0
    #     winning_trades = 0
    #     losing_trades = 0
        
    #     for i, trade in enumerate(tracker.completed_trades, 1):
    #         pnl = trade.profit_loss_absolute
    #         pnl_pct = trade.profit_loss_percent
    #         net_pnl = trade.net_profit_loss_absolute
            
    #         total_pnl += pnl
    #         if pnl > 0:
    #             winning_trades += 1
    #             status = "WIN ✓"
    #         elif pnl < 0:
    #             losing_trades += 1
    #             status = "LOSS ✗"
    #         else:
    #             status = "BREAK-EVEN"
            
    #         logger.debug(f"Trade #{i:2d}: {trade.side.value:<5} {trade.matched_quantity:>6.3f} BTC "
    #             f"@ {trade.entry_price:>8.0f} -> {trade.exit_price:>8.0f} "
    #             f"| P&L: {pnl:>8.0f} ({pnl_pct:>+6.2f}%) "
    #             f"| Net: {net_pnl:>8.0f} | {status}")
        
    #     logger.debug("-" * 80)
    #     logger.debug(f"SUMMARY: {len(tracker.completed_trades)} trades | "
    #         f"Wins: {winning_trades} | Losses: {losing_trades} | "
    #         f"Win Rate: {winning_trades/len(tracker.completed_trades)*100:.1f}%")
    #     logger.debug(f"Total P&L: {total_pnl:.0f} | Average P&L: {total_pnl/len(tracker.completed_trades):.0f}")
    #     logger.debug("="*80)

    # def get_equity_curve(self) -> pd.DataFrame:
    #     """
    #     Generate equity curve data.
        
    #     Returns:
    #         DataFrame with equity curve data
    #     """
    #     if not self.completed_trades:
    #         return pd.DataFrame(columns=['timestamp', 'equity'])
        
    #     # Sort trades by exit time
    #     sorted_trades = sorted(self.completed_trades, key=lambda t: t.exit_time)
        
    #     # Generate equity curve
    #     curve_data = []
    #     cumulative_return = 100.0  # Start with 100 units
        
    #     for trade in sorted_trades:
    #         # Apply the trade profit/loss to the equity
    #         cumulative_return *= (1 + trade.profit_loss_percent / 100)
    #         curve_data.append({
    #             'timestamp': trade.exit_time,
    #             'equity': cumulative_return
    #         })
        
    #     return pd.DataFrame(curve_data)
    
    # def generate_report(self, output_file: str = 'performance_report.html') -> None:
    #     """
    #     Generate a performance report.
        
    #     Args:
    #         output_file: Path to save the HTML report
    #     """
    #     try:
    #         # Get metrics
    #         metrics = self.get_performance_metrics()
    #         equity_curve = self.get_equity_curve()
            
    #         # Create HTML report
    #         html = """
    #         <html>
    #         <head>
    #             <title>Trading Bot Performance Report</title>
    #             <style>
    #                 body { font-family: Arial, sans-serif; margin: 20px; }
    #                 .container { max-width: 1200px; margin: 0 auto; }
    #                 .metrics { display: flex; flex-wrap: wrap; }
    #                 .metric-card { 
    #                     background-color: #f9f9f9; 
    #                     border-radius: 8px; 
    #                     padding: 15px; 
    #                     margin: 10px; 
    #                     width: 200px;
    #                     box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    #                 }
    #                 .metric-value { font-size: 24px; font-weight: bold; }
    #                 .metric-label { color: #666; }
    #                 h1, h2 { color: #333; }
    #                 table { width: 100%; border-collapse: collapse; margin: 20px 0; }
    #                 th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
    #                 th { background-color: #f2f2f2; }
    #                 tr:hover { background-color: #f5f5f5; }
    #             </style>
    #         </head>
    #         <body>
    #             <div class="container">
    #                 <h1>Trading Bot Performance Report</h1>
    #                 <p>Generated on {date}</p>
                    
    #                 <h2>Performance Metrics</h2>
    #                 <div class="metrics">
    #                     <div class="metric-card">
    #                         <div class="metric-value">{total_trades}</div>
    #                         <div class="metric-label">Total Trades</div>
    #                     </div>
    #                     <div class="metric-card">
    #                         <div class="metric-value">{win_rate:.2f}%</div>
    #                         <div class="metric-label">Win Rate</div>
    #                     </div>
    #                     <div class="metric-card">
    #                         <div class="metric-value">{avg_profit:.2f}%</div>
    #                         <div class="metric-label">Avg. Profit/Loss</div>
    #                     </div>
    #                     <div class="metric-card">
    #                         <div class="metric-value">{total_profit:.2f}%</div>
    #                         <div class="metric-label">Total Profit/Loss</div>
    #                     </div>
    #                     <div class="metric-card">
    #                         <div class="metric-value">{sharpe:.2f}</div>
    #                         <div class="metric-label">Sharpe Ratio</div>
    #                     </div>
    #                 </div>
                    
    #                 <h2>Recent Trades</h2>
    #                 <table>
    #                     <tr>
    #                         <th>Symbol</th>
    #                         <th>Entry Time</th>
    #                         <th>Exit Time</th>
    #                         <th>Entry Price</th>
    #                         <th>Exit Price</th>
    #                         <th>Quantity</th>
    #                         <th>P/L %</th>
    #                     </tr>
    #                     {trade_rows}
    #                 </table>
    #             </div>
    #         </body>
    #         </html>
    #         """.format(
    #             date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #             total_trades=metrics['total_trades'],
    #             win_rate=metrics['win_rate'],
    #             avg_profit=metrics['avg_profit_loss'],
    #             total_profit=metrics['total_profit_loss'],
    #             sharpe=metrics['sharpe_ratio'],
    #             trade_rows=self._generate_trade_table_rows()
    #         )
            
    #         # Save to file
    #         with open(output_file, 'w') as f:
    #             f.write(html)
            
    #         logger.debug(f"Performance report saved to {output_file}")
        
    #     except Exception as e:
    #         logger.error(f"Error generating performance report: {e}")
    
    # def _generate_trade_table_rows(self) -> str:
    #     """Generate HTML table rows for trades."""
    #     rows = []
        
    #     # Get the 10 most recent trades
    #     recent_trades = sorted(self.completed_trades, key=lambda t: t.exit_time, reverse=True)[:10]
        
    #     for trade in recent_trades:
    #         row = f"""
    #         <tr>
    #             <td>{trade.symbol}</td>
    #             <td>{trade.entry_time}</td>
    #             <td>{trade.exit_time}</td>
    #             <td>{trade.entry_price:.2f}</td>
    #             <td>{trade.exit_price:.2f}</td>
    #             <td>{trade.quantity:.4f}</td>
    #             <td>{trade.profit_loss_percent:.2f}%</td>
    #         </tr>
    #         """
    #         rows.append(row)
        
    #     return "".join(rows)
