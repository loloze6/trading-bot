import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            f = df["forecast"].values.astype(float)
            raw = df["debug_info.components.grind_fall.last_history_value"].values.astype(float) if "debug_info.components.grind_fall.last_history_value" in df else np.full(n, np.nan)
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n, 72):
                r = {"coin": coin, "w": w, "year": ts.iloc[i].year, "f": f[i], "raw": raw[i]}
                for h in (24, 72, 168):
                    r["fwd%d" % h] = c[i+h]/c[i]-1 if i+h < n else np.nan
                r["past72"] = c[i]/c[i-72]-1 if i >= 72 else np.nan
                r["past720"] = c[i]/c[i-720]-1 if i >= 720 else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    for h in (24, 72, 168):
        d["ex%d" % h] = d["fwd%d" % h] - d.groupby("coin")["fwd%d" % h].transform("mean")
    a = d[(d.f < 0) & d.fwd72.notna()].copy()
    a["gain"] = a.f/10*a.ex72
    def tm(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["all"] = tm(a.gain)
    out["by_coin"] = a.groupby("coin").gain.apply(tm).unstack()
    out["by_year"] = a.groupby("year").gain.apply(tm).unstack()
    a["fq"] = pd.qcut(a.f, 5, labels=False)  # 0 = most negative
    out["fq_ex72"] = a.groupby("fq").agg(n=("ex72","size"), f=("f","mean"), ex24=("ex24","mean"), ex72=("ex72","mean"), ex168=("ex168","mean"), past72=("past72","mean"))
    a["pq"] = pd.qcut(a.past72, 3, labels=False)  # 0 = biggest fall
    out["fallsize_x_fq_ex72"] = a.groupby(["pq", pd.qcut(a.f, 2, labels=False)]).ex72.agg(["size","mean"]).unstack()
    a["trend"] = np.sign(a.past720)
    out["by_30d_trend"] = a.groupby("trend").gain.apply(tm).unstack()
    out["ex72_by_30d_trend"] = a.groupby("trend").ex72.apply(tm).unstack()
    for h in (24, 168):
        g = a.f/10*a["ex%d" % h]
        out["gain_h%d" % h] = tm(g)
    # flat bars vs short bars excess return
    b = d[d.fwd72.notna()]
    out["ex72_short_vs_flat"] = pd.DataFrame({"short": tm(b[b.f<0].ex72), "flat": tm(b[b.f==0].ex72)})
    # correlation raw grind (unstandardised) with ex72 in falls
    aa = a.dropna(subset=["raw"])
    out["spearman_raw_ex72"] = pd.Series(stats.spearmanr(aa.raw, aa.ex72)[:2], index=["rho","p"])
    out["spearman_f_ex72"] = pd.Series(stats.spearmanr(a.f, a.ex72)[:2], index=["rho","p"])
    return out
