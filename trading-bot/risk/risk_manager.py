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
        - Validates allocation changes (min/max limits)
    """

    def __init__(self, controls_cfg: dict):
        self.controls = controls_cfg

    def approve_allocation_change(self, symbol, change, data):
        time = data['timestamp'].iloc[-1]
        debug = {"symbol": symbol, "time": time, "controls": {}}

        for name, params in self.controls.items():
            method = getattr(self, f"_ctrl_{name}", None)
            if not method:
                continue
            passed = method(change, symbol, params)
            debug["controls"][name] = {
                "passed": passed,
                }
            if not passed: return False, debug
        return True, debug 

    def _ctrl_max_allocation_change(self, change, symbol, p):
        if abs(change) > p["max"] + 1e-6:
            logger.warning(f"RISK MANAGER - |{change:.3f}| > max {p['max']} for {symbol}")
            return False
        return True

    def _ctrl_min_allocation_change(self, change, symbol, p):
        if abs(change) < p["threshold"] - 1e-6:
            logger.warning(f"RISK MANAGER - |{change:.3f}| < threshold {p['threshold']} for {symbol}")
            return False
        return True