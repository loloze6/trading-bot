"""
Portfolio Risk Gate
===================
Off-by-default portfolio-level risk controls that run in the per-bar pipeline
BEFORE the forecast -> allocation -> Δ map (see core/trading_bot.py::
_process_symbol_candle_completion). Additive to, and independent of, RiskManager:
RiskManager keeps enforcing the per-trade allocation-change band ("0.2 <= |Δ| <=
4.0"); this gate constrains the target ALLOCATION itself.

PR-1 (fix/risk-layer) ships one control: absolute_allocation_cap, a stateless
clamp of the target allocation to [-cap, +cap]. The stateful pair
(max_drawdown_kill, daily_loss_limit) and the Europe/Paris tz machinery they need
are PR-2; this module's shape (config sub-block, observe/apply split at the call
site, the validate_portfolio_controls key set) is what they slot into.

Config home is config.json's risk_management.portfolio_controls -- deliberately a
separate sibling of risk_management.controls (RiskManager's band) so the two
dispatch tables never mix. Absent block or absent key = that control off, so a
config that carries no portfolio_controls builds no gate and leaves every output
byte-identical.
"""

import copy
import math

# Controls implemented in this PR. max_drawdown_kill and daily_loss_limit join
# this set in PR-2; until then a config that names them is an unknown key and
# fails loud rather than silently arming a safety control that does nothing.
_KNOWN_CONTROLS = {"absolute_allocation_cap"}


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

    return errors


class PortfolioRiskGate:
    """Owns the portfolio_controls state for one backtest/live run.

    Built only when the effective portfolio_controls block is non-empty (see
    core/launcher.py); an absent block builds no gate and the per-bar hook is
    never entered. One gate instance per run.
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

        # PR-2 scaffolding: max_drawdown_kill / daily_loss_limit state (peak_equity,
        # killed, day_key, day_start_equity, daily_halted) and the zoneinfo day-key
        # derivation that consumes tz_default land here without changing this
        # signature. Accepted now, unused in PR-1.
        _ = tz_default

    def apply(self, target_allocation: float) -> tuple[float, dict]:
        """Constrain this bar's target allocation and report what the gate did.

        Returns (final_target, extras). extras rides record_state's **extras into
        portfolio_states.csv/bars.csv so the gate's per-bar effect is auditable.
        Stateless in PR-1: reads only this bar's target, no prior-bar or future
        data (the no-lookahead argument is asserted in
        tests/test_portfolio_risk_gate.py).
        """
        raw = target_allocation
        # Fail loud on a degenerate target: NaN passes any clamp unchanged AND mislabels
        # risk_cap_clamped True (nan != nan), so it would silently corrupt the recorded
        # series and the exposure it drives. Never a legitimate allocation. (inf IS
        # clamped by the cap below and is left to that path deliberately.)
        if math.isnan(raw):
            raise ValueError("PortfolioRiskGate.apply got a NaN target_allocation")
        final = raw
        if self.cap is not None:
            final = min(max(raw, -self.cap), self.cap)
        return final, {"risk_target_raw": raw, "risk_cap_clamped": final != raw}
