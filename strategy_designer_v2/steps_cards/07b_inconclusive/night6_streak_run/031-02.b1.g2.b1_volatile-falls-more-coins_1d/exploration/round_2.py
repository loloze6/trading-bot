import numpy as np, pandas as pd

def _cases(data, h):
    rows = []
    for coin, wins in data["bars"].items():
        per = []
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r1 = c.pct_change()
            vol = r1.rolling(60, min_periods=60).std()
            r3 = c / c.shift(3) - 1
            fwd = c.shift(-h) / c - 1
            idx = np.arange(0, len(c), h)
            g = pd.DataFrame({"r1": r1.iloc[idx].values, "vol": vol.iloc[idx].values, "r3": r3.iloc[idx].values,
                              "fwd": fwd.iloc[idx].values, "day": ts.iloc[idx].dt.floor("D").values,
                              "year": ts.iloc[idx].dt.year.values})
            g["coin"] = coin; g["win"] = w
            per.append(g)
        g = pd.concat(per)
        g["ex"] = g["fwd"] - g["fwd"].mean()
        g["usual"] = g["fwd"].std()
        rows.append(g)
    return pd.concat(rows).dropna(subset=["fwd", "r1"])

def _slope_t(y, x, day):
    x = np.asarray(x, float); y = np.asarray(y, float)
    xm = x - x.mean(); b = (xm * (y - y.mean())).sum() / (xm ** 2).sum()
    e = y - y.mean() - b * xm
    s = pd.DataFrame({"s": xm * e, "d": day}).groupby("d")["s"].sum()
    se = np.sqrt((s ** 2).sum()) / (xm ** 2).sum()
    return b, b / se

def _clt(x, day):
    d = pd.DataFrame({"x": x - x.mean(), "d": day}).groupby("d")["x"].sum()
    se = np.sqrt((d ** 2).sum()) / len(x)
    return x.mean() / se if se > 0 else np.nan

def explore(data):
    out = {}
    g = _cases(data, 1)
    dn = g[g.r1 < 0].copy()
    dn["fall"] = -dn.r1
    dn["fq"] = pd.qcut(dn["fall"], 10, labels=False)
    q = dn.groupby("fq").agg(n=("ex", "size"), fall=("fall", "mean"), ex=("ex", "mean"),
                             strength=("ex", lambda s: (s / dn.loc[s.index, "usual"]).mean()))
    q["t"] = [ _clt(s.ex.values, s.day.values) for _, s in dn.groupby("fq")]
    out["h1_fall_decile"] = q
    # trimmed: without top 1% falls
    cut = dn.fall.quantile(0.99)
    s = dn[dn.fall < cut]; b, t = _slope_t(s.ex, s.fall, s.day.values)
    out["h1_slope_without_top1pct"] = pd.Series({"b": b, "t": t, "n": len(s)})
    b, t = _slope_t(dn.ex, dn.fall, dn.day.values)
    out["h1_slope_all"] = pd.Series({"b": b, "t": t, "n": len(dn), "days": dn.day.nunique()})
    dv = dn.dropna(subset=["vol"]).copy(); dv["vt"] = pd.qcut(dv.vol, 3, labels=False)
    vt = []
    for k, s in dv.groupby("vt"):
        b, t = _slope_t(s.ex, s.fall, s.day.values); vt.append({"vol_terc": k, "n": len(s), "b": b, "t": t, "mean_ex": s.ex.mean()})
    out["h1_by_vol_tercile"] = pd.DataFrame(vt)
    yy = []
    for k, s in dn.groupby("year"):
        b, t = _slope_t(s.ex, s.fall, s.day.values); yy.append({"year": k, "n": len(s), "b": b, "t": t})
    out["h1_by_year"] = pd.DataFrame(yy)
    cy = []
    for k, s in dn.groupby("coin"):
        b, t = _slope_t(s.ex, s.fall, s.day.values); cy.append({"coin": k, "n": len(s), "b": b, "t": t})
    out["h1_by_coin"] = pd.DataFrame(cy)
    # regime: prior 3-day return sign
    rg = []
    for lab, s in [("r3<0", dn[dn.r3 < 0]), ("r3>=0", dn[dn.r3 >= 0])]:
        b, t = _slope_t(s.ex, s.fall, s.day.values); rg.append({"reg": lab, "n": len(s), "b": b, "t": t})
    out["h1_by_prior3d"] = pd.DataFrame(rg)
    # 2-day forward split into day1 and day2 using h=1 grid
    allr = []
    for coin, wins in data["bars"].items():
        for w, bb in wins.items():
            c = bb["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(bb["timestamp"]).reset_index(drop=True)
            r1 = c.pct_change(); d2 = c.shift(-2) / c.shift(-1) - 1
            allr.append(pd.DataFrame({"r1": r1, "d2": d2, "coin": coin, "day": ts.dt.floor("D")}))
    a = pd.concat(allr).dropna()
    a["ex2"] = a.d2 - a.groupby("coin").d2.transform("mean")
    a = a[a.r1 < 0]
    b, t = _slope_t(a.ex2, -a.r1, a.day.values)
    out["second_day_only_overlapping"] = pd.Series({"b": b, "t": t, "n": len(a)})
    return out
