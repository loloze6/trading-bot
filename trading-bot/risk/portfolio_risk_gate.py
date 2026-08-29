"""
Portfolio Risk Gate
===================
Off-by-default portfolio-level risk controls that run in the per-bar pipeline
around the forecast -> allocation -> Δ map (see core/trading_bot.py::
_process_symbol_candle_completion). Additive to, and independent of, RiskManager:
RiskManager keeps enforcing the per-trade allocation-change band ("0.2 <= |Δ| <=
4.0"); this gate constrains the target ALLOCATION itself and can force the book
flat.

Controls:
  absolute_allocation_cap (PR-1) -- stateless clamp of the target allocation to
    [-cap, +cap].
  max_drawdown_kill (PR-2) -- stateful, terminal. Tracks the running peak of
    decision-time equity; on drawdown >= threshold it LATCHES for the rest of the
    run, forcing the target to 0 every bar. The flatten is routed through the
    DIRECT execution path (see core/trading_bot.py) so the min-Δ band cannot block
    it. Un-latching is human (a fresh run).
  daily_loss_limit (PR-2) -- stateful, day-scoped. Anchors day-start equity per
    Europe/Paris calendar day (tz-aware, derived from the UTC bar timestamp); on
    intraday loss >= threshold it halts (forces flat) for the remainder of that
    Paris day and re-arms at the next Paris-midnight rollover with a fresh anchor.

Config home is config.json's risk_management.portfolio_controls -- deliberately a
separate sibling of risk_management.controls (RiskManager's band) so the two
dispatch tables never mix. Absent block or absent key = that control off, so a
config that carries no portfolio_controls builds no gate and leaves every output
byte-identical.

zoneinfo is imported LAZILY inside the daily-loss day-key derivation and the
validator's tz check, NEVER at module top: requirements.txt gained tzdata for
Windows, but a default-OFF run (or a cap-/drawdown-only run that never configures
daily_loss_limit) must never touch the tz database, so a missing tzdata can only
ever fail a run that has daily_loss_limit actually configured -- fail-loud at the
right boundary.
"""

import copy
import math

import pandas as pd

# Controls implemented across PR-1 (cap) and PR-2 (the stateful pair). A config
# that names anything outside this set is an unknown key and fails loud rather
# than silently arming a safety control that does nothing.
_KNOWN_CONTROLS = {"absolute_allocation_cap", "max_drawdown_kill", "daily_loss_limit"}


def _threshold_errors(control: str, threshold) -> list[str]:
    """Shared fraction check for the stateful controls: a finite number in (0, 1)."""
    # bool is an int subclass -- reject it explicitly so True never reads as 1.0.
    if (
        isinstance(threshold, bool)
        or not isinstance(threshold, (int, float))
        or not math.isfinite(threshold)
        or not (0 < threshold < 1)
    ):
        return [f"{control}.threshold must be a finite number in (0, 1), got {threshold!r}"]
    return []


def _tz_error(tz) -> list[str]:
    """Validate a tz string by resolving it via ZoneInfo (lazy import, so a
    tzdata-less box only ever hits this when daily_loss_limit configures a tz)."""
    if not isinstance(tz, str):
        return [f"daily_loss_limit.tz must be a string, got {tz!r}"]
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

    try:
        ZoneInfo(tz)
    except (ZoneInfoNotFoundError, ValueError):
        return [f"daily_loss_limit.tz is not a known timezone: {tz!r}"]
    return []


def _iso(data_time) -> str:
    """Stable string form of a bar-close timestamp for trip telemetry."""
    return str(pd.Timestamp(data_time))


