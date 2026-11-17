import pandas as pd, numpy as np
from scipy import stats

def _rsi(c, n=14):
    d = c.diff()
    up = d.clip(lower=0).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    return 100 - 100/(1+up/dn)

def _reg(df, x, y):
    d = df[[x, y]].dropna()
    if len(d) < 10: return (np.nan, np.nan, len(d))
    r = stats.linregress(d[x], d[y])
    return (r.slope, r.slope/r.stderr if r.stderr > 0 else np.nan, len(d))

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r1 = c.pct_change()
            rsi = _rsi(c)
            share = (rsi > 50).astype(float).where(rsi.notna()).rolling(30, min_periods=30).mean()
            vol30 = r1.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "r1": r1, "f1": c.shift(-1)/c-1, "f7": c.shift(-7)/c-1, "f14": c.shift(-14)/c-1,
                "p30": c/c.shift(30)-1, "p7": c/c.shift(7)-1,
                "share": share, "rsi": rsi, "vol30": vol30,
                "regime": b["regime"], "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # demean per coin
    for h in ["f1", "f7", "f14"]:
        A[h+"d"] = A[h] - A.groupby("coin")[h].transform("mean")
    G14 = A[A["pos"] % 14 == 0]
    G7 = A[A["pos"] % 7 == 0]
    G1 = A
    out = {}
    res = []
    for name, G, y in [("all14", G14, "f14d"), ("all7", G7, "f7d")]:
        for x in ["share", "p30", "p7", "rsi", "vol30"]:
            for reg in ["trending", "unknown", None]:
                g = G if reg is None else G[G["regime"] == reg]
                s, t, n = _reg(g, x, y)
                res.append({"grid": name, "x": x, "reg": reg or "all", "slope": s, "t": t, "n": n})
    out["regressions"] = pd.DataFrame(res)
    # by coin, share on f14 grid
    rc = []
    for coin in G14["coin"].unique():
        for reg in ["trending", "unknown"]:
            g = G14[(G14["coin"] == coin) & (G14["regime"] == reg)]
            for x in ["share", "p30"]:
                s, t, n = _reg(g, x, "f14d")
                rc.append({"coin": coin, "reg": reg, "x": x, "slope": s, "t": t, "n": n})
    out["by_coin"] = pd.DataFrame(rc)
    # large daily moves -> next day / next 7 days (7-grid not usable for r1 condition; use all bars for f1)
    A["z"] = A["r1"] / A["vol30"]
    A["zq"] = pd.qcut(A["z"], 5, labels=False, duplicates="drop")
    out["after_move_q"] = A.groupby("zq").agg(n=("f1d", "count"), f1d=("f1d", "mean"), f1t=("f1d", lambda s: s.mean()/s.std()*np.sqrt(s.count())))
    # vol level quintile -> next 7d on grid
    G7 = A[A["pos"] % 7 == 0].copy()
    G7["vq"] = pd.qcut(G7["vol30"], 5, labels=False, duplicates="drop")
    out["vol_q_f7"] = G7.groupby("vq")["f7d"].agg(["count", "mean", "std"])
    # weekday
    out["weekday"] = A.groupby("wd")["f1d"].agg(["count", "mean", lambda s: s.mean()/s.std()*np.sqrt(s.count())])
    # regime and f14 base
    out["regime_f14"] = G14.groupby(["coin", "regime"])["f14d"].agg(["count", "mean"])
    # book: daily returns by sign of position
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; bk.append(d)
    D = pd.concat(bk)
    out["book_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].mean()
    # share quintile in all bars, f14 grid
    G14 = G14.copy()
    G14["sq"] = pd.qcut(G14["share"], 4, labels=False, duplicates="drop")
    out["share_q_f14"] = G14.groupby(["regime", "sq"])["f14d"].agg(["count", "mean"])
    return out
