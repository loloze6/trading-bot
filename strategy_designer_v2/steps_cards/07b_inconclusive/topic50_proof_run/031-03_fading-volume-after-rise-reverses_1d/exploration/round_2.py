def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    col = "debug_info.components.vol_drop.last_history_value"
    rows = []
    drift = {}; usual = {}
    for coin, wins in bars.items():
        for h in [15, 30]:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = np.mean(rs); usual[(coin, h)] = np.std(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            reg = (df["regime"].astype(str) == "mean_reversion").values
            vr = df[col].astype(float).values if col in df.columns else np.full(len(df), np.nan)
            fc = df["forecast"].astype(float).values
            r60 = pd.Series(c).pct_change(60).values
            for h in [15, 30]:
                for i in range(0, len(c) - h, h):
                    if not reg[i]:
                        continue
                    r = c[i + h] / c[i] - 1
                    rows.append(dict(coin=coin, w=w, h=h, vr=vr[i], fc=fc[i], r60=r60[i],
                                     ex=r - drift[(coin, h)], st=(r - drift[(coin, h)]) / usual[(coin, h)]))
    R = pd.DataFrame(rows)
    def summ(g):
        n = len(g); m = g["ex"].mean()
        t = m / (g["ex"].std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series(dict(n=n, mean_ex=m, t=t, strength=g["st"].mean()))
    res = {}
    for h in [15, 30]:
        g = R[R.h == h].dropna(subset=["vr"])
        for name, gg in [("all", g), ("drop_only", g[g.vr < 0]), ("short_fc", g[g.fc < 0])]:
            if len(gg) > 4:
                s = stats.linregress(gg["vr"], gg["ex"])
                res[(h, name)] = dict(n=len(gg), slope=s.slope, t=s.slope / s.stderr, mean_ex=gg["ex"].mean())
    out["vr_slope_subsets"] = pd.DataFrame(res).T
    g = R[R.h == 30].dropna(subset=["vr"]).copy()
    g["drop_bucket"] = pd.cut(g["vr"], [-10, -0.3, -0.1, 0.1, 0.3, 10])
    out["h30_by_vr_bucket"] = g.groupby("drop_bucket").apply(summ)
    out["h30_by_fc_sign"] = g.groupby(np.sign(g["fc"])).apply(summ)
    g2 = R[(R.h == 30)].dropna(subset=["r60"]).copy()
    if len(g2) > 4:
        g2["trend"] = np.where(g2.r60 > 0.10, "rising", np.where(g2.r60 < -0.10, "falling", "choppy"))
        out["h30_by_trend60"] = g2.groupby("trend").apply(summ)
    out["h15_by_coin"] = R[R.h == 15].groupby("coin").apply(summ)
    return out
