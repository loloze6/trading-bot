import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [1, 2, 3]
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values.astype(float)
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values.astype(float); n = len(cl)
            s = pd.Series(cl); r1 = s.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            z = (r1 / sd30).values
            prior5 = ((s.shift(1) / s.shift(6) - 1) / sd30).values
            reg = df["regime"].astype(str).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in H:
                for i in range(0, n - h, h):
                    if reg[i] not in ("mean_reversion", "unknown") or not (r1.values[i] > 0):
                        continue
                    ret = cl[i + h] / cl[i] - 1
                    rows.append(dict(h=h, coin=c, win=w, year=yr[i], z=z[i], prior=prior5[i],
                                     fell=prior5[i] < 0, u=-(ret - drift[(c, h)]),
                                     day=str(df["timestamp"].iloc[i])[:10]))
    d = pd.DataFrame(rows).dropna(subset=["z", "u"])
    def summ(x):
        if len(x) < 3: return pd.Series({"n": len(x)})
        m = x.u.mean()
        dev = x.groupby("day")["u"].apply(lambda v: (v - m).sum())
        G = len(dev); se = np.sqrt((dev**2).sum() * G / (G - 1)) / len(x)
        return pd.Series({"n": len(x), "days": G, "mean": m, "t_day": m / se})
    out = {}
    out["all_updays_by_h"] = d.groupby("h").apply(summ).reset_index()
    out["all_updays_by_h_fell"] = d.groupby(["h", "fell"]).apply(summ).reset_index()
    d1 = d[d.h == 1].copy()
    d1["zq"] = pd.qcut(d1.z, 5, labels=False, duplicates="drop")
    out["h1_by_z_quintile"] = d1.groupby("zq").apply(lambda x: pd.concat([summ(x), pd.Series({"z": x.z.mean()})])).reset_index()
    out["h1_by_year"] = d1.groupby("year").apply(summ).reset_index()
    out["h1_by_win"] = d1.groupby("win").apply(summ).reset_index()
    out["h1_by_coin"] = d1.groupby("coin").apply(summ).reset_index()
    out["h1_corr_z_u"] = float(np.corrcoef(d1.z, d1.u)[0, 1])
    d2 = d1.copy(); d2["us"] = d2.u
    b = np.polyfit(d2.z, d2.u, 1)
    res = d2.u - np.polyval(b, d2.z)
    se = np.sqrt((res**2).sum() / (len(d2) - 2) / ((d2.z - d2.z.mean())**2).sum())
    out["h1_slope_u_on_z"] = pd.Series({"slope": b[0], "t": b[0] / se, "n": len(d2)})
    d3 = d[d.h == 3].copy()
    d3["zq"] = pd.qcut(d3.z, 5, labels=False, duplicates="drop")
    out["h3_by_z_quintile"] = d3.groupby("zq").apply(lambda x: pd.concat([summ(x), pd.Series({"z": x.z.mean()})])).reset_index()
    return out
