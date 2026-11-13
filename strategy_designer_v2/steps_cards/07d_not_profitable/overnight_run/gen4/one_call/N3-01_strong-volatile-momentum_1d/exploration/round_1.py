import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    # trades
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t) == 0: continue
            t = t.copy(); t["coin"] = c; t["win"] = w
            tr.append(t)
    tr = pd.concat(tr, ignore_index=True)
    tr["days_held"] = tr["duration_minutes"] / 1440
    tr["year"] = pd.to_datetime(tr["entry_time"]).dt.year
    tr["fee_pct"] = tr["profit_loss_percent"] - tr["net_profit_loss_percent"]
    out["trades_overall"] = pd.Series({
        "n": len(tr), "mean_days": tr.days_held.mean(), "median_days": tr.days_held.median(),
        "gross_mean": tr.profit_loss_percent.mean(), "net_mean": tr.net_profit_loss_percent.mean(),
        "fee_mean": tr.fee_pct.mean(), "win_rate": (tr.profit_loss_percent > 0).mean(),
        "gross_median": tr.profit_loss_percent.median(),
        "t_gross": stats.ttest_1samp(tr.profit_loss_percent, 0).statistic,
        "worst": tr.profit_loss_percent.min(), "best": tr.profit_loss_percent.max()})
    out["trades_by_coin"] = tr.groupby("coin").agg(n=("profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        days=("days_held", "mean"), win=("profit_loss_percent", lambda x: (x > 0).mean()))
    out["trades_by_year"] = tr.groupby("year").agg(n=("profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        sum_net=("net_profit_loss_percent", "sum"))
    tr["dur_b"] = pd.cut(tr.days_held, [0, 2, 5, 10, 20, 1000])
    out["trades_by_duration"] = tr.groupby("dur_b").agg(n=("profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    tr["ef_b"] = pd.cut(tr.entry_forecast, [-0.01, 2, 5, 10, 15, 20.01])
    out["trades_by_entry_fc"] = tr.groupby("ef_b").agg(n=("profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        days=("days_held", "mean"))
    out["exit_fc"] = tr.exit_forecast.describe()

    # days: book vs coin, by state
    dd = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = c; d["win"] = w
            d["vol20"] = d["coin_return"].rolling(20).std()
            d["ret20"] = d["close"] / d["close"].shift(20) - 1
            v = d["book_value"]
            d["dd"] = v / v.cummax() - 1
            dd.append(d)
    dd = pd.concat(dd, ignore_index=True)
    dd["year"] = pd.to_datetime(dd["day"]).dt.year
    dd["inpos"] = dd["book_return"].abs() > 1e-9
    out["book_by_year"] = dd.groupby("year").agg(book=("book_return", "mean"),
        coin=("coin_return", "mean"), inpos=("inpos", "mean"), maxdd=("dd", "min"))
    dd["coin_dir"] = np.where(dd.coin_return > 0, "up", "down")
    out["inpos_by_coin_dir"] = dd[dd.inpos].groupby("coin_dir").agg(n=("book_return", "size"),
        book=("book_return", "mean"), coin=("coin_return", "mean"))
    dd["volq"] = dd.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=["low", "mid", "high"]))
    out["inpos_by_vol"] = dd[dd.inpos].groupby("volq").agg(n=("book_return", "size"),
        book=("book_return", "mean"), sd=("book_return", "std"))
    out["maxdd_by_coin"] = dd.groupby("coin")["dd"].min()
    out["worst_window_dd"] = dd.groupby(["coin", "win"])["dd"].min().describe()

    # forecast bucket forward 5-bar returns, non-overlapping
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            f5 = b["close"].shift(-5) / b["close"] - 1
            r1 = b["close"].shift(-1) / b["close"] - 1
            idx = np.arange(0, len(b), 5)
            s = pd.DataFrame({"fc": b["forecast"].values[idx], "f5": f5.values[idx],
                              "r1": r1.values[idx], "coin": c, "regime": b["regime"].values[idx]})
            rows.append(s)
    s = pd.concat(rows).dropna(subset=["f5"])
    s["ex"] = s.f5 - s.groupby("coin").f5.transform("mean")
    s["fb"] = pd.cut(s.fc, [-0.01, 0.001, 2, 5, 10, 20.01])
    g = s.groupby("fb").ex
    out["fwd5_by_fc"] = pd.DataFrame({"n": g.size(), "mean_ex": g.mean(),
        "t": g.mean() / (g.std() / np.sqrt(g.size()))})
    g2 = s.groupby("regime").ex
    out["fwd5_by_regime"] = pd.DataFrame({"n": g2.size(), "mean_ex": g2.mean(),
        "t": g2.mean() / (g2.std() / np.sqrt(g2.size()))})
    return out
