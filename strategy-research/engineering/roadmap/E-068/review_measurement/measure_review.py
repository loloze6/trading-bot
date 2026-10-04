"""E-068 3b, item 6: the offline measurement of the claim-test review.

Runs the review (orchestrator.claim_test_review) on three known cards, twice
each, with REAL LLM calls, using the SAME prompt builder, call function and
answer check the pipeline uses (run_phase1_research._claim_review_prompt,
_invoke_reader_llm, _validate_claim_review). The review ships only if all six
calls meet their expectation (fixed before the first call):

  A  run_070 attempt-2 retry card: 1h bars, statement "the next 1 to 10 days",
     horizons [1, 2, 5, 10] bars (= 1 to 10 HOURS) -> MUST flag the units
     (some test has horizon_units_ok: false).
  B  run_070 attempt-0 card: 1h bars, "the next 1-4 hours", horizons [1, 2, 4]
     -> the control: MUST NOT flag the units (every horizon_units_ok: true).
  C  run_070's final card + block manifest: both tests select on the close's
     LEVEL (a 100-bar quantile), the statement is about the 1h MOVE -> MUST
     flag it (every close-selector test has measures_statement: false).

A and B never reached 1b, so they get a stated synthetic forecast manifest
(inputs/<case>/block_manifest.yaml). Outputs are written ONLY under this
folder (inputs/, work/, raw/, summary.*), never under runs/; any input path
inside a holdout store is refused.

Usage (from anywhere): <python> measure_review.py [--repeats 2]
"""
from __future__ import annotations

import argparse
import asyncio
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SR = HERE.parents[3]                                   # strategy-research/
sys.path.insert(0, str(SR / "workflow"))
sys.path.insert(0, str(SR / "tools"))

import yaml  # noqa: E402

TEMP_CASES = Path("C:/Users/alauz/AppData/Local/Temp/e068_validation")
MAIN_RUN_070 = Path("C:/Users/alauz/Documents/Projects/trading-bot/strategy-research/runs/"
                    "run_070/artifacts")
SYNTHETIC_MANIFEST = {
    "block": {"kind": "forecast",
              "config_paths": ["/strategies/regimes/unknown/components/0"]},
    "scaffolding": ["/regime_detector"],
    "rationale": ("SYNTHETIC (offline review measurement): this card never reached step 1b; "
                  "its signal is taken as one forecast component."),
}
CASES = {
    "A": {"card": TEMP_CASES / "hypothesis_card_2_retry.yaml", "manifest": None,
          "expect": "units_flagged"},
    "B": {"card": TEMP_CASES / "hypothesis_card_attempt0.yaml", "manifest": None,
          "expect": "units_not_flagged"},
    "C": {"card": MAIN_RUN_070 / "hypothesis_card.yaml",
          "manifest": MAIN_RUN_070 / "block_manifest.yaml",
          "expect": "level_not_move_flagged"},
}
HOLDOUT_DIR_NAME = "holdout_sealed"


def _refuse_holdout(path: Path) -> None:
    if HOLDOUT_DIR_NAME in Path(path).resolve().parts:
        raise SystemExit(f"refusing to read a holdout store: {path}")


def _inside(child: Path, parent: Path) -> bool:
    try:
        Path(child).resolve().relative_to(Path(parent).resolve())
        return True
    except ValueError:
        return False


