"""Topic 47, measurement 1d-2 (operator, 2026-11-23: "is the swing per trade ten times the gain? on all backtests?
does a small change of the share of winning trades change the total?"). For every book step 5 confirmed on night 5
(and the phase-A books), from its trades (the engine's realized return per trade, after costs, in % of the price):
trades, share of winning trades, mean gain of a winner, mean loss of a loser, mean per trade, the swing (standard
deviation) per trade and its ratio to the mean, and the margin: how many points the share of winners can lose before
the mean per trade is 0 (mean / (mean win + mean loss)). Writes trade_odds.csv.
  python3 topics/47_review/trade_odds.py"""
import pathlib
import numpy as np, pandas as pd

STEPS = pathlib.Path(__file__).resolve().parents[2]
gate = pd.read_csv(pathlib.Path(__file__).with_name("calmar_gate.csv"))
rows = []
books = [(r.run, r.backtest, "pays" if r.pays else "does not pay") for r in gate.itertuples()]
books += [("book_reflects_idea_run", p.name, "phase A") for p in sorted((STEPS / "04_backtest" / "book_reflects_idea_run" / "backtests").iterdir()) if p.is_dir()]
for run, rid, group in books:
    t = pd.read_csv(STEPS / "04_backtest" / run / "backtests" / rid / "chart_trades.csv.gz")
    x = t.realized_return.to_numpy(float)
    if len(x) < 3: continue
    win, loss = x[x > 0], -x[x <= 0]
    mean, sd = x.mean(), x.std(ddof=1)
    rows.append({"group": group, "run": run, "book": rid, "trades": len(x), "win_share": len(win) / len(x),
                 "mean_win": win.mean() if len(win) else 0.0, "mean_loss": loss.mean() if len(loss) else 0.0,
                 "mean": mean, "swing": sd, "swing_over_mean": sd / mean if mean > 0 else np.nan,
                 "margin_points": 100 * mean / (win.mean() + loss.mean()) if len(win) and len(loss) else np.nan,
                 "t": mean / sd * np.sqrt(len(x))})
d = pd.DataFrame(rows); d.to_csv(pathlib.Path(__file__).with_name("trade_odds.csv"), index=False, float_format="%.4g")
pd.set_option("display.width", 200)
q = lambda s: f"{s.median():.2f} (middle half {s.quantile(.25):.2f} to {s.quantile(.75):.2f})"
for g, x in d.groupby("group"):
    pos = x[x["mean"] > 0]
    print(f"\n== {g}: {len(x)} books; mean per trade above 0: {len(pos)}")
    print(" trades per book      ", q(x.trades))
    print(" share of winners     ", q(100 * x.win_share), "%")
    print(" mean winner / loser  ", q(x.mean_win), "% /", q(x.mean_loss), "%")
    print(" mean per trade       ", q(x["mean"]), "%")
    print(" swing per trade      ", q(x.swing), "%")
    print(" swing / mean (mean>0)", q(pos.swing_over_mean))
    print(" margin, in points of the share of winners (mean>0):", q(pos.margin_points))
