import numpy as np, pandas as pd
from scipy import stats

def _er(c, n=60, s=5):
    ch = (c - c.shift(n)).abs()
    vol = c.diff().abs().rolling(n).sum()
    return (ch / vol).rolling(s).mean()

def explore(data):
    H = 10
    rows = []
    grid_rows = []
    daily = []
    for coin, wins in data["bars"].items():
        # coin drift on grid
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            er = _er(c)
            ph = hi.shift(1).rolling(60).max(); pl = lo.shift(1).rolling(60).min()
            fwd = c.shift(-H) / c - 1
            past10 = c / c.shift(10) - 1
            dret = c.pct_change()
            vol20 = dret.rolling(20).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "c": c, "er": er,
                               "up": (c / ph - 1) * 100, "dn": (c / pl - 1) * 100,
                               "width": (ph / pl - 1) * 100, "fwd": fwd, "past10": past10,
                               "vol20": vol20, "pos": np.arange(len(b)),
                               "wd": ts.dt.dayofweek, "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
            daily.append(pd.DataFrame({"coin": coin, "wd": ts.dt.dayofweek, "r": dret}))
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % H == 0) & A["fwd"].notna()].copy()
    drift = G.groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    G["ex"] = G["fwd"] - G["coin"].map(drift)
    out = {}
    out["drift_by_coin"] = drift.round(4)

    def summ(df, key):
        g = df.groupby(key, observed=True)["ex"]
        r = pd.DataFrame({"n": g.size(), "mean": g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.size()))})
        return r.round(4)

    # first bar of breakouts (no breakout previous bar), once per grid cell
    A["cell"] = A["pos"] // H
    up = A[(A["up"] > 0) & A["ex"].notna()]
    up = up[A.loc[up.index - 1, "up"].values <= 0] if len(up) else up
    up = up.drop_duplicates(["coin", "w", "cell"])
    up = up.copy(); up["erb"] = pd.cut(up["er"], [0, 0.15, 0.3, 0.45, 1.0])
    out["upbreak_by_ER"] = summ(up, "erb")
    up["szb"] = pd.qcut(up["up"], 4)
    out["upbreak_by_size"] = summ(up, "szb")
    up["wb"] = pd.qcut(up["width"], 4)
    out["upbreak_by_width"] = summ(up, "wb")
    dn = A[(A["dn"] < 0) & A["ex"].notna()]
    dn = dn[A.loc[dn.index - 1, "dn"].values >= 0]
    dn = dn.drop_duplicates(["coin", "w", "cell"]).copy()
    dn["erb"] = pd.cut(dn["er"], [0, 0.15, 0.3, 0.45, 1.0])
    out["dnbreak_by_ER (ex = raw long return)"] = summ(dn, "erb")
    # grid: past 10d return buckets
    G["p10b"] = pd.qcut(G["past10"], 5)
    out["grid_by_past10"] = summ(G.dropna(subset=["past10"]), "p10b")
    G["vb"] = pd.qcut(G["vol20"], 4)
    out["grid_by_vol20"] = summ(G.dropna(subset=["vol20"]), "vb")
    G["wb"] = pd.qcut(G["width"], 4)
    out["grid_by_width60"] = summ(G.dropna(subset=["width"]), "wb")
    D = pd.concat(daily).dropna()
    g = D.groupby("wd")["r"]
    out["daily_by_weekday"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.size()))}).round(5)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)], ignore_index=True)
    out["trades"] = pd.Series({"n": len(T), "mean_net": T["net_profit_loss_percent"].mean(),
                               "median_net": T["net_profit_loss_percent"].median(),
                               "win": (T["net_profit_loss_percent"] > 0).mean(),
                               "mean_dur_days": T["duration_minutes"].mean() / 1440}).round(3)
    T["dq"] = pd.qcut(T["duration_minutes"], 3, duplicates="drop")
    out["trades_by_duration"] = T.groupby("dq", observed=True)["net_profit_loss_percent"].agg(["size", "mean", "median"]).round(3)
    return out
