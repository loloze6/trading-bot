"""Topic 47, measurement 1d-4 (operator: "is it the same for other types of strategies?"). Every book of the
similarity register (all runs: paying and confirmed), with its chart files: holding horizon (the plan's
min_holding_bars times the bar, in days; none: 'no horizon set'), trades a year, mean and swing per trade, share of
winners and the margin (points of winners before the mean trade is 0), coins opening on the same day, the real and
the coin-decorrelated deepest fall and Calmar. Writes book_types.csv.  python3 topics/47_review/book_types.py"""
import json, pathlib, warnings
import numpy as np, pandas as pd
import streaks as st

warnings.simplefilter("ignore")
STEPS = st.STEPS; rng = np.random.default_rng(2)
HOURS = {"1h": 1, "4h": 4, "1d": 24}
books = json.load(open(STEPS / "orchestration/ideas_similarities_check/register/books.json"))
rows = []
for b in books:
    rec = STEPS / "04_backtest" / b["run"] / "backtests" / b["id"]
    cfgf = STEPS / "03_test_plan" / b["run"] / "plans" / f"{b['id']}_config.json"
    if not (rec / "chart_bars.csv.gz").exists() or not (rec / "chart_trades.csv.gz").exists() or not cfgf.exists():
        continue
    hold = json.load(open(cfgf))["strategies"].get("min_holding_bars")
    horizon = hold * HOURS[b["bar"]] / 24 if hold else None
    t = pd.read_csv(rec / "chart_trades.csv.gz"); x = t.realized_return.to_numpy(float)
    if len(x) < 30: continue
    ret, pos = st.per_coin(rec); R = ret.to_numpy(); P = pos.fillna(False).to_numpy()
    cal, fall = st.calmar(np.nan_to_num(np.nanmean(R, axis=1)))
    sims = np.array([st.calmar(np.nan_to_num(np.nanmean(np.column_stack([np.roll(R[:, j], rng.integers(len(R))) for j in range(R.shape[1])]), axis=1))) for _ in range(100)])
    opens = P & ~np.r_[np.zeros((1, P.shape[1]), bool), P[:-1]]; k = opens.sum(1)
    win, loss = x[x > 0], -x[x <= 0]
    rows.append({"run": b["run"], "book": b["id"], "kind": b.get("kind"), "bar": b["bar"], "coins": R.shape[1],
                 "horizon_days": horizon, "trades_per_year": len(x) / (len(R) / 365), "mean": x.mean(), "swing": x.std(ddof=1),
                 "win_share": len(win) / len(x), "margin_points": 100 * x.mean() / (win.mean() + loss.mean()) if len(win) and len(loss) else np.nan,
                 "coins_opening_together": float(k[k > 0].mean()) if (k > 0).any() else np.nan,
                 "fall": fall, "fall_decorrelated": float(np.median(sims[:, 1])), "calmar": cal, "calmar_decorrelated": float(np.median(sims[:, 0]))})
d = pd.DataFrame(rows); d.to_csv(pathlib.Path(__file__).with_name("book_types.csv"), index=False, float_format="%.4g")
d["horizon"] = pd.cut(d.horizon_days.fillna(-1), [-2, 0, 1.01, 5.01, 1e9], labels=["no horizon set", "up to 1 day", "2 to 5 days", "over 5 days"])
cols = dict(books=("book", "size"), pays=("kind", lambda s: int((s == "paying").sum())), trades_per_year=("trades_per_year", "median"),
            swing_over_mean=("swing_over_mean", "median"), win_share=("win_share", "median"), margin_points=("margin_points", "median"),
            together=("coins_opening_together", "median"), fall=("fall", "median"), fall_decorr=("fall_decorrelated", "median"),
            calmar=("calmar", "median"), calmar_decorr=("calmar_decorrelated", "median"))
d["swing_over_mean"] = np.where(d["mean"] > 0, d.swing / d["mean"], np.nan)
pd.set_option("display.width", 250)
for by in (["horizon"], ["bar"], ["kind"]):
    print(d.groupby(by, observed=True).agg(**cols).round(2).to_string(), "\n")
