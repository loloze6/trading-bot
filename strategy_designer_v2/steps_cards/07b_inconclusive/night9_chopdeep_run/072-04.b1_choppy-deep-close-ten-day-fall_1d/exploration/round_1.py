import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = [1, 3, 5, 10, 20]
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            hi = c.rolling(20).max()
            sd = r.rolling(20).std()
            depth = (c / hi - 1) / sd
            r60 = c / c.shift(60) - 1
            vol30 = r.rolling(30).std()
            vmed = vol30.rolling(365, min_periods=120).median()
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                              "depth": depth, "fc": b["forecast"].astype(float),
                              "chop": (b["regime"] == "unknown"),
                              "up": (r > 0), "agit": vol30 > vmed, "r60": r60})
            for h in H:
                d[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    drift = {h: D[D.pos % h == 0].groupby("coin")[f"f{h}"].mean() for h in H}
    # per horizon: grid cases in choppy with depth<0
    res = []
    for h in H:
        g = D[(D.pos % h == 0) & D.chop & (D.depth < 0)].dropna(subset=["depth", f"f{h}"]).copy()
        g["ex"] = g[f"f{h}"] - g.coin.map(drift[h])
        sl = stats.linregress(g.depth, g.ex)
        q = pd.qcut(g.depth, 3, labels=["deep", "mid", "shallow"])
        m = g.groupby(q, observed=True)["ex"].mean()
        res.append({"h": h, "n": len(g), "slope_ex_on_depth": sl.slope, "t": sl.slope / sl.stderr,
                    "mean_ex": g.ex.mean(), "t_mean": g.ex.mean() / (g.ex.std() / np.sqrt(len(g))),
                    "deep": m.get("deep"), "mid": m.get("mid"), "shallow": m.get("shallow")})
    out["by_horizon_choppy"] = pd.DataFrame(res)
    # all profiles at h=10, by trend group
    h = 10
    g = D[(D.pos % h == 0) & (D.depth < 0)].dropna(subset=["depth", "f10", "r60"]).copy()
    g["ex"] = g.f10 - g.coin.map(drift[10])
    g["trend"] = np.where(g.r60 > 0.1, "rising", np.where(g.r60 < -0.1, "falling", "choppy"))
    def summ(x):
        sl = stats.linregress(x.depth, x.ex) if len(x) > 10 else None
        return pd.Series({"n": len(x), "mean_ex": x.ex.mean(),
                          "t_mean": x.ex.mean() / (x.ex.std() / np.sqrt(len(x))),
                          "slope": sl.slope if sl else np.nan,
                          "t_slope": sl.slope / sl.stderr if sl else np.nan})
    out["h10_by_trend"] = g.groupby("trend").apply(summ)
    gc = g[g.trend == "choppy"]
    out["h10_choppy_by_coin"] = gc.groupby("coin").apply(summ)
    out["h10_choppy_by_window"] = gc.groupby("w").apply(summ)
    out["h10_choppy_by_upday"] = gc.groupby("up").apply(summ)
    out["h10_choppy_by_agit"] = gc.dropna(subset=["agit"]).groupby("agit").apply(summ)
    gc2 = gc.copy(); gc2["dq"] = pd.qcut(gc2.depth, 5, labels=False)
    out["h10_choppy_depth_quintile"] = gc2.groupby("dq").apply(summ)
    out["share_choppy_regime_vs_price"] = float((D.chop == ((D.r60.abs() <= 0.1))).mean())
    return out
