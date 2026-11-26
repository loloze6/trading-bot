def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in (3, 5, 10)}
        for w, df in wins.items():
            c = df["close"].values
            for h in (3, 5, 10):
                for i in range(0, len(c) - h, h):
                    allr[h].append(c[i + h] / c[i] - 1)
        drift[coin] = {h: np.mean(v) for h, v in allr.items()}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; v = df["volume"]
            ret10 = c / c.shift(10) - 1
            ret60 = c / c.shift(60) - 1
            m1 = v.rolling(30).mean(); m0 = m1.shift(30)
            shrink = -np.log(m1 / m0)
            dret = c.pct_change()
            vol30 = dret.rolling(30).std()
            volrank = vol30.rolling(60, min_periods=30).rank(pct=True)
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, len(df) - 5, 5):
                r = {"coin": coin, "win": w, "year": ts.iloc[i].year,
                     "fc": df["forecast"].iloc[i], "regime": df["regime"].iloc[i],
                     "ret10": ret10.iloc[i], "ret60": ret60.iloc[i],
                     "shrink": shrink.iloc[i], "volrank": volrank.iloc[i],
                     "day": ts.iloc[i].normalize()}
                for h in (3, 5, 10):
                    if i + h < len(df):
                        r[f"x{h}"] = -(c.iloc[i + h] / c.iloc[i] - 1 - drift[coin][h])
                rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g, col="x5"):
        g = g.dropna(subset=[col])
        if len(g) < 3: return pd.Series({"n": len(g), "mean": np.nan, "t_day": np.nan, "days": 0})
        s = g.groupby("day")[col].sum()
        n = len(g); m = g[col].mean()
        se = np.sqrt((s - s.index.map(g.groupby("day").size()).values * m).pow(2).sum()) / n
        return pd.Series({"n": n, "mean": m, "t_day": m / se if se > 0 else np.nan, "days": len(s)})
    sig = d[d.fc < 0].copy()
    fall = d[(d.regime == "trending")].copy()
    out = {}
    out["signal_all_h"] = pd.DataFrame({h: summ(sig, f"x{h}") for h in (3, 5, 10)})
    out["by_coin"] = sig.groupby("coin").apply(summ)
    out["by_window"] = sig.groupby("win").apply(summ)
    out["by_year"] = sig.groupby("year").apply(summ)
    sig["fcq"] = pd.qcut(sig.fc.abs(), 3, labels=["weak", "mid", "strong"])
    out["by_fc_tercile"] = sig.groupby("fcq").apply(summ)
    sig["r10q"] = pd.qcut(sig.ret10, 3, labels=["deep", "mid", "shallow"])
    out["by_ret10_tercile"] = sig.groupby("r10q").apply(summ)
    sig["agit"] = np.where(sig.volrank > 0.5, "agitated_rel", "calm_rel")
    out["by_agitation_proxy"] = sig.groupby("agit").apply(summ)
    # falling-market bars (trending regime), by volume shrink vs growth
    fall["vgrp"] = np.where(fall.shrink > 0, "shrinking", np.where(fall.shrink <= 0, "growing", "na"))
    out["falling_by_volume"] = fall.groupby("vgrp").apply(summ)
    f2 = fall.dropna(subset=["shrink"])
    f2["shq"] = pd.qcut(f2.shrink, 4, labels=["q1grow", "q2", "q3", "q4dry"])
    out["falling_by_shrink_quartile"] = f2.groupby("shq").apply(summ)
    out["falling_no_signal"] = summ(fall[fall.fc == 0]).to_frame("v")
    return out