def validate_portfolio_controls(cfg) -> list[str]:
    """Return a list of human-readable errors for a portfolio_controls block.

    Empty list == valid. Shared by ConfigManager.validate (config.json path) and
    run_backtest's risk_controls override path so both entry points enforce one
    rule set. Unknown keys are errors (fail loud): a typo like "absolute_allocaton_cap"
    would otherwise leave the intended control silently off.
    """
    if not isinstance(cfg, dict):
        return [f"portfolio_controls must be a dict, got {type(cfg).__name__}"]

    errors: list[str] = []

    unknown = set(cfg) - _KNOWN_CONTROLS
    if unknown:
        errors.append(f"unknown portfolio_controls key(s): {sorted(unknown)}; known: {sorted(_KNOWN_CONTROLS)}")

    cap_cfg = cfg.get("absolute_allocation_cap")
    if cap_cfg is not None:
        if not isinstance(cap_cfg, dict):
            errors.append('absolute_allocation_cap must be a dict, e.g. {"cap": 1.0}')
        else:
            cap_unknown = set(cap_cfg) - {"cap"}
            if cap_unknown:
                errors.append(f"unknown absolute_allocation_cap key(s): {sorted(cap_unknown)}")
            if "cap" not in cap_cfg:
                errors.append('absolute_allocation_cap requires a "cap" value')
            else:
                cap = cap_cfg["cap"]
                # bool is an int subclass -- reject it explicitly so True never
                # reads as cap=1.0.
                if isinstance(cap, bool) or not isinstance(cap, (int, float)) or not math.isfinite(cap) or cap <= 0:
                    errors.append(f"absolute_allocation_cap.cap must be a finite number > 0, got {cap!r}")

    dd_cfg = cfg.get("max_drawdown_kill")
    if dd_cfg is not None:
        if not isinstance(dd_cfg, dict):
            errors.append('max_drawdown_kill must be a dict, e.g. {"threshold": 0.25}')
        else:
            dd_unknown = set(dd_cfg) - {"threshold"}
            if dd_unknown:
                errors.append(f"unknown max_drawdown_kill key(s): {sorted(dd_unknown)}")
            if "threshold" not in dd_cfg:
                errors.append('max_drawdown_kill requires a "threshold" value')
            else:
                errors += _threshold_errors("max_drawdown_kill", dd_cfg["threshold"])

    dl_cfg = cfg.get("daily_loss_limit")
    if dl_cfg is not None:
        if not isinstance(dl_cfg, dict):
            errors.append('daily_loss_limit must be a dict, e.g. {"threshold": 0.05, "tz": "Europe/Paris"}')
        else:
            dl_unknown = set(dl_cfg) - {"threshold", "tz"}
            if dl_unknown:
                errors.append(f"unknown daily_loss_limit key(s): {sorted(dl_unknown)}")
            if "threshold" not in dl_cfg:
                errors.append('daily_loss_limit requires a "threshold" value')
            else:
                errors += _threshold_errors("daily_loss_limit", dl_cfg["threshold"])
            if "tz" in dl_cfg:
                errors += _tz_error(dl_cfg["tz"])

    return errors


