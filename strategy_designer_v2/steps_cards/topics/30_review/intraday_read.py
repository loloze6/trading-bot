import json, sys
from pathlib import Path
import pandas as pd
S = Path("/tmp/claude-0/-home-user-trading-bot/9a8c137d-677e-59d2-8d4c-7c621473a28a/scratchpad/r30")
orig = S / "strategy_designer_v2/steps_cards/04_backtest/intraday_1h_run/backtests"
done = [l.split(":")[0] for l in (S / "rerun_progress.txt").read_text().splitlines() if "exit 0" in l]
rows = []
for bt in done:
    new, old = S / "rerun" / bt, orig / bt
    same = diff = 0; g = n = f = edge = turn = 0.0
    for m in new.glob("*/w*/metrics.json"):
        c = json.load(open(m))["core"]; o = old / m.relative_to(new)
        if o.exists():
            co = json.load(open(o))["core"]
            same += abs(c["net_pnl"] - co["net_pnl"]) < 1e-6; diff += abs(c["net_pnl"] - co["net_pnl"]) >= 1e-6
        g += c["gross_pnl"]; n += c["net_pnl"]; f += c["fees_paid"]
        b = pd.read_csv(m.with_name("bars.csv.gz"), usecols=["close", "postRebalance_current_allocation"])
        a = b["postRebalance_current_allocation"].fillna(0); r = b["close"].pct_change().shift(-1).fillna(0)
        edge += (a * r).sum() * 1000; turn += a.diff().abs().sum()
    rows.append({"idea": bt[:58], "net same as committed": f"{same}/{same+diff}", "at closes": round(edge), "spread+slip": round(edge - g),
                 "fees": round(f), "net": round(n), "edge bps/unit": round(edge / turn / 1000 * 1e4, 1) if turn else None,
                 "cost bps/unit": round((edge - g + f) / turn / 1000 * 1e4, 1) if turn else None})
pd.set_option("display.width", 250)
print(pd.DataFrame(rows).to_string(index=False))
