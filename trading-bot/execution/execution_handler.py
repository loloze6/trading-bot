from binance.client import Client
from config.settings import API_KEY, API_SECRET, USE_TESTNET
from config.cost_model import resolve_cost_model
from time import time, sleep
import logging
from typing import Dict, List, Optional, Union, Tuple
import datetime
from performance.metrics import EnhancedPerformanceTracker, CompletedTrade
from enum import Enum
from abc import ABC, abstractmethod


logger = logging.getLogger("trading_bot")  # Use the logger set up elsewhere

class PositionType(Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    CLOSE = "CLOSE"

"""
Execution Handler Module
========================
Manages order execution for both live trading (Binance API) and backtesting (mock).

Classes:
    - PositionType: Enum for position types (LONG/SHORT/CLOSE)
    - ExecutionHandler: Live trading execution with Binance margin API
    - MockExecutionHandler: Simulated execution for backtesting
"""

class BaseExecutionHandler(ABC):
    """
    Shared orchestration for live and mock execution.
    Subclasses implement open_long_position, open_short_position, close_position.
    All primitives must return (success: bool, debug: dict) where debug contains
    {symbol, price, quantity, trade_type}.
    """

    def __init__(self, performance_tracker=None, portfolio_info=None):
        self.performance_tracker = performance_tracker
        self.portfolio_info = portfolio_info
        self.executed_orders_counter = 0

    # ── Orchestration (identical for live and mock) ────────────────────

    def _execute_portfolio_rebalance(self, symbol, target_allocation, actual_allocation,
                                     allocation_change, balances, total_portfolio_value,
                                     data, signal=None) -> tuple[bool, dict]:
        try:

            if allocation_change != 0:
                current_price = data['close'].iloc[-1]
                target_position_value = total_portfolio_value * abs(target_allocation)
                logger.debug(f"   💼 Portfolio: ${total_portfolio_value:.2f} │ Target: ${target_position_value:.2f} ({target_position_value/current_price:.6f} units)")
                return self._handle_allocation_change(
                    symbol, actual_allocation, target_allocation,
                    allocation_change, current_price, data, signal, total_portfolio_value, balances
                )

            logger.warning(f"   ⚠ Allocation change is zero, no rebalance needed")
            return True, {}

        except Exception as e:
            logger.error(f"   ❌ Rebalance error for {symbol}: {e}", exc_info=True)
            return False, {"error": str(e)}

    def _handle_allocation_change(self, symbol, current_allocation, target_allocation,
                                  allocation_change, current_price, data, signal,
                                  total_portfolio_value, balances) -> tuple[bool, dict]:
        target_quantity     = abs(target_allocation)  * total_portfolio_value / current_price
        additional_quantity = abs(allocation_change)  * total_portfolio_value / current_price

        if (current_allocation <= 0 and target_allocation >= 0) or \
           (current_allocation >= 0 and target_allocation <= 0):
            direction = "Short/Neutral → Long/Neutral" if allocation_change > 0 else "Long/Neutral → Short/Neutral"
            logger.debug(f"   🔄 TRANSITION │ {direction} │ {target_quantity:.6f} @ ${current_price:.2f}")
            return self._execute_position_transition(
                symbol, current_allocation, target_allocation,
                target_quantity, current_price, data, signal, total_portfolio_value, balances
            )

        if allocation_change > 0:
            if current_allocation >= 0:
                logger.debug(f"   📈 ADD LONG │ +{additional_quantity:.6f} @ ${current_price:.2f}")
                return self._post_order(*self.open_long_position(symbol=symbol, quantity=additional_quantity, trade_type='LONG', data=data, signal=signal, total_portfolio_value=total_portfolio_value, balances=balances))
            else:
                logger.debug(f"   📈 REDUCE SHORT │ -{additional_quantity:.6f} @ ${current_price:.2f}")
                return self._post_order(*self.open_long_position(symbol=symbol, quantity=additional_quantity, trade_type='REDUCE_SHORT', data=data, signal=signal, total_portfolio_value=total_portfolio_value, balances=balances))
        else:
            if current_allocation <= 0:
                logger.debug(f"   📉 ADD SHORT │ +{additional_quantity:.6f} @ ${current_price:.2f}")
                return self._post_order(*self.open_short_position(symbol=symbol, quantity=-additional_quantity, trade_type='SHORT', data=data, signal=signal, total_portfolio_value=total_portfolio_value, balances=balances))
            else:
                logger.debug(f"   📉 REDUCE LONG │ -{additional_quantity:.6f} @ ${current_price:.2f}")
                return self._post_order(*self.open_short_position(symbol=symbol, quantity=-additional_quantity, trade_type='REDUCE_LONG', data=data, signal=signal, total_portfolio_value=total_portfolio_value, balances=balances))

    def _execute_position_transition(self, symbol, current_allocation, target_allocation,
                                     target_quantity, current_price, data, signal=None,
                                     total_portfolio_value=None, balances=None) -> tuple[bool, dict]:
        try:
            success, debug = True, {}

            if abs(current_allocation) > 0.00000001:
                success, debug = self.close_position(
                    symbol=symbol, data=data, signal=signal,
                    total_portfolio_value=total_portfolio_value, balances=balances, trade_type='CLOSE'
                )
                success, debug = self._post_order(success, debug)
                if not success:
                    return success, debug

            elif abs(current_allocation) != 0:
                logger.warning(f"      ⚠ Current allocation too small to close: {current_allocation}")

            if target_allocation > 0.00000001:
                return self._post_order(*self.open_long_position(symbol=symbol, quantity=target_quantity, trade_type='LONG', data=data, signal=signal, total_portfolio_value=total_portfolio_value, balances=balances))
            elif target_allocation < -0.00000001:
                return self._post_order(*self.open_short_position(symbol=symbol, quantity=-target_quantity, trade_type='SHORT', data=data, signal=signal, total_portfolio_value=total_portfolio_value, balances=balances))
            elif abs(target_allocation) != 0:
                logger.warning(f"      ⚠ Target allocation too small to open: {target_allocation}")

            return success, debug  # close-only (going neutral), balance already updated

        except Exception as e:
            logger.error(f"      ❌ Transition error: {e}", exc_info=True)
            return False, {"error": str(e)}

    def _post_order(self, success: bool, debug: dict) -> tuple[bool, dict]:
        """Update local balance after any successful order."""
        if success and self.portfolio_info and 'error' not in debug:
            self.portfolio_info.update_local_balance(
                symbol=debug['symbol'], price=debug['price'],
                quantity=debug['quantity'], trade_type=debug['trade_type']
            )
        return success, debug

    # ── Primitives (implemented by subclasses) ─────────────────────────

    @abstractmethod
    def open_long_position(self, symbol, quantity, trade_type, data, signal,
                           total_portfolio_value, balances) -> tuple[bool, dict]: ...

    @abstractmethod
    def open_short_position(self, symbol, quantity, trade_type, data, signal,
                            total_portfolio_value, balances) -> tuple[bool, dict]: ...

    @abstractmethod
    def close_position(self, symbol, data, signal, total_portfolio_value,
                       balances, trade_type) -> tuple[bool, dict]: ...

class ExecutionHandler(BaseExecutionHandler):

    def __init__(self, test_mode=False, performance_tracker=None, portfolio_info=None):
        super().__init__(performance_tracker=performance_tracker, portfolio_info=portfolio_info)
        self.client = Client(API_KEY, API_SECRET, testnet=USE_TESTNET)
        self.test_mode = test_mode
        self.positions = {}
        try:
            self.client.enable_margin_account()
            logger.debug(f"🔗 Live Execution Handler │ {'Testnet' if USE_TESTNET else 'Live'} │ Margin: Enabled")
        except Exception as e:
            logger.debug(f"🔗 Margin status: {e}")

    def _get_free_margin_balance(self, asset: str) -> float:
        """Get free margin balance for an asset — avoids unnecessary borrows."""
        try:
            account = self.client.get_margin_account()
            for a in account['userAssets']:
                if a['asset'] == asset:
                    return float(a['free'])
        except Exception:
            pass
        return 0.0

    def open_long_position(self, symbol, quantity, trade_type, data=None, signal=None,
                           total_portfolio_value=None, balances=None) -> tuple[bool, dict]:
        try:
            price = data['close'].iloc[-1] if hasattr(data['close'], 'iloc') else data['close']
            quantity = self._round_quantity(symbol, quantity)
            required_usdt = quantity * price

            # Only borrow the shortfall, not the full amount
            available_usdt = self._get_free_margin_balance('USDT')
            shortfall = max(0.0, required_usdt - available_usdt)
            if shortfall > 0:
                self.client.create_margin_loan(asset='USDT', amount=shortfall)

            order = self.client.create_margin_order(
                symbol=symbol, side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET, quantity=quantity
            )
            executed_qty = float(order.get('executedQty', quantity))
            logger.debug(f"🟢 LIVE BUY │ {symbol} │ {executed_qty:.6f} @ ${price:.2f} │ Borrowed: ${shortfall:.2f}")

            self.positions[symbol] = {
                'type': PositionType.LONG, 'entry_price': price,
                'quantity': executed_qty, 'borrowed_amount': shortfall, 'borrowed_asset': 'USDT'
            }

            if self.performance_tracker:
                self.performance_tracker.record_trade(symbol, price, executed_qty, signal=signal, total_portfolio_value=total_portfolio_value)

            return True, {'symbol': symbol, 'price': price, 'quantity': executed_qty, 'trade_type': trade_type}

        except Exception as e:
            logger.error(f"❌ LONG open failed │ {symbol}: {e}")
            return False, {"error": str(e)}

    def open_short_position(self, symbol, quantity, trade_type, data=None, signal=None,
                            total_portfolio_value=None, balances=None) -> tuple[bool, dict]:
        try:
            price = data['close'].iloc[-1] if hasattr(data['close'], 'iloc') else data['close']
            quantity = abs(quantity)
            quantity = self._round_quantity(symbol, quantity)
            base_asset = symbol.replace('USDT', '').replace('BUSD', '')

            # Only borrow the shortfall
            available_base = self._get_free_margin_balance(base_asset)
            shortfall = max(0.0, quantity - available_base)
            if shortfall > 0:
                self.client.create_margin_loan(asset=base_asset, amount=shortfall)

            order = self.client.create_margin_order(
                symbol=symbol, side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET, quantity=quantity
            )
            executed_qty = float(order.get('executedQty', quantity))
            logger.debug(f"🔴 LIVE SELL │ {symbol} │ {executed_qty:.6f} @ ${price:.2f} │ Borrowed: {shortfall:.6f} {base_asset}")

            self.positions[symbol] = {
                'type': PositionType.SHORT, 'entry_price': price,
                'quantity': executed_qty, 'borrowed_amount': shortfall, 'borrowed_asset': base_asset
            }

            if self.performance_tracker:
                self.performance_tracker.record_trade(symbol, price, -executed_qty, signal=signal, total_portfolio_value=total_portfolio_value)

            return True, {'symbol': symbol, 'price': price, 'quantity': executed_qty, 'trade_type': trade_type}

        except Exception as e:
            logger.error(f"❌ SHORT open failed │ {symbol}: {e}")
            return False, {"error": str(e)}

    def close_position(self, symbol, data=None, signal=None, total_portfolio_value=None,
                       balances=None, trade_type='CLOSE') -> tuple[bool, dict]:
        if symbol not in self.positions:
            logger.error(f"❌ No position found for {symbol}")
            return False, {'error': f'No position for {symbol}'}
        try:
            price = data['close'].iloc[-1] if hasattr(data['close'], 'iloc') else data['close']
            position = self.positions[symbol]
            quantity = position['quantity']
            position_type = position['type']

            if position_type == PositionType.LONG:
                order = self.client.create_margin_order(symbol=symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_MARKET, quantity=quantity)
                if position['borrowed_amount'] > 0:
                    self.client.repay_margin_loan(asset='USDT', amount=position['borrowed_amount'])
            else:
                order = self.client.create_margin_order(symbol=symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=quantity)
                if position['borrowed_amount'] > 0:
                    self.client.repay_margin_loan(asset=position['borrowed_asset'], amount=position['borrowed_amount'])

            executed_qty = float(order.get('executedQty', quantity))
            closed_quantity = executed_qty if position_type == PositionType.LONG else -executed_qty
            logger.debug(f"⚪ LIVE CLOSE │ {symbol} │ {closed_quantity:.6f} @ ${price:.2f}")

            if self.performance_tracker:
                self.performance_tracker.record_trade(symbol, price, -closed_quantity, signal=signal, total_portfolio_value=total_portfolio_value)

            del self.positions[symbol]
            return True, {'symbol': symbol, 'price': price, 'quantity': closed_quantity, 'trade_type': trade_type}

        except Exception as e:
            logger.error(f"❌ CLOSE failed │ {symbol}: {e}")
            return False, {"error": str(e)}

    def _round_quantity(self, symbol, quantity): return round(quantity, 5)
    def _round_price(self, symbol, price): return round(price, 2)

class MockExecutionHandler(BaseExecutionHandler):

    def __init__(self, performance_tracker=None, portfolio_info=None,
                 exchange: str = "binance", market_type: str = "margin",
                 slippage_override: float | dict | None = None,
                 cost_model_path: str | None = None):
        """
        Applies flat basis-point slippage against the trade direction at fill
        time (E-010) -- buys fill above the bar close, sells below it; closing
        a LONG is economically a SELL (price down) and closing a SHORT is a
        buy-to-cover (price down's opposite -- price up).

        S3 (2026-09-10, "slippage becomes on-by-default, real per-symbol
        calibration"): slippage is no longer a single flat number threaded in
        at construction. A multi-symbol run needs a DIFFERENT bps value per
        trade's symbol (BTCUSDT vs ETHUSDT vs ...), so this handler resolves
        slippage_bps per trade, at fill time, from config/cost_model.json's
        (exchange, market_type, symbol) lookup -- see
        config/cost_model.py::resolve_cost_model and _resolve_slippage_bps
        below. exchange/market_type identify which cost_model.json entry to
        read; they default to "binance"/"margin", matching TradingParams' own
        defaults.

        slippage_override: test/research-only full-or-partial bypass of
        cost_model.json for this handler's slippage resolution (threaded from
        run_backtest's own cost_model_override -- see core/launcher.py).
        A flat float applies uniformly to every symbol with no fallback
        logging (an explicit deliberate override, not a calibration gap).
        A dict replaces cost_model.json's per-symbol table wholesale for the
        fill-time lookup -- same "default"-key fallback + logging behavior as
        the real table. None (default) reads the real committed
        cost_model.json. Never set by production callers.

        cost_model_path: test-only override of the cost_model.json path used
        at fill time (lets a fixture-backed handler avoid touching the
        committed file). None (default) -> the real committed
        config/cost_model.json.

        This is the single seam: the adjusted `price` computed here flows to BOTH
        downstream consumers (self.performance_tracker.record_trade and, via
        BaseExecutionHandler._post_order, self.portfolio_info.update_local_balance)
        automatically, since both already read this one returned value. Slippage
        must never be wired into performance/metrics.py or execution/portfolio_info.py
        directly -- that would double-apply it or let the two paths disagree.
        """
        super().__init__(performance_tracker=performance_tracker, portfolio_info=portfolio_info)
        self.exchange = exchange
        self.market_type = market_type
        self.slippage_override = slippage_override
        self.cost_model_path = cost_model_path

    def _resolve_slippage_bps(self, symbol: str) -> float:
        """Resolve this trade's slippage_bps, logging loudly if a per-symbol
        calibration is missing and the "default" fallback fires -- per S3's
        explicit requirement that a fallback never silently read as a
        calibrated number. See config/cost_model.py::resolve_cost_model."""
        if self.slippage_override is not None:
            if isinstance(self.slippage_override, dict):
                table = self.slippage_override
                if symbol in table:
                    return float(table[symbol])
                value = float(table["default"])
                logger.warning(
                    f"⚠ SLIPPAGE FALLBACK (override table) │ {symbol} │ "
                    f"{self.exchange}/{self.market_type}: no per-symbol override "
                    f"entry, using default={value} bps -- not a calibrated "
                    f"number for {symbol}"
                )
                return value
            return float(self.slippage_override)

        kwargs = {"path": self.cost_model_path} if self.cost_model_path else {}
        _fee_bps, slippage_bps, used_fallback = resolve_cost_model(
            self.exchange, self.market_type, symbol=symbol, **kwargs
        )
        if used_fallback:
            logger.warning(
                f"⚠ SLIPPAGE FALLBACK │ {symbol} │ {self.exchange}/{self.market_type}: "
                f"no calibrated per-symbol entry in cost_model.json, using "
                f"default={slippage_bps} bps -- not a calibrated number for {symbol}"
            )
        return slippage_bps

    def open_long_position(self, symbol, quantity, trade_type, data, signal=None,
                           total_portfolio_value=None, balances=None) -> tuple[bool, dict]:
        try:
            # A BUY -- buyer pays MORE (slippage_bps=0 -> price unchanged, byte-identical).
            slippage_bps = self._resolve_slippage_bps(symbol)
            price = data['close'].iloc[-1] * (1 + slippage_bps / 10000)
            logger.debug(f"🟢 MOCK BUY │ {symbol} │ {quantity:.6f} @ ${price:.2f} │ Cost: ${quantity * price:.2f}")
            self.executed_orders_counter += 1
            if self.performance_tracker:
                self.performance_tracker.record_trade(symbol, price, quantity, data['timestamp'].iloc[-1], signal, total_portfolio_value)
            return True, {'symbol': symbol, 'price': price, 'quantity': quantity, 'trade_type': trade_type}
        except Exception as e:
            logger.error(f"❌ MOCK BUY error: {e}", exc_info=True)
            return False, {"error": str(e)}

    def open_short_position(self, symbol, quantity, trade_type, data, signal=None,
                            total_portfolio_value=None, balances=None) -> tuple[bool, dict]:
        try:
            # A SELL -- seller receives LESS (slippage_bps=0 -> price unchanged).
            slippage_bps = self._resolve_slippage_bps(symbol)
            price = data['close'].iloc[-1] * (1 - slippage_bps / 10000)
            logger.debug(f"🔴 MOCK SELL │ {symbol} │ {quantity:.6f} @ ${price:.2f} │ Value: ${abs(quantity) * price:.2f}")
            self.executed_orders_counter += 1
            if self.performance_tracker:
                self.performance_tracker.record_trade(symbol, price, quantity, data['timestamp'].iloc[-1], signal, total_portfolio_value)
            return True, {'symbol': symbol, 'price': price, 'quantity': -quantity, 'trade_type': trade_type}
            #                                                                ↑ negate: quantity is negative, update_local_balance expects positive
        except Exception as e:
            logger.error(f"❌ MOCK SELL error: {e}", exc_info=True)
            return False, {"error": str(e)}

    def close_position(self, symbol, data, signal=None, total_portfolio_value=None,
                       balances=None, trade_type='CLOSE') -> tuple[bool, dict]:
        if symbol not in balances:
            logger.error(f"❌ No balance found for {symbol}")
            return False, {'error': f'No balance for {symbol}'}
        try:
            close = data['close'].iloc[-1]
            b = balances[symbol]
            position = b.get('free', 0.0) - b.get('locked', 0.0)
            slippage_bps = self._resolve_slippage_bps(symbol)
            # Closing a LONG (position > 0) is economically a SELL -- price down,
            # same adjustment as open_short_position. Closing a SHORT (position < 0)
            # is a buy-to-cover -- price up, same adjustment as open_long_position.
            # position == 0 (nothing to close) leaves price unadjusted -- unreachable
            # in practice since callers only invoke close_position on a nonzero book.
            if position > 0:
                price = close * (1 - slippage_bps / 10000)
            elif position < 0:
                price = close * (1 + slippage_bps / 10000)
            else:
                price = close
            logger.debug(f"⚪ MOCK CLOSE │ {symbol} │ {position:.6f} @ ${price:.2f} │ Value: ${position * price:.2f}")
            self.executed_orders_counter += 1
            if self.performance_tracker:
                self.performance_tracker.record_trade(symbol, price, -position, data['timestamp'].iloc[-1], signal, total_portfolio_value)
            return True, {'symbol': symbol, 'price': price, 'quantity': position, 'trade_type': trade_type}
        except Exception as e:
            logger.error(f"❌ MOCK CLOSE error: {e}", exc_info=True)
            return False, {"error": str(e)}