def prepare(case: str, rpr) -> tuple:
    """Copy the case's inputs under inputs/<case>/ and lay out a scratch run
    directory work/<case>/artifacts/ (never under runs/)."""
    spec = CASES[case]
    for p in (spec["card"], spec["manifest"]):
        if p is not None:
            _refuse_holdout(p)
    inputs = HERE / "inputs" / case
    inputs.mkdir(parents=True, exist_ok=True)
    if not (inputs / "hypothesis_card.yaml").exists():
        shutil.copyfile(spec["card"], inputs / "hypothesis_card.yaml")
    if not (inputs / "block_manifest.yaml").exists():
        if spec["manifest"] is None:
            (inputs / "block_manifest.yaml").write_text(
                yaml.safe_dump(SYNTHETIC_MANIFEST, sort_keys=False), encoding="utf-8")
        else:
            shutil.copyfile(spec["manifest"], inputs / "block_manifest.yaml")
    work = HERE / "work" / case
    if _inside(work, SR / "runs"):
        raise SystemExit("refusing to write under runs/")
    (work / "artifacts").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(inputs / "block_manifest.yaml", work / "artifacts" / "block_manifest.yaml")
    text = (inputs / "hypothesis_card.yaml").read_text(encoding="utf-8")
    try:
        card = yaml.safe_load(text)
    except yaml.YAMLError:
        # The attempt-0 card (case B) is not valid YAML as a whole (unquoted
        # colons in its prose fields). The review reads only hypothesis_id,
        # timeframe and the `claim` block, so exactly those are parsed: the
        # top-level `claim:` block on its own, the two scalars by line.
        card = _parse_review_fields(text)
    (work / "artifacts" / "hypothesis_card.yaml").write_text(
        yaml.safe_dump(card, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return work, card


def _parse_review_fields(text: str) -> dict:
    lines = text.splitlines()
    out = {}
    for key in ("hypothesis_id", "timeframe"):
        hit = [ln for ln in lines if ln.startswith(f"{key}:")]
        if len(hit) != 1:
            raise SystemExit(f"cannot read {key} from the card")
        out[key] = yaml.safe_load(hit[0])[key]
    start = [i for i, ln in enumerate(lines) if ln.startswith("claim:")]
    if len(start) != 1:
        raise SystemExit("cannot find one top-level claim: block")
    end = start[0] + 1
    while end < len(lines) and (not lines[end].strip() or lines[end][:1] in (" ", "#")):
        end += 1
    out["claim"] = yaml.safe_load("\n".join(lines[start[0]:end]))["claim"]
    return out


def judge(expect: str, rows, card: dict) -> tuple:
    """(meets the expectation, why)."""
    if rows is None:
        return False, "invalid answer (review_error)"
    if expect == "units_flagged":
        hit = [n for n, r in rows.items() if r["horizon_units_ok"] is False]
        return bool(hit), f"horizon_units_ok false on {hit}" if hit else "no units flag"
    if expect == "units_not_flagged":
        bad = [n for n, r in rows.items() if r["horizon_units_ok"] is not True]
        return not bad, "every horizon_units_ok true" if not bad else f"flagged on {bad}"
    if expect == "level_not_move_flagged":
        close_tests = [t["name"] for t in card["claim"]["tests"]
                       if (t.get("selector") or {}).get("field") == "close"]
        missed = [n for n in close_tests if rows[n]["measures_statement"] is not False]
        return (not missed and bool(close_tests),
                "every close-level test flagged" if not missed else f"not flagged: {missed}")
    raise ValueError(expect)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repeats", type=int, default=2)
    ap.add_argument("--tag", default="run1", help="output sub-folder name (raw/<tag>/)")
    a = ap.parse_args(argv)
    os.chdir(SR)                    # _build_stage_prompt reads ./workflow_artifacts/skills
    import run_phase1_research as rpr

    raw_dir = HERE / "raw" / a.tag
    raw_dir.mkdir(parents=True, exist_ok=True)
    rows_out = []
    for case in CASES:
        work, card = prepare(case, rpr)
        names = rpr._claim_test_names(card.get("claim"))
        prompt = rpr._claim_review_prompt(work, card)
        (raw_dir / f"prompt_{case}.txt").write_text(prompt, encoding="utf-8")
        for i in range(1, a.repeats + 1):
            text, meta = asyncio.run(rpr._invoke_reader_llm(prompt))
            (raw_dir / f"{case}_{i}.txt").write_text(text or "", encoding="utf-8")
            rows, error = rpr._validate_claim_review(text, names)
            ok, why = judge(CASES[case]["expect"], rows, card)
            tokens = rpr._usage_token_record(meta.get("usage") or {})
            rows_out.append({
                "case": case, "call": i, "expect": CASES[case]["expect"], "pass": ok,
                "why": why, "review_error": error,
                "flags": ({n: {k: r[k] for k in rpr._CLAIM_REVIEW_FLAGS} for n, r in rows.items()}
                          if rows else None),
                "cost_usd": meta.get("cost_usd"), "tokens": tokens,
                "num_turns": meta.get("num_turns")})
            print(f"{case}#{i}: {'PASS' if ok else 'FAIL'} -- {why} "
                  f"(${meta.get('cost_usd') or 0:.4f})")
    verdict = "PASS" if all(r["pass"] for r in rows_out) else "FAIL"
    total = sum(float(r["cost_usd"] or 0) for r in rows_out)
    summary = {"measured_at": datetime.now(timezone.utc).isoformat(), "tag": a.tag,
               "model": rpr._CLAUDE_WORKER_MODEL, "verdict": verdict,
               "total_cost_usd": round(total, 6), "calls": rows_out}
    (HERE / f"summary_{a.tag}.yaml").write_text(
        yaml.safe_dump(summary, sort_keys=False, allow_unicode=True), encoding="utf-8")
    lines = [f"# Claim-test review: offline measurement ({a.tag})", "",
             f"Model `{rpr._CLAUDE_WORKER_MODEL}`, closed-book (the pipeline's own options). "
             f"Verdict: **{verdict}** ({sum(r['pass'] for r in rows_out)}/{len(rows_out)} calls "
             f"met their expectation). Total cost ${total:.4f}.", "",
             "| case | call | expectation | result | why | cost (USD) | input | output | "
             "cache read | cache write |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows_out:
        t = r["tokens"] or {}
        lines.append(f"| {r['case']} | {r['call']} | {r['expect']} | "
                     f"{'pass' if r['pass'] else 'FAIL'} | {r['why']} | "
                     f"{float(r['cost_usd'] or 0):.4f} | {t.get('input', 0)} | "
                     f"{t.get('output', 0)} | {t.get('cache_read', 0)} | "
                     f"{t.get('cache_creation', 0)} |")
    (HERE / f"summary_{a.tag}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"verdict {verdict}; total ${total:.4f}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
