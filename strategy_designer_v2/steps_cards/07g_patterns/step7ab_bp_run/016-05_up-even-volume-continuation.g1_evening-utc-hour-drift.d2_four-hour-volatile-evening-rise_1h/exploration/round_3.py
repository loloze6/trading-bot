import numpy as np, pandas as pd

def tstat(x):
    x = pd.Series(x).dropna()
    return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan

def explore(data):
    bars = data["bars"]; out = {}
    rows = []
    for coin, wins in bars.items():
        g24 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 24, 24)
            g24.extend(list(c[idx + 24] / c[idx] - 1))
        m24, s24 = np.mean(g24), np.std(g24)
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]); c = df["close"].values.astype(float)
            lr = np.r_[np.nan, np.diff(np.log(c))]
            for t in np.where(ts.dt.hour.values == 23)[0]:
                if t + 24 >= len(c) or t < 168: continue
                nxt = ts.iloc[t] + pd.Timedelta(hours=1)
                F = c[t + 24] / c[t] - 1
                p7 = c[t] / c[t - 168] - 1
                p1 = c[t] / c[t - 24] - 1
                v7 = np.nanstd(lr[t - 167:t + 1])
                rows.append((coin, w, nxt.weekday(), nxt.year, F - m24, (F - m24) / s24, p7, p1, p7 / (v7 * np.sqrt(168))))
    D = pd.DataFrame(rows, columns=["coin", "w", "wd", "yr", "Fu", "Fz", "p7", "p1", "p7z"])
    D["pt"] = D.groupby(["coin", "wd"])["p7"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    piv = D.groupby(["wd", "pt"])["Fu"].mean().unstack() * 1e4
    piv["top_minus_bottom"] = piv[2] - piv[0]
    piv["t_top"] = D[D["pt"] == 2].groupby("wd")["Fu"].apply(tstat)
    out["next-day unusual move (bps) by weekday x 7d-return third"] = piv.round(2)
    D["ptall"] = D.groupby("coin")["p7z"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["all days: next-day by 7d return/vol quintile"] = D.groupby("ptall").agg(n=("Fu", "size"), Fu_bps=("Fu", lambda x: x.mean() * 1e4), Fz=("Fz", "mean"), t=("Fu", tstat)).round(3)
    sat = D[D["wd"] == 5]
    top = sat[sat["pt"] == 2]
    out["Sat top 7d third by coin"] = top.groupby("coin").agg(n=("Fu", "size"), Fu_bps=("Fu", lambda x: x.mean() * 1e4), t=("Fu", tstat)).round(2)
    out["Sat top 7d third by year"] = top.groupby("yr").agg(n=("Fu", "size"), Fu_bps=("Fu", lambda x: x.mean() * 1e4), t=("Fu", tstat)).round(2)
    out["Sat top third share of windows positive"] = pd.Series({"windows": top["w"].nunique(), "share>0": top.groupby("w")["Fu"].mean().gt(0).mean()})
    # Saturday: correlation of next-day with p7 standardized, and with Friday's own day return
    out["Sat corr"] = pd.Series({"corr Fz~p7z": sat["Fz"].corr(sat["p7z"]), "corr Fz~p1": sat["Fz"].corr(sat["p1"]),
                                 "other days corr Fz~p7z": D[D["wd"] != 5]["Fz"].corr(D[D["wd"] != 5]["p7z"]), "n_sat": len(sat)})
    return out
