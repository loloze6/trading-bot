import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    allz = []
    H = [1, 2, 3, 5, 10]
    drift = {}
    for coin, wins in data["bars"].items():
        rets = {h: [] for h in H}
        for w, b in wins.items():
            c = b["close"].values
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                rets[h].extend(list(c[idx + h] / c[idx] - 1))
        drift[coin] = {h: np.mean(rets[h]) for h in H}
        sd1 = np.std(rets[1])
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            vol = r1.rolling(20, min_periods=20).std()
            z = r1 / vol.shift(0)
            r90 = c / c.shift(90) - 1
            fall = np.where(r90.notna(), r90 < 0, b["regime"] == "mean_reversion")
            f = b["forecast"].fillna(0).values
            low = 0.0
            n = len(b)
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for t in range(n):
                case = False
                if f[t] >= 0:
                    low = 0.0
                else:
                    if f[t] <= low - 2:
                        case = True
                        low = f[t]
                fwd = {h: (c.iloc[t + h] / c.iloc[t] - 1) if t + h < n else np.nan for h in H}
                d = dict(coin=coin, win=w, year=yr[t], z=z.iloc[t], r1=r1.iloc[t],
                         r90=r90.iloc[t], fall=bool(fall[t]), case=case, fc=f[t])
                for h in H:
                    d[f"ex{h}"] = -(fwd[h] - drift[coin][h]) if not np.isnan(fwd[h]) else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    cs = df[df.case]
    out = {}
    def summ(g, col="ex1"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["cases_n"] = len(cs)
    out["by_horizon"] = pd.DataFrame({h: summ(cs, f"ex{h}") for h in H}).T
    out["by_coin"] = cs.groupby("coin").apply(summ)
    out["by_year"] = cs.groupby("year").apply(summ)
    cs = cs.copy()
    cs["fq"] = pd.qcut(cs["fc"].abs().rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["by_forecast_quartile"] = cs.groupby("fq").apply(summ)
    cs["zq"] = pd.qcut(cs["z"].rank(method="first"), 4, labels=["z1", "z2", "z3", "z4"])
    out["by_z_quartile"] = cs.groupby("zq").apply(lambda g: pd.concat([summ(g), pd.Series({"zmean": g.z.mean()})]))
    cs["dq"] = pd.qcut(cs["r90"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
    out["by_r90_depth"] = cs.groupby("dq").apply(lambda g: pd.concat([summ(g), summ(g, "ex3").add_prefix("h3_")]))
    # all bars with z>1.5: falling vs rising, graded by z bin
    a = df[df.z.notna() & (df.z > 0)].copy()
    a["zb"] = pd.cut(a.z, [0, 1, 1.5, 2, 3, 20])
    out["allbars_fall_vs_rise_h1"] = a.groupby(["fall", "zb"]).apply(summ).unstack(0)
    out["allbars_fall_vs_rise_h3"] = a.groupby(["fall", "zb"]).apply(lambda g: summ(g, "ex3")).unstack(0)
    return out
