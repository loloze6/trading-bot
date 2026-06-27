"""
run_protocol.py — walk-forward protocol runner.

CLI (run from repo root or strategy-research/):
  python strategy-research/tools/run_protocol.py <config_path> <protocol_path>
  python strategy-research/tools/run_protocol.py <config_path> <protocol_path> --holdout --i-understand
"""
import sys
import os
import json
import argparse
import statistics
import re
from datetime import datetime, timezone, date
from hashlib import sha256
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))   # strategy-research/tools/
_SR   = os.path.dirname(_HERE)                        # strategy-research/
_REPO = os.path.dirname(_SR)                          # repo root
_TBOT = os.path.join(_REPO, "trading-bot")            # trading-bot/

if _TBOT not in sys.path:
    sys.path.insert(0, _TBOT)

from core.launcher import run_backtest

_RESULTS_ROOT = os.path.join(_SR, "results")


def _config_sha(config_path: str):
    with open(config_path, encoding="utf-8") as f:
        cfg = json.load(f)
    canonical = json.dumps(cfg, sort_keys=True, separators=(",", ":"))
    digest = sha256(canonical.encode()).hexdigest()
    return digest, digest[:8]


def _protocol_run_id(sha8: str) -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + sha8


# ---------------------------------------------------------------------------
# Hypothesis-specific verdict evaluation (evaluate_against_decision_rules)
# ---------------------------------------------------------------------------

_UNTESTED_KEYWORDS = [
    'delta', 'walk-forward pe', 'holdout pe', ' pe ', ' lag',
    'conditional sharpe', 'regime-conditional', 'v5', 'reverse control',
    'parameter drift', 'generalization', 'buy-hold', 'buy.hold',
]

_KEYWORD_TO_FIELD = [
    (['mr frequency', 'mr freq', 'regime frequency', 'regime_frequency', 'mr regime'], 'regime_frequency'),
    (['win rate', 'win_rate', 'hit rate'],                          'median_win_rate'),
    (['sharpe'],                                                     'median_sharpe'),
    (['drawdown'],                                                   'max_abs_drawdown_pct'),
    (['trade count', 'trade_count', 'trades'],                      'min_trade_count'),
]

def _is_untested(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in _UNTESTED_KEYWORDS)

def _resolve_field(text: str):
    lower = text.lower()
    for keywords, field in _KEYWORD_TO_FIELD:
        if any(kw in lower for kw in keywords):
            return field
    return None

def _parse_op_value(text: str):
    m = re.search(r'([≥>≤<]=?)\s*([0-9]+\.?[0-9]*)\s*%?', text)
    if not m:
        return None, None
    op  = m.group(1).replace('≥', '>=').replace('≤', '<=')
    val = float(m.group(2))
    return op, val

def _apply_op(op: str, actual: float, threshold: float) -> bool:
    return {'>': actual > threshold, '>=': actual >= threshold,
            '<': actual < threshold, '<=': actual <= threshold}.get(op, False)

def _build_extended_summary(per_symbol_summary: dict, results: list) -> dict:
    """Augment per_symbol_summary with median_win_rate and regime_frequency."""
    extended = {s: dict(v) for s, v in per_symbol_summary.items()}
    for symbol in extended:
        rows = [r for r in results if r['symbol'] == symbol]
        win_rates = [r['core']['win_rate'] for r in rows
                     if r.get('core', {}).get('win_rate') is not None]
        extended[symbol]['median_win_rate'] = (
            round(statistics.median(win_rates), 4) if win_rates else None
        )
        # regime_frequency: requires per_regime in results (Step 3 adds this)
        freqs = []
        for r in rows:
            pr = r.get('per_regime')
            if pr:
                mr_bars = pr.get('mean_reversion', {}).get('bar_count', 0)
                total   = sum(v.get('bar_count', 0) for v in pr.values())
                if total > 0:
                    freqs.append(mr_bars / total * 100)  # as %, to match "≥ 5%" in text
        extended[symbol]['regime_frequency'] = (
            round(statistics.median(freqs), 4) if freqs else None
        )
    return extended

def _split_criteria(text: str) -> list:
    return [p.strip().rstrip('.')
            for p in re.split(r'\bAND\b|\bOR\b', text, flags=re.IGNORECASE)
            if p.strip()]

