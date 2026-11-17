import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            v = b["volume"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd": c.shift(-H)/c - 1,
                "past20": c/c.shift(20) - 1,
                "past5": c/c.shift(5) - 1,
                "dist30": c/c.rolling(30).max() - 1,
                "vol20": r1.rolling(20).std(),
                "volu": v/v.rolling(20).mean(),
                "trend": (b["regime"] == "trending").astype(int),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "pos": np.arange(len(b)),
            })
            rows.append(df)
    a = pd.concat(rows, ignore_index=True)
    g = a[(a["pos"] % H == 0)].dropna(subset=["fwd"]).copy()
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    out["n_grid"] = len(g)
    out["trend_share_allbars"] = a["trend"].mean()

    def qtab(col, q=5):
        s = g.dropna(subset=[col]).copy()
        s["q"] = s.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        t = s.groupby("q")["ex"].agg(["mean", "count", "std"])
        t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
        top, bot = s[s.q == q-1]["ex"], s[s.q == 0]["ex"]
        t.loc["top-bot_t", "mean"] = stats.ttest_ind(top, bot, equal_var=False).statistic
        return t
    for col in ["past20", "past5", "dist30", "vol20", "volu"]:
        out["q_" + col] = qtab(col)

    tt = g.groupby("trend")["ex"].agg(["mean", "count", "std"])
    out["by_trend_regime"] = tt

    # daily returns by weekday, coin-demeaned
    a["r1n"] = a.groupby(["coin", "win"])["fwd"].transform(lambda x: x)  # placeholder
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            dd.append(d)
    d = pd.concat(dd, ignore_index=True)
    d["wd"] = pd.to_datetime(d["day"]).dt.dayofweek
    d["year"] = pd.to_datetime(d["day"]).dt.year
    wt = d.groupby("wd")["coin_return"].agg(["mean", "count", "std"])
    wt["t"] = wt["mean"]/(wt["std"]/np.sqrt(wt["count"]))
    out["weekday_coin_ret"] = wt
    bt = d.groupby("year")[["book_return", "coin_return"]].mean()
    out["year_book_vs_coin"] = bt
    out["book_by_coin"] = d.groupby("coin")[["book_return", "coin_return"]].mean()
    # book: active share
    a["active"] = (a["alloc"].abs() > 1e-6)
    out["active_share_by_coin"] = a.groupby("coin")["active"].mean()
    return out
