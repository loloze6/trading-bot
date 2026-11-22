import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [5, 10, 20]
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            r1 = pd.Series(cl).pct_change()
            vol = r1.rolling(20, min_periods=10).std()
            z = (r1 / vol).values
            r90 = (pd.Series(cl) / pd.Series(cl).shift(90) - 1).values
            fc = df["forecast"].values
            reg = df["regime"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(cl)
            for thr, kind in [(1.0, "z1"), (1.5, "z15"), (2.0, "z2")]:
                for s in range(0, n, 10):
                    for i in range(s, min(s + 10, n)):
                        if np.isfinite(z[i]) and z[i] >= thr and reg[i] == "trending":
                            rec = dict(coin=c, win=w, year=yr[i], fc=fc[i], z=z[i], r90=r90[i], kind=kind)
                            for h in H:
                                rec[f"u{h}"] = (cl[i + h] / cl[i] - 1 - drift[(c, h)]) if i + h < n else np.nan
                            rows.append(rec); break
            for s in range(0, n, 10):
                for i in range(s, min(s + 10, n)):
                    if fc[i] >= 2:
                        rows.append(dict(coin=c, win=w, year=yr[i], fc=fc[i], z=z[i], r90=r90[i], kind="plan",
                                         **{f"u{h}": (cl[i + h] / cl[i] - 1 - drift[(c, h)]) if i + h < n else np.nan for h in H}))
                        break
    d = pd.DataFrame(rows)
    def summ(g):
        out = {}
        for h in H:
            x = g[f"u{h}"].dropna()
            out[f"m{h}"] = x.mean(); out[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        out["n"] = len(g)
        return pd.Series(out)
    p = d[d.kind == "plan"].copy()
    p["zbin"] = pd.cut(p["z"], [-10, 0, 0.5, 1, 1.5, 2, 10])
    z15 = d[d.kind == "z15"].copy()
    z15["r90q"] = pd.qcut(z15["r90"], 3, labels=False, duplicates="drop")
    return {
        "plan_fc_quantiles": p["fc"].describe(),
        "plan_by_rawz": p.groupby("zbin").apply(summ),
        "trend_by_thr": d[d.kind != "plan"].groupby("kind").apply(summ),
        "z15_by_coin": z15.groupby("coin").apply(summ),
        "z15_by_year": z15.groupby("year").apply(summ),
        "z15_by_r90tercile": z15.groupby("r90q").apply(summ),
        "z15_corr_z_u10": pd.Series({"corr": z15[["z", "u10"]].dropna().corr().iloc[0, 1]}),
    }
