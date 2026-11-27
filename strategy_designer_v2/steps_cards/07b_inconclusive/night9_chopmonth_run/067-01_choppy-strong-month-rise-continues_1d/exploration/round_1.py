import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for h in [3, 7, 14]:
        for coin, ws in bars.items():
            cells = []
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                c = df["close"].values
                col = "debug_info.components.month_rise.last_history_value"
                r30 = df[col].values if col in df else np.full(len(df), np.nan)
                fc = df["forecast"].values
                reg = df["regime"].values
                # recompute 30d return from prices too
                r30p = pd.Series(c).pct_change(30).values * 100
                for i in range(0, len(df) - h, h):
                    cells.append(dict(coin=coin, w=w, h=h, fwd=c[i + h] / c[i] - 1,
                                      r30=r30[i], r30p=r30p[i], fc=fc[i], chop=(reg[i] == "unknown")))
            cd = pd.DataFrame(cells)
            if len(cd) == 0:
                continue
            cd["ex"] = cd["fwd"] - cd["fwd"].mean()
            rows.append(cd)
    A = pd.concat(rows)
    out = {}

    def slope(d, x):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 10:
            return (np.nan, np.nan, len(d), np.nan)
        r = stats.linregress(d[x], d["ex"])
        return (r.slope, r.slope / r.stderr, len(d), d["ex"].mean())

    res = []
    for h in [3, 7, 14]:
        d = A[(A.h == h) & A.chop]
        d = d.assign(r30u=d["r30"].fillna(d["r30p"]))
        for name, sub in [("all", d), ("up", d[d.r30u > 0]), ("down", d[d.r30u <= 0]), ("fc>0", d[d.fc > 0])]:
            s, t, n, m = slope(sub, "r30u")
            res.append(dict(h=h, part=name, slope_per_pct=s, t=t, n=n, mean_ex=m,
                            t_mean=sub["ex"].mean() / (sub["ex"].std() / np.sqrt(len(sub))) if len(sub) > 2 else np.nan))
    out["slopes_by_h_side"] = pd.DataFrame(res)

    d7 = A[(A.h == 7) & A.chop].copy()
    d7["r30u"] = d7["r30"].fillna(d7["r30p"])
    d7["q"] = pd.qcut(d7["r30u"], 6, labels=False)
    out["sextiles_7d"] = d7.groupby("q").agg(r30_mean=("r30u", "mean"), ex_mean=("ex", "mean"),
                                             ex_std=("ex", "std"), n=("ex", "size"))
    g = []
    for coin, sub in d7.groupby("coin"):
        s, t, n, m = slope(sub, "r30u")
        su = sub[sub.r30u > 0]
        s2, t2, n2, m2 = slope(su, "r30u")
        g.append(dict(coin=coin, slope_all=s, t_all=t, n_all=n, slope_up=s2, t_up=t2, n_up=n2, mean_ex_up=m2))
    out["by_coin_7d"] = pd.DataFrame(g)
    g = []
    for w, sub in d7.groupby("w"):
        s, t, n, m = slope(sub, "r30u")
        su = sub[sub.r30u > 0]
        s2, t2, n2, m2 = slope(su, "r30u")
        g.append(dict(w=w, slope_all=s, t_all=t, n_all=n, t_up=t2, n_up=n2, mean_ex_up=m2))
    out["by_window_7d"] = pd.DataFrame(g)
    out["share_chop_cells_7d"] = float(A[A.h == 7].chop.mean())
    out["r30_vs_r30p_corr"] = float(d7[["r30", "r30p"]].dropna().corr().iloc[0, 1])
    return out