def _evaluate_criterion(text: str, extended: dict, is_reject: bool) -> dict:
    if _is_untested(text):
        return {'criterion': text, 'result': 'UNTESTED',
                'reason': 'not available in current metrics pipeline'}
    field = _resolve_field(text)
    if field is None:
        return {'criterion': text, 'result': 'UNTESTED',
                'reason': 'no matching metric keyword'}
    op, threshold = _parse_op_value(text)
    if op is None:
        return {'criterion': text, 'result': 'UNTESTED',
                'reason': 'could not parse numeric threshold'}
    per_symbol = []
    for symbol, vals in extended.items():
        actual = vals.get(field)
        if actual is None:
            per_symbol.append({'symbol': symbol, 'result': 'UNTESTED',
                                'reason': f'{field} not computed'})
            continue
        condition_met = _apply_op(op, actual, threshold)
        # approve: condition_met=True → PASS, False → FAIL
        # reject:  condition_met=True → FAIL, False → PASS  (D3)
        result = ('FAIL' if (is_reject and condition_met)
                         or (not is_reject and not condition_met)
                  else 'PASS')
        per_symbol.append({'symbol': symbol, 'actual': round(actual, 4),
                            'required': f'{op} {threshold}', 'result': result})
    overall = ('UNTESTED' if all(r['result'] == 'UNTESTED' for r in per_symbol)
               else 'FAIL'  if any(r['result'] == 'FAIL'    for r in per_symbol)
               else 'PASS')
    return {'criterion': text, 'field': field, 'required': threshold,
            'result': overall, 'per_symbol': per_symbol}