class PortfolioRiskGate:
    """Owns the portfolio_controls state for one backtest/live run.

    Built only when the effective portfolio_controls block is non-empty (see
    core/launcher.py); an absent block builds no gate and the per-bar hook is
    never entered. One gate instance per run.

    Two-phase per-bar contract (see core/trading_bot.py::
    _process_symbol_candle_completion):
      observe(data_time, equity)  -- update peak / daily anchor from this bar's
        decision-time equity, evaluate the stateful trips, latch. Reads only this
        bar's close-derived equity and its own past state -> no look-ahead.
      apply(target_allocation)    -- override the target to 0 while latched flat,
        else clamp to the cap; return (final_target, per-bar extras).
    """

    def __init__(self, portfolio_controls_cfg: dict, *, tz_default: str = "Europe/Paris"):
        errors = validate_portfolio_controls(portfolio_controls_cfg)
        if errors:
            # Defense in depth behind the validator wired into both entry points.
            raise ValueError("invalid portfolio_controls: " + "; ".join(errors))

        # The effective block, echoed verbatim into run provenance (config hash +
        # manifest) and metrics.json so a run WITH controls is distinguishable from
        # one without. Deep-copied so a caller mutating its input dict after build
        # cannot silently change the recorded provenance.
        self.config = copy.deepcopy(portfolio_controls_cfg)

        cap_cfg = portfolio_controls_cfg.get("absolute_allocation_cap")
        self.cap = float(cap_cfg["cap"]) if cap_cfg is not None else None

        dd_cfg = portfolio_controls_cfg.get("max_drawdown_kill")
        self.dd_threshold = float(dd_cfg["threshold"]) if dd_cfg is not None else None

        dl_cfg = portfolio_controls_cfg.get("daily_loss_limit")
        self.dl_threshold = float(dl_cfg["threshold"]) if dl_cfg is not None else None
        self.tz = dl_cfg.get("tz", tz_default) if dl_cfg is not None else tz_default

        # max_drawdown_kill state (terminal latch).
        self.peak_equity = None
        self.killed = False
        self.kill_ts = None

        # daily_loss_limit state (day-scoped, re-arms at Paris rollover).
        self.day_key = None
        self.day_start_equity = None
        self.daily_halted = False

        # Trip telemetry + per-bar counters (source of truth for the metrics block;
        # the Paris dates in daily_trips are derived here so the tz logic has one
        # home).
        self.trip_log: list[dict] = []
        self.n_bars_killed = 0
        self.n_bars_daily_halted = 0

        # This bar's recorded telemetry (set by observe, read by apply).
        self._bar_drawdown = None
        self._bar_daily_loss = None
        self._bar_trip = None

    def _paris_day(self, data_time):
        """Calendar day of `data_time` in self.tz. Lazy zoneinfo import (only
        reached when daily_loss_limit is configured). The bar timestamp is a candle
        CLOSE, so the day key uses only data timestamped at this bar -- no
        look-ahead."""
        from zoneinfo import ZoneInfo

        ts = pd.Timestamp(data_time)
        ts = ts.tz_localize("UTC") if ts.tz is None else ts.tz_convert("UTC")
        return ts.tz_convert(ZoneInfo(self.tz)).date()

    def observe(self, data_time, equity: float) -> None:
        """Fold this bar's decision-time equity into the stateful controls.

        `equity` is total_portfolio_value at core/trading_bot.py's pre-rebalance
        mark-to-market (funding-adjusted when model_funding is on), derived from
        this bar's close only. No-op when only the stateless cap (or nothing) is
        configured, so a cap-only run never touches equity tracking or zoneinfo.
        """
        if self.dd_threshold is None and self.dl_threshold is None:
            return

        # Fail loud on a degenerate book: a non-finite or non-positive equity makes
        # every drawdown / daily-loss fraction meaningless (and would divide by a
        # zero anchor). Never a legitimate decision-time equity in a solvent run.
        if not math.isfinite(equity) or equity <= 0:
            raise ValueError(f"PortfolioRiskGate.observe got non-finite/non-positive equity {equity!r}")

        self._bar_drawdown = None
        self._bar_daily_loss = None
        self._bar_trip = None

        # (b) max_drawdown_kill -- evaluated first so that if both trip on the same
        # bar the KILL is the recorded cause.
        if self.dd_threshold is not None:
            if self.peak_equity is None or equity > self.peak_equity:
                self.peak_equity = equity
            drawdown = (self.peak_equity - equity) / self.peak_equity
            self._bar_drawdown = drawdown
            if not self.killed and drawdown >= self.dd_threshold:
                self.killed = True
                self.kill_ts = _iso(data_time)
                self._bar_trip = "max_drawdown_kill"
                self.trip_log.append({"control": "max_drawdown_kill", "timestamp": self.kill_ts, "day": None})

        # (c) daily_loss_limit -- day-scoped. Guarded by `not self.killed`: once the
        # terminal kill latches we are flat to run end, so a daily trip is
        # unreachable (kill dominates the "both trip" and "already latched" cases).
        if self.dl_threshold is not None:
            day = self._paris_day(data_time)
            anchor = self.day_start_equity
            if self.day_key != day or anchor is None:
                self.day_key = day
                self.day_start_equity = anchor = equity
                self.daily_halted = False
            daily_loss = (anchor - equity) / anchor
            self._bar_daily_loss = daily_loss
            if not self.killed and not self.daily_halted and daily_loss >= self.dl_threshold:
                self.daily_halted = True
                if self._bar_trip is None:
                    self._bar_trip = "daily_loss_limit"
                self.trip_log.append(
                    {
                        "control": "daily_loss_limit",
                        "timestamp": _iso(data_time),
                        "day": str(day),
                    }
                )

        if self.killed:
            self.n_bars_killed += 1
        if self.daily_halted:
            self.n_bars_daily_halted += 1

    def apply(self, target_allocation: float) -> tuple[float, dict]:
        """Constrain this bar's target allocation and report what the gate did.

        While latched flat (killed or daily-halted) the target is forced to 0.0 --
        the caller then routes the resulting Δ through the DIRECT execution path so
        the min-Δ band cannot block the flatten. Otherwise the cap clamps the
        target. Returns (final_target, extras); extras rides record_state's
        **extras into portfolio_states.csv/bars.csv.

        Reads only this bar's target plus gate state that observe() updated from
        data timestamped <= this bar's close, so it introduces no look-ahead.
        """
        raw = target_allocation
        # Fail loud on a degenerate target: NaN passes any clamp unchanged AND
        # mislabels risk_cap_clamped True (nan != nan). Never a legitimate
        # allocation. (inf IS clamped by the cap below and is left to that path.)
        if math.isnan(raw):
            raise ValueError("PortfolioRiskGate.apply got a NaN target_allocation")

        if self.killed or self.daily_halted:
            final = 0.0
            cap_clamped = False
        elif self.cap is not None:
            final = min(max(raw, -self.cap), self.cap)
            cap_clamped = final != raw
        else:
            final = raw
            cap_clamped = False

        extras = {"risk_target_raw": raw, "risk_cap_clamped": cap_clamped}
        if self.dd_threshold is not None:
            extras["risk_killed"] = self.killed
            extras["risk_drawdown"] = self._bar_drawdown
        if self.dl_threshold is not None:
            extras["risk_daily_halted"] = self.daily_halted
            extras["risk_daily_loss"] = self._bar_daily_loss
        if self.dd_threshold is not None or self.dl_threshold is not None:
            extras["risk_trip"] = self._bar_trip
        return final, extras

    def stateful_summary(self) -> dict:
        """Metrics-block contribution for the stateful controls (empty for a
        cap-only gate, so its metrics block stays byte-identical to PR-1)."""
        out: dict = {}
        if self.dd_threshold is not None:
            out["n_bars_killed"] = self.n_bars_killed
        if self.dl_threshold is not None:
            out["n_bars_daily_halted"] = self.n_bars_daily_halted
        if self.dd_threshold is not None or self.dl_threshold is not None:
            first = self.trip_log[0] if self.trip_log else None
            out["first_trip"] = (
                {"control": first["control"], "timestamp": first["timestamp"]} if first is not None else None
            )
            out["daily_trips"] = [e["day"] for e in self.trip_log if e["control"] == "daily_loss_limit"]
        return out
