import numpy as np, pandas as pd

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

def _summ(df, by, col):
    g = df.groupby(by, observed=True)[col]
    return pd.DataFrame({"n": g.size(), "mean_bp": g.mean() * 1e4, "t": g.apply(_t)})

def _slope(df, x, y):
    d = df[[x, y]].dropna()
    if len(d) < 10: return pd.Series({"n": len(d), "slope_bp": np.nan, "t": np.nan})
    X = d[x] - d[x].mean(); Y = d[y]
    b = (X * Y).sum() / (X * X).sum()
    res = Y - Y.mean() - b * X
    se = np.sqrt((res ** 2).sum() / (len(d) - 2) / (X * X).sum())
    return pd.Series({"n": len(d), "slope_bp": b * 1e4, "t": b / se})

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(720, min_periods=240).std()
            ts = pd.to_datetime(b["timestamp"])
            for h in (12, 24, 48):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(b), h)
                d = pd.DataFrame({
                    "coin": coin, "w": w, "h": h,
                    "r24z": ((c / c.shift(24) - 1) / (sd * np.sqrt(24))).values[idx],
                    "r72z": ((c / c.shift(72) - 1) / (sd * np.sqrt(72))).values[idx],
                    "vol24": (r1.rolling(24).std() / sd).values[idx],
                    "year": ts.dt.year.values[idx],
                    "fwd": fwd.values[idx],
                })
                rows.append(d)
    D = pd.concat(rows).dropna(subset=["fwd", "r24z", "vol24"])
    D["drift"] = D.groupby(["coin", "h"])["fwd"].transform("mean")
    D["ex"] = D["fwd"] - D["drift"]
    D["vq"] = D.groupby("h")["vol24"].transform(lambda s: pd.qcut(s, 4, labels=False))
    D["wnum"] = D["w"].str[1:].astype(int)
    D["half"] = np.where(D["wnum"] <= 12, "w1-12", "w13-24")
    res = {}
    res["slope_ex_on_r24z_by_h_volq"] = D.groupby(["h", "vq"]).apply(lambda g: _slope(g, "r24z", "ex"))
    H = D[(D.h == 24) & (D.vq == 3)].copy()
    res["h24_hivol_slope_by_coin"] = H.groupby("coin").apply(lambda g: _slope(g, "r24z", "ex"))
    res["h24_hivol_slope_by_half"] = H.groupby("half").apply(lambda g: _slope(g, "r24z", "ex"))
    res["h24_hivol_slope_by_year"] = H.groupby("year").apply(lambda g: _slope(g, "r24z", "ex"))
    H["mq"] = pd.qcut(H["r24z"], 5)
    res["h24_hivol_ex_by_r24z_quintile"] = _summ(H, ["mq"], "ex")
    H["sgnex"] = -np.sign(H["r24z"]) * H["ex"]
    res["h24_hivol_reversal_gain_by_coin"] = _summ(H, ["coin"], "sgnex")
    res["h24_hivol_slope_on_r72z"] = _slope(H.dropna(subset=["r72z"]), "r72z", "ex")
    L = D[(D.h == 24) & (D.vq == 0)]
    res["h24_lowvol_slope_by_coin"] = L.groupby("coin").apply(lambda g: _slope(g, "r24z", "ex"))
    return res