def evaluate_against_decision_rules(
    per_symbol_summary: dict,
    results: list,
    validation_protocol: dict,
) -> dict:
    """
    Evaluate per_symbol_summary against criteria from a loaded validation_protocol.yaml dict.
    Reads both decision_rules AND required_evidence (D1).
    Derives win_rate and regime_frequency from results list (D2).
    Reject criteria FAILing → kill; approve/evidence FAILing → refine only (D3).
    """
    extended = _build_extended_summary(per_symbol_summary, results)

    decision_rules    = validation_protocol.get('decision_rules', {})
    required_evidence = validation_protocol.get('required_evidence', []) or []

    # Fix 2: normalize required_evidence items — YAML parses "key: value" entries as
    # {key: value} dicts; convert back to "key: value" strings before evaluation.
    def _normalize_evidence_item(item) -> str:
        if isinstance(item, dict):
            k, v = next(iter(item.items()))
            return f"{k}: {v}"
        return str(item)
    required_evidence = [_normalize_evidence_item(i) for i in required_evidence]

    def _dict_to_criterion_text(d: dict) -> str:
        """Convert a multi-key criterion dict to a single evaluable string."""
        metric    = d.get('metric',    d.get('criterion', ''))
        operator  = d.get('operator',  d.get('op', ''))
        threshold = d.get('threshold', d.get('value', ''))
        window    = d.get('window', '')
        text = f"{metric}: {operator} {threshold}"
        if window:
            text += f" ({window})"
        return text

    # Handle three decision_rules formats:
    #   list of dicts  → new SKILL.md format; single-key {k:v} or multi-key {metric:,threshold:,...}
    #   dict with approve_if_all_met/reject_if_any_met lists → future structured format
    #   dict with approve/reject prose strings → run_010 legacy format
    if isinstance(decision_rules, list):
        approve_texts = []
        for item in decision_rules:
            if isinstance(item, dict):
                if len(item) == 1:
                    # Single-key {criterion_name: threshold_expr} — already works
                    k, v = next(iter(item.items()))
                    approve_texts.append(f"{k}: {v}")
                else:
                    # Multi-key {metric:, operator:, threshold:, ...} — reconstruct as one string
                    approve_texts.append(_dict_to_criterion_text(item))
            elif isinstance(item, str):
                # Plain-string criterion — process it (not a "summary note")
                approve_texts.append(item)
        reject_texts = []
    elif 'approve_if_all_met' in decision_rules:
        approve_texts = list(decision_rules['approve_if_all_met'])
        reject_texts  = list(decision_rules.get('reject_if_any_met', []))
    else:
        approve_texts = _split_criteria(decision_rules.get('approve', ''))
        reject_texts  = _split_criteria(decision_rules.get('reject',  ''))

    criteria_results = []
    approve_rows, reject_rows, evidence_rows = [], [], []

    for text in approve_texts:
        row = _evaluate_criterion(text, extended, is_reject=False)
        criteria_results.append(row); approve_rows.append(row)

    for text in reject_texts:
        row = _evaluate_criterion(text, extended, is_reject=True)
        criteria_results.append(row); reject_rows.append(row)

    for text in required_evidence:
        row = _evaluate_criterion(text, extended, is_reject=False)
        criteria_results.append(row); evidence_rows.append(row)

    # Fix 1: deduplicate — required_evidence often repeats criteria already in decision_rules.
    # Key is resolved metric field (e.g. 'median_sharpe') so that differently-worded
    # criteria for the same field collapse to one. UNTESTED rows (no field) fall back
    # to lowercased criterion text. First occurrence (decision_rules order) wins.
    seen = set()
    deduped = []
    for row in criteria_results:
        key = row.get('field') or row['criterion'].lower().strip()
        if key not in seen:
            seen.add(key)
            deduped.append(row)
    criteria_results = deduped
    row_ids = {id(r) for r in criteria_results}
    approve_rows  = [r for r in approve_rows  if id(r) in row_ids]
    reject_rows   = [r for r in reject_rows   if id(r) in row_ids]
    evidence_rows = [r for r in evidence_rows if id(r) in row_ids]

    reject_triggered  = any(r['result'] == 'FAIL' for r in reject_rows)
    approve_fails     = sum(1 for r in approve_rows + evidence_rows if r['result'] == 'FAIL')
    approve_evaluated = sum(1 for r in approve_rows + evidence_rows if r['result'] != 'UNTESTED')

    if reject_triggered:
        verdict = 'kill'
    elif approve_fails == 0 and approve_evaluated > 0:
        verdict = 'promote'
    else:
        verdict = 'refine'

    tested   = [r for r in criteria_results if r['result'] != 'UNTESTED']
    untested = [r for r in criteria_results if r['result'] == 'UNTESTED']
    fail_n   = sum(1 for r in tested if r['result'] == 'FAIL')

    # A4: diagnostics block — evidence for altitude decision by verdict_interpreter
    gross_pnls  = [r["core"].get("gross_pnl")              for r in results if r["core"].get("gross_pnl")              is not None]
    cost_drags  = [r["core"].get("cost_drag_pct")          for r in results if r["core"].get("cost_drag_pct")          is not None]
    corrs       = [r["core"].get("forecast_return_corr")   for r in results if r["core"].get("forecast_return_corr")   is not None]

    uninformative: list = []
    for r in results:
        for regime, stats in r.get("regime_validity", {}).items():
            if not stats.get("informative", True) and regime not in uninformative:
                uninformative.append(regime)

    # Use criteria_results (all evaluated criteria) so classification is robust even when
    # decision_rules uses string items that might route via evidence_rows instead of approve_rows.
    wr_rows     = [row for row in criteria_results if row.get("field") == "median_win_rate"]
    sharpe_rows = [row for row in criteria_results if row.get("field") == "median_sharpe"]
    wr_pass     = bool(wr_rows)     and all(r["result"] == "PASS" for r in wr_rows)
    sharpe_fail = bool(sharpe_rows) and any(r["result"] == "FAIL" for r in sharpe_rows)
    if wr_pass and sharpe_fail:
        wr_vs_sharpe = "win_rate PASS + sharpe FAIL"
    elif not wr_pass and sharpe_fail:
        wr_vs_sharpe = "both FAIL"
    else:
        wr_vs_sharpe = "both PASS or N/A"

    diagnostics = {
        "median_gross_pnl":            round(statistics.median(gross_pnls), 4) if gross_pnls else None,
        "median_cost_drag_pct":        round(statistics.median(cost_drags), 4) if cost_drags else None,
        "median_forecast_return_corr": round(statistics.median(corrs),      4) if corrs      else None,
        "uninformative_regimes":       uninformative,
        "win_rate_vs_sharpe":          wr_vs_sharpe,
    }

    return {
        'verdict':          verdict,
        'criteria_results': criteria_results,
        'verdict_reason':   f"{fail_n} of {len(tested)} evaluable criteria FAIL; "
                            f"{len(untested)} UNTESTED",
        'diagnostics':      diagnostics,
    }


