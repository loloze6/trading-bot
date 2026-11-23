import numpy as np, pandas as pd

def tstat(x):
    x = pd.Series(x).dropna()
    return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            c = b["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r1 = c.pct_change()
            vol = r1.rolling(24, min_periods=20).std()
            z1 = r1 / vol
            vol24 = vol.rolling(24 * 30, min_periods=200).median()
            vrel = vol / vol24
            h = 24
            idx = np.arange(0, len(c) - h, h)
            fwd = (c.shift(-h) / c - 1)
            # also: every bar with |z1|>1, read once per 24h grid cell (first such bar in each cell)
            cell = np.arange(len(c)) // h
            dfa = pd.DataFrame({"coin": coin, "wn": int(w[1:]), "cell": cell, "fwd": fwd.values,
                                "z1": z1.values, "hour": ts.dt.hour.values, "vrel": vrel.values})
            rows.append(dfa)
    d = pd.concat(rows).dropna(subset=["fwd", "z1"])
    grid = d.groupby(["coin", "wn"]).apply(lambda g: g.iloc[::24]).reset_index(drop=True)
    drift = grid.groupby("coin").fwd.mean(); usual = grid.groupby("coin").fwd.std()
    d["ex"] = d.fwd - d.coin.map(drift); d["usual"] = d.coin.map(usual)
    big = d[(d.z1.abs() > 1) & (d.z1.abs() <= 3)].copy()
    big = big.groupby(["coin", "wn", "cell"]).first().reset_index()  # one case per grid cell
    big["mv"] = -np.sign(big.z1) * big.ex * 100
    big["tot"] = -np.sign(big.z1) * big.fwd * 100
    big["str"] = -np.sign(big.z1) * big.ex / big.usual
    out = {}
    out["cases_h24_one_per_cell"] = pd.Series({"n": len(big), "unusual_%": big.mv.mean(),
        "total_%": big.tot.mean(), "strength": big.str.mean(), "t": tstat(big.mv),
        "net_of_0.19%": big.tot.mean() - 0.19})
    big["presettle"] = big.hour.isin([23, 7, 15])
    out["by_presettle_hour"] = big.groupby("presettle").mv.agg(["count", "mean", tstat])
    big["vq"] = pd.qcut(big.vrel, 3, labels=["lowvol", "midvol", "highvol"])
    out["by_vol_regime"] = big.groupby("vq", observed=True).mv.agg(["count", "mean", tstat])
    big["wgrp"] = pd.cut(big.wn, [0, 6, 12, 18, 24])
    out["by_wgroup"] = big.groupby("wgrp", observed=True).mv.agg(["count", "mean", tstat])
    # condition alone: high-vol regime bars without signal (|z1|<=1), direction from sign of z1
    small = d[d.z1.abs() <= 1].groupby(["coin", "wn", "cell"]).first().reset_index()
    small["mv"] = -np.sign(small.z1) * small.ex * 100
    small["vq"] = pd.cut(small.vrel, [0] + list(big.vrel.quantile([1/3, 2/3])) + [np.inf], labels=["lowvol", "midvol", "highvol"])
    out["no_signal_by_vol_regime"] = small.groupby("vq", observed=True).mv.agg(["count", "mean", tstat])
    # book daily returns by window group
    D = pd.concat([days[c][w].assign(coin=c, wn=int(w[1:])) for c in days for w in days[c]])
    D["wgrp"] = pd.cut(D.wn, [0, 6, 12, 18, 24])
    out["book_daily_by_wgroup_%"] = D.groupby("wgrp", observed=True).book_return.agg(lambda x: 100 * x.mean())
    return out
