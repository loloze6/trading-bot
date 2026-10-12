"""Lane-1 config validity replay (DECISION_LOG D-106).

Feeds the brief's config and a run's authored config, bar by bar, the same three
fixed synthetic daily series (series_1.csv .. series_3.csv in this folder, sha256
pinned in D-106), and compares the strategy's forecast and regime on every bar and
its required_bars. VALID iff zero differences on every series and equal
required_bars; any difference voids the run (the run still counts as a trial).

Usage, from the repository root (prints YAML; write it to the run's artifacts):
    venv/Scripts/python.exe strategy-research/engineering/lane1_replay/replay_config.py \\
        strategy-research/briefs/<brief>.md strategy-research/runs/<run>/artifacts/backtest_spec.yaml

Reads no market data: only the three synthetic files.
"""
import hashlib
import json
import logging
import os
import sys
import tempfile
from pathlib import Path

import pandas as pd
import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SERIES_SHA256 = {
    "series_1.csv": "d6534df11e4d661295b33889efe8c9df1838af2a4758599e716cc99fce7f16a6",
    "series_2.csv": "6868f7d38e0ff55adc4940b764816bed034277de3392422b41d68dcb0eb31e26",
    "series_3.csv": "6640ad6918bb9aa9242a5ec02278ffa3c383a84290efc420316dbddcc8ddbdb9",
}


def _brief_config(brief_path: Path) -> dict:
    text = brief_path.read_text(encoding="utf-8").replace("\r\n", "\n")
    front = text.split("---\n")[1]
    constraint = yaml.safe_load(front)["constraints"][0]
    return json.loads(constraint.split("\n", 1)[1])


def _strategy(config: dict):
    from strategies.main_strategy import AdvancedStrategy
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    json.dump(config, f)
    f.close()
    try:
        return AdvancedStrategy(config_path=f.name)
    finally:
        os.unlink(f.name)


def replay(brief_path: Path, spec_path: Path) -> dict:
    sys.path.insert(0, str(REPO / "trading-bot"))
    logging.disable(logging.CRITICAL)
    want = _brief_config(brief_path)
    got = yaml.safe_load(spec_path.read_text(encoding="utf-8"))["config"]
    out = {"brief": brief_path.name, "authored": f"{spec_path.parent.parent.name}/{spec_path.name}",
           "identical_json": want == got, "series": {}}
    valid = True
    for name, pinned in SERIES_SHA256.items():
        raw = (HERE / name).read_bytes().replace(b"\r\n", b"\n")
        sha = hashlib.sha256(raw).hexdigest()
        if sha != pinned:
            raise SystemExit(f"{name}: sha256 {sha} is not the pinned {pinned} (D-106)")
        df = pd.read_csv(HERE / name, parse_dates=["timestamp"])
        a, b = _strategy(want), _strategy(got)
        diff = nonzero = 0
        for i in range(len(df)):
            a.update(df.iloc[i:i + 1])
            b.update(df.iloc[i:i + 1])
            oa, ob = a.generate_signals(), b.generate_signals()
            if oa.forecast != ob.forecast or oa.regime != ob.regime:
                diff += 1
            nonzero += int(oa.forecast != 0)
        same_rb = a.required_bars == b.required_bars
        valid = valid and diff == 0 and same_rb
        out["series"][name] = {"sha256": sha, "bars": len(df), "forecast_or_regime_differences": diff,
                               "nonzero_forecasts_brief": nonzero,
                               "required_bars": [a.required_bars, b.required_bars]}
    out["verdict"] = "VALID" if valid else "VOID"
    return out


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    print(yaml.safe_dump(replay(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()), sort_keys=False))