def main():
    parser = argparse.ArgumentParser(description="Walk-forward protocol runner")
    parser.add_argument("config_path",   help="Path to strategy_config.json")
    parser.add_argument("protocol_path", help="Path to protocol JSON spec")
    parser.add_argument("--holdout",      action="store_true")
    parser.add_argument("--i-understand", action="store_true", dest="i_understand")
    parser.add_argument("--validation-protocol", default=None,
                        help="Path to validation_protocol.yaml for hypothesis-specific verdict")
    args = parser.parse_args()

    # Holdout gate: require BOTH flags or NEITHER
    if args.holdout != args.i_understand:
        print("ERROR: --holdout requires --i-understand (and vice versa). Pass both or neither.",
              file=sys.stderr)
        sys.exit(1)

    with open(args.protocol_path, encoding="utf-8") as f:
        protocol = json.load(f)

    config_sha256, config_sha8 = _config_sha(args.config_path)
    symbols = protocol["symbols"]
    os.makedirs(_RESULTS_ROOT, exist_ok=True)

    run_id = _protocol_run_id(config_sha8)
    out_dir = Path(_RESULTS_ROOT) / "protocols" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # HOLDOUT MODE
    # ------------------------------------------------------------------
    if args.holdout:
        h = protocol["holdout"]
        start = h["start"]
        end   = h["end"] if h["end"] is not None else date.today().isoformat()

        holdout_results = {}
        for symbol in symbols:
            print(f"[holdout] {symbol}  {start} to {end} ...")
            rd = run_backtest(args.config_path, symbol, start, end, _RESULTS_ROOT)
            with open(rd / "metrics.json", encoding="utf-8") as f:
                m = json.load(f)
            holdout_results[symbol] = {"run_id": rd.name, "core": m["core"]}

        payload = {
            "protocol_run_id": run_id,
            "config_sha256":   config_sha256,
            "holdout_window":  {"start": start, "end": end},
            "results":         holdout_results,
        }
        (out_dir / "holdout_result.json").write_text(
            json.dumps(payload, indent=2, default=str), encoding="utf-8"
        )
        print(f"Holdout result: {out_dir / 'holdout_result.json'}")

        log_path = Path(_RESULTS_ROOT) / "holdout_log.jsonl"
        line = {
            "utc":             datetime.now(timezone.utc).isoformat(),
            "config_sha256":   config_sha256,
            "protocol_run_id": run_id,
            "symbols_core":    {s: holdout_results[s]["core"] for s in symbols},
        }
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(line, default=str) + "\n")
        print(f"Appended to {log_path}")
        return

    # ------------------------------------------------------------------
    # NORMAL MODE — walk-forward windows
    # ------------------------------------------------------------------
    budget_path = Path(_RESULTS_ROOT) / "protocol_budget.jsonl"
    prior_runs = 0
    if budget_path.exists():
        with open(budget_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                entry = json.loads(line)
                if entry.get("config_sha256") == config_sha256:
                    prior_runs += entry.get("n_runs", 0)
    n_new = len(symbols) * len(protocol["windows"])
    print(f"Budget used for this config: {prior_runs}/20 scored runs")
    if prior_runs + n_new > 20:
        print(f"WARNING: this run adds {n_new}, bringing total to {prior_runs + n_new}/20 (over budget). Continuing.")

    results = []
    for symbol in symbols:
        for window in protocol["windows"]:
            label = window["label"]
            start = window["test"]["start"]
            end   = window["test"]["end"]
            print(f"  {symbol}  window={label}  {start} to {end} ...")
            rd = run_backtest(args.config_path, symbol, start, end, _RESULTS_ROOT)
            with open(rd / "metrics.json", encoding="utf-8") as f:
                m = json.load(f)
            core = m["core"]
            results.append({
                "symbol":          symbol,
                "window":          label,
                "run_id":          rd.name,
                "core":            core,
                "per_regime":      m.get("per_regime", {}),
                "regime_validity": m.get("regime_validity", {}),
            })
            print(f"    sharpe={core.get('sharpe', 0):.3f}  trades={core.get('trade_count', 0)}"
                  f"  dd={core.get('max_drawdown_pct', 0):.1f}%")

    # Per-symbol summary
    promo = protocol["promotion"]
    per_symbol = {}
    for symbol in symbols:
        rows     = [r for r in results if r["symbol"] == symbol]
        sharpes  = [r["core"]["sharpe"] for r in rows]
        dds      = [abs(r["core"]["max_drawdown_pct"]) for r in rows]
        trades   = [r["core"]["trade_count"] for r in rows]
        per_symbol[symbol] = {
            "median_sharpe":        round(statistics.median(sharpes), 4),
            "max_abs_drawdown_pct": round(max(dds), 4),
            "min_trade_count":      min(trades),
        }

    def _promote(s):
        p = per_symbol[s]
        return (p["median_sharpe"]        >  promo["median_sharpe_gt"]
                and p["max_abs_drawdown_pct"] <  promo["max_abs_drawdown_pct_lt"]
                and p["min_trade_count"]       >= promo["min_trade_count_gte"])

    def _kill(s):
        return per_symbol[s]["median_sharpe"] < promo["kill_median_sharpe_lt"]

    if all(_promote(s) for s in symbols):
        verdict = "promote"
        parts = [f"{s}: median_sharpe={per_symbol[s]['median_sharpe']:.3f}>0"
                 f" max_dd={per_symbol[s]['max_abs_drawdown_pct']:.1f}%<30"
                 f" min_trades={per_symbol[s]['min_trade_count']}>=20"
                 for s in symbols]
        verdict_reason = "; ".join(parts)
    elif all(_kill(s) for s in symbols):
        verdict = "kill"
        parts = [f"{s}: median_sharpe={per_symbol[s]['median_sharpe']:.3f}<-1" for s in symbols]
        verdict_reason = "both symbols below kill threshold: " + ", ".join(parts)
    else:
        verdict = "refine"
        parts = []
        for s in symbols:
            p = per_symbol[s]
            fails = []
            if p["median_sharpe"] <= promo["median_sharpe_gt"]:
                fails.append(f"median_sharpe={p['median_sharpe']:.3f}<=0")
            if p["max_abs_drawdown_pct"] >= promo["max_abs_drawdown_pct_lt"]:
                fails.append(f"max_dd={p['max_abs_drawdown_pct']:.1f}%>=30")
            if p["min_trade_count"] < promo["min_trade_count_gte"]:
                fails.append(f"min_trades={p['min_trade_count']}<20")
            if fails:
                parts.append(f"{s}: " + ", ".join(fails))
        verdict_reason = "; ".join(parts) if parts else "mixed — not all pass promote, not all fail at kill"

    hypothesis_verdict = None
    if args.validation_protocol:
        import yaml
        with open(args.validation_protocol, encoding="utf-8") as f:
            vp = yaml.safe_load(f)
        hypothesis_verdict = evaluate_against_decision_rules(per_symbol, results, vp)
        print(f"Hypothesis verdict : {hypothesis_verdict['verdict']}")
        print(f"Reason             : {hypothesis_verdict['verdict_reason']}")

    summary = {
        "protocol_run_id":    run_id,
        "config_sha256":      config_sha256,
        "protocol_file":      args.protocol_path,
        "results":            results,
        "per_symbol_summary": per_symbol,
        "verdict":            verdict,
        "verdict_reason":     verdict_reason,
        "hypothesis_verdict": hypothesis_verdict,
    }
    (out_dir / "protocol_summary.json").write_text(
        json.dumps(summary, indent=2, default=str), encoding="utf-8"
    )
    print(f"\nProtocol summary: {out_dir / 'protocol_summary.json'}")
    print(f"Verdict : {verdict}")
    print(f"Reason  : {verdict_reason}")

    # Task 5.4 — append to budget log
    budget_entry = {
        "utc":             datetime.now(timezone.utc).isoformat(),
        "config_sha256":   config_sha256,
        "protocol_run_id": run_id,
        "n_runs":          n_new,
    }
    with open(budget_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(budget_entry, default=str) + "\n")
    print(f"Budget log: {budget_path}")


if __name__ == "__main__":
    main()
