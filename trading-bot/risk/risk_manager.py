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
        since the position was last set, and the min_allocation_change band
        judges that instead of `change` (the sized order delta). None (the
        default; every caller without a sizing block) leaves every control's
        input exactly `change`, byte-identical to before. A non-finite
        signal_change is refused (a NaN must never pass the band)."""
        time = data['timestamp'].iloc[-1]
        debug = {"symbol": symbol, "time": time, "controls": {}}

        for name, params in self.controls.items():
            method = getattr(self, f"_ctrl_{name}", None)
            if not method:
                continue
            if name == "min_allocation_change" and signal_change is not None:
                passed = math.isfinite(signal_change) and method(signal_change, symbol, params)
            else:
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