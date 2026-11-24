import numpy as np, pandas as pd
from scipy import stats

def _cases(data, h):
    rows = []
    for coin, wins in data["bars"].items():
        # coin mean h-day return on grid over all windows
        allr = []
        per = []
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r1 = c.pct_change()
            vol = r1.rolling(60, min_periods=60).std()
            fwd = c.shift(-h) / c - 1
            fc = b["debug_info.components.fall_vol.post_pipeline_value"].astype(float).reset_index(drop=True) if "debug_info.components.fall_vol.post_pipeline_value" in b else pd.Series(np.nan, index=c.index)
            idx = np.arange(0, len(c), h)
            g = pd.DataFrame({"r1": r1.iloc[idx].values, "vol": vol.iloc[idx].values, "fwd": fwd.iloc[idx].values,
                              "fc": fc.iloc[idx].values, "day": ts.iloc[idx].dt.floor("D").values,
                              "year": ts.iloc[idx].dt.year.values})
            g["coin"] = coin; g["win"] = w
            per.append(g)
        g = pd.concat(per)
        g["ex"] = g["fwd"] - g["fwd"].mean()
        rows.append(g)
    return pd.concat(rows).dropna(subset=["fwd", "r1"])

def _clt(x, day):
    d = pd.DataFrame({"x": x - x.mean(), "d": day}).groupby("d")["x"].sum()
    se = np.sqrt((d ** 2).sum()) / len(x)
    return x.mean() / se if se > 0 else np.nan

def _slope_t(y, x, day):
    x = np.asarray(x, float); y = np.asarray(y, float)
    xm = x - x.mean(); b = (xm * (y - y.mean())).sum() / (xm ** 2).sum()
    e = y - y.mean() - b * xm
    s = pd.DataFrame({"s": xm * e, "d": day}).groupby("d")["s"].sum()
    se = np.sqrt((s ** 2).sum()) / (xm ** 2).sum()
    return b, b / se

def explore(data):
    out = {}
    hz = []
    for h in [1, 2, 3, 5, 10]:
        g = _cases(data, h)
        dn = g[g.r1 < 0]; up = g[g.r1 > 0]
        b1, t1 = _slope_t(dn.ex, -dn.r1, dn.day.values)
        dv = dn.dropna(subset=["vol"])
        b2, t2 = _slope_t(dv.ex, -dv.r1 * dv.vol, dv.day.values)
        b3, t3 = _slope_t(dv.ex, -dv.r1 / dv.vol, dv.day.values)
        b4, t4 = _slope_t(up.ex, up.r1, up.day.values)
        hz.append({"h": h, "n_down": len(dn), "t_fall": t1, "t_fall_x_vol": t2, "t_fall_over_vol": t3,
                   "t_rise_up_days": t4, "mean_ex_down": dn.ex.mean(), "t_mean_down": _clt(dn.ex.values, dn.day.values)})
    out["horizons"] = pd.DataFrame(hz)
    g = _cases(data, 2); dn = g[g.r1 < 0].dropna(subset=["vol"]).copy()
    dn["z"] = -dn.r1 / dn.vol
    dn["fq"] = pd.qcut(dn["z"], 5, labels=False)
    dn["vq"] = pd.qcut(dn["vol"], 3, labels=False)
    out["fall_z_quintile"] = dn.groupby("fq").agg(n=("ex", "size"), z=("z", "mean"), ex=("ex", "mean"))
    out["fallz_x_volterc"] = dn.pivot_table(index="fq", columns="vq", values="ex", aggfunc="mean")
    cy = []
    for k, s in dn.groupby("coin"):
        if len(s) > 50:
            b, t = _slope_t(s.ex, s.z, s.day.values); cy.append({"coin": k, "n": len(s), "t_z": t, "mean_ex": s.ex.mean()})
    out["by_coin"] = pd.DataFrame(cy)
    yy = []
    for k, s in dn.groupby("year"):
        b, t = _slope_t(s.ex, s.z, s.day.values); yy.append({"year": k, "n": len(s), "t_z": t, "mean_ex": s.ex.mean()})
    out["by_year"] = pd.DataFrame(yy)
    return out
