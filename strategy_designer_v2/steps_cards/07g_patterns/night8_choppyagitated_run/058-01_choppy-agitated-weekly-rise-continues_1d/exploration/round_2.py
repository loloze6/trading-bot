import pandas as pd, numpy as np
from scipy import stats

def ct(df, col, daycol="day"):
    d = df.dropna(subset=[col])
    if len(d) < 3:
        return pd.Series({"n": len(d), "days": d[daycol].nunique() if len(d) else 0, "mean": d[col].mean() if len(d) else np.nan, "t": np.nan})
    m = d[col].mean()
    s = (d[col] - m).groupby(d[daycol]).sum()
    D = len(s)
    se = np.sqrt((s**2).sum() * D/(D-1)) / len(d) if D > 1 else np.nan
    return pd.Series({"n": len(d), "days": D, "mean": m, "t": m/se if se and se > 0 else np.nan})

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        g7 = []; g3 = []
        for w, b in wins.items():
            c = b["close"].values
            g7 += [c[i+7]/c[i]-1 for i in range(0, len(c)-7, 7)]
            g3 += [c[i+3]/c[i]-1 for i in range(0, len(c)-3, 3)]
        m7, m3 = np.mean(g7), np.mean(g3)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r1 = c.pct_change(); sd30 = r1.rolling(30).std()
            r7 = c/c.shift(7)-1
            z7 = r7/(sd30*np.sqrt(7))
            r60 = c/c.shift(60)-1
            f7 = c.shift(-7)/c-1; f3 = c.shift(-3)/c-1
            day = pd.to_datetime(b["timestamp"]).dt.floor("D")
            inp = b["regime"] == "unknown"
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for i in range(0, len(b)-7, 7):
                rows.append(dict(h=7, coin=coin, win=w, day=day[i], yr=yr[i], inp=inp[i], z=z7[i],
                                 r60=r60[i], fx=f7[i]-m7))
            for i in range(0, len(b)-3, 3):
                rows.append(dict(h=3, coin=coin, win=w, day=day[i], yr=yr[i], inp=inp[i], z=z7[i],
                                 r60=r60[i], fx=f3[i]-m3))
    G = pd.DataFrame(rows)
    out = {}
    for h in (7, 3):
        g = G[(G.h == h)]
        gi = g[g.inp]
        out[f"h{h}_inprof_all"] = ct(gi, "fx")
        out[f"h{h}_inprof_by_sign"] = gi.dropna(subset=["z"]).groupby(gi["z"] > 0).apply(lambda d: ct(d, "fx"))
        out[f"h{h}_inprof_by_coin"] = gi.groupby("coin").apply(lambda d: ct(d, "fx"))
        out[f"h{h}_inprof_by_win"] = gi.groupby("win").apply(lambda d: ct(d, "fx"))
        gd = gi.dropna(subset=["z", "fx"])
        out[f"h{h}_inprof_spearman_z"] = pd.Series({"rho": stats.spearmanr(gd.z, gd.fx)[0] if len(gd) > 5 else np.nan, "n": len(gd)})
        go = g[~g.inp].dropna(subset=["z", "fx"]).copy()
        go["zq"] = pd.qcut(go.z, 5, labels=False)
        out[f"h{h}_outprof_zq"] = go.groupby("zq").apply(lambda d: ct(d, "fx"))
        go2 = g.dropna(subset=["r60", "fx"]).copy()
        go2["trend"] = np.where(go2.r60 > 0.1, "rising", np.where(go2.r60 < -0.1, "falling", "choppy"))
        out[f"h{h}_by_trend"] = go2.groupby("trend").apply(lambda d: ct(d, "fx"))
    return out
