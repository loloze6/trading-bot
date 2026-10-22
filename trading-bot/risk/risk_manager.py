import math
import time
import logging
from typing import Any, Dict, List, Optional, Union, Tuple

logger = logging.getLogger("trading_bot")

"""
Risk Management Module
======================
Controls position sizing, allocation limits, and trade approval.

Classes:
    - RiskManager: Risk management with trade frequency limits
"""

class RiskManager:
    """
    Risk manager for live trading.
    
    Features:
        - Validates allocation changes (min limit)
    """

    def __init__(self, controls_cfg: dict):
        self.controls = controls_cfg

    def approve_allocation_change(self, symbol, change, data, signal_change=None):
        """signal_change (D-176): with a strategies.sizing block the caller
        passes the change in the UNSIZED signal allocation (forecast / 10)
        since the position was last set. The min_allocation_change band then
        passes when EITHER the signal's change OR `change` (the sized order
        delta: target sized allocation minus the current position) reaches the
        threshold, the same 1e-6 tolerance for both (operator ruling on the
        D-176 safety review). The pre-D-176 judgement of the sized change is
        kept as a subset and the signal path is added, so a volatility move
        alone, or a restart with the book far from its sized target, still
        re-centres the position. The band's debug entry then also records
        passed_on ("signal" | "sized" | "both"; None when refused). A
        non-finite value never passes on its own path: a non-finite
        signal_change leaves the sized change judged alone (a de-risking sized
        move is not refused because of it). None (the default; every caller
        without a sizing block) leaves every control's input exactly `change`
        and every debug entry exactly as before D-176."""
        time = data['timestamp'].iloc[-1]
        debug = {"symbol": symbol, "time": time, "controls": {}}

        for name, params in self.controls.items():
            method = getattr(self, f"_ctrl_{name}", None)
            if not method:
                continue
            if name == "min_allocation_change" and signal_change is not None:
                passed, passed_on = self._min_allocation_change_signal_or_sized(
                    change, signal_change, symbol, params)
                debug["controls"][name] = {"passed": passed, "passed_on": passed_on}
                if not passed: return False, debug
                continue
            passed = method(change, symbol, params)
            debug["controls"][name] = {
                "passed": passed,
                }
            if not passed: return False, debug
        return True, debug 

    def _ctrl_min_allocation_change(self, change, symbol, p):
        if abs(change) < p["threshold"] - 1e-6:
            logger.warning(f"RISK MANAGER - |{change:.3f}| < threshold {p['threshold']} for {symbol}")
            return False
        return True

    def _min_allocation_change_signal_or_sized(self, change, signal_change, symbol, p):
        """D-176 band with a sizing block: passes when |signal_change| or
        |change| reaches p["threshold"], with _ctrl_min_allocation_change's
        1e-6 tolerance. A non-finite value never passes on its own path.
        Returns (passed, passed_on)."""
        floor = p["threshold"] - 1e-6
        on_signal = math.isfinite(signal_change) and abs(signal_change) >= floor
        on_sized = math.isfinite(change) and abs(change) >= floor
        if on_signal and on_sized:
            return True, "both"
        if on_signal:
            return True, "signal"
        if on_sized:
            return True, "sized"
        logger.warning(
            f"RISK MANAGER - signal |{signal_change:.3f}| and sized |{change:.3f}| "
            f"< threshold {p['threshold']} for {symbol}")
        return False, None