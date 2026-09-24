"""Golden byte-identity harness for the promote path (branch 3 code review, item 8).

`run_scenario(module, scenario, root)` drives `module._dispatch_verdict_route`'s
promote branch in a sandbox built from `inputs.yaml` and returns the two files it
writes (promotion_audit.yaml, and profit_bars_evaluation.yaml when the
profit_bars_file flag is on), with the one wall-clock field (`generated_at`)
normalised.

The committed `<scenario>/*.yaml` outputs were produced by running this harness
against the MASTER code at 83794d9a (before branch 3), exactly:

    git show 83794d9a:strategy-research/workflow/run_phase1_research.py > rpr_master.py
    python tests/fixtures/profit_bars_golden/golden_harness.py rpr_master.py

(cwd: strategy-research). tests/test_profit_bars_every_backtest.py runs the same
harness against the CURRENT code with the new flag absent and compares bytes.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
INPUTS = HERE / "inputs.yaml"
_GENERATED_AT = re.compile(r"^generated_at: .*$", re.MULTILINE)


def scenarios() -> dict:
    return yaml.safe_load(INPUTS.read_text(encoding="utf-8"))["scenarios"]


def _common() -> dict:
    return yaml.safe_load(INPUTS.read_text(encoding="utf-8"))


def run_scenario(module, name: str, root: Path) -> dict:
    """Returns {filename: normalised text} for the files the promote branch wrote."""
    common = _common()
    sc = common["scenarios"][name]
    root = Path(root)
    module.ROOT = root
    module.CAMPAIGN_STATE_PATH = root / "campaign_state.yaml"
    (root / "config").mkdir(parents=True, exist_ok=True)
    (root / "config" / "campaign_config.yaml").write_text(
        yaml.safe_dump({"orchestrator": sc["orchestrator"]}), encoding="utf-8")
    (root / "config" / "profitability_bars.yaml").write_text(
        yaml.safe_dump(common["bars"]), encoding="utf-8")
    ledger = [dict(r) for r in common["ledger"]]
    for r in ledger:  # YAML cannot hold NaN portably as a literal we want to keep
        if r.get("sharpe") == "nan":
            r["sharpe"] = float("nan")
    module.save_yaml(module.CAMPAIGN_STATE_PATH, {"runs": ["a", "b"], "trial_sharpes": ledger})
    rd = root / "runs" / "run_gold"
    arts = rd / "artifacts"
    arts.mkdir(parents=True)
    module.save_yaml(rd / "pipeline_state.yaml", {"status": "active", "flags": {}, "audit_log": {}})
    module.save_yaml(arts / "verdict_interpretation.yaml", {"hypothesis_id": "H-GOLD"})
    prs = common["protocol_results"]
    module.save_yaml(arts / "protocol_result.yaml", prs[sc["protocol_result"]])
    for vid, pr_name in (sc.get("variants") or {}).items():
        module.save_yaml(arts / "variants" / vid / "protocol_result.yaml", prs[pr_name])
    route = module._dispatch_verdict_route(rd, "run_gold", {}, {}, "promote", None)
    out = {"route.txt": f"{route}\n"}
    for fname in ("promotion_audit.yaml", "profit_bars_evaluation.yaml"):
        p = arts / fname
        if p.exists():
            out[fname] = _GENERATED_AT.sub("generated_at: <normalised>", p.read_text(encoding="utf-8"))
    return out


def _load(path: str):
    spec = importlib.util.spec_from_file_location("rpr_golden_source", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["rpr_golden_source"] = mod
    spec.loader.exec_module(mod)
    return mod


if __name__ == "__main__":
    import tempfile
    sys.path.insert(0, str(HERE.parents[2] / "workflow"))
    sys.path.insert(0, str(HERE.parents[2] / "tools"))
    mod = _load(sys.argv[1])
    for name in scenarios():
        files = run_scenario(mod, name, Path(tempfile.mkdtemp()))
        (HERE / name).mkdir(exist_ok=True)
        for fname, text in files.items():
            (HERE / name / fname).write_text(text, encoding="utf-8", newline="\n")
        print(name, sorted(files))
