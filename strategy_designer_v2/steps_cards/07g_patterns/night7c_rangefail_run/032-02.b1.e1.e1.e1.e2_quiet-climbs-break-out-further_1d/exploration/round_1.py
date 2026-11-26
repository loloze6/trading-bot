import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    out = {}
    H = 20
    # coin mean 20d return over all windows (non-overlapping)
    coin_mean = {}; coin_sd = {}
    for c in bars:
        rs = []
        for w, df in bars[c].items():
            cl = df["close"].values
            for i in range(0, len(cl) - H, H):
                rs.append(cl[i + H] / cl[i] - 1)
        coin_mean[c] = np.mean(rs); coin_sd[c] = np.std(rs, ddof=1)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            cl = df["close"].reset_index(drop=True)
            n = len(cl)
            prior_max = cl.shift(1).rolling(60).max()
            prior_min = cl.shift(1).rolling(60).min()
            r60 = cl.shift(1) / cl.shift(61) - 1
            r1 = cl / cl.shift(1) - 1
            vol20 = r1.rolling(20).std()
            vol120 = r1.rolling(120).std()
            r5 = cl / cl.shift(5) - 1
            r20p = cl / cl.shift(20) - 1
            dist_hi = cl / prior_max - 1
            dist_lo = cl / prior_min - 1
            rng = prior_max / prior_min - 1
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            fc = df["forecast"].reset_index(drop=True)
            for i in range(0, n - H, H):
                # all-bar grid sample
                rows.append(dict(coin=c, w=w, kind="grid", i=i, fwd=cl[i + H] / cl[i] - 1,
                                 r60=r60[i], r20=r20p[i], r5=r5[i], vol20=vol20[i], vol120=vol120[i],
                                 dhi=dist_hi[i], dlo=dist_lo[i], rng=rng[i], wd=ts[i].dayofweek, yr=ts[i].year,
                                 fc=fc[i]))
            # breakout cases: first breakout in each grid cell
            for g in range(0, n - H, H):
                for i in range(g, min(g + H, n - H)):
                    if not np.isnan(prior_max[i]) and cl[i] > prior_max[i]:
                        rows.append(dict(coin=c, w=w, kind="up", i=i, fwd=cl[i + H] / cl[i] - 1,
                                         r60=r60[i], r20=r20p[i], r5=r5[i], vol20=vol20[i], vol120=vol120[i],
                                         dhi=dist_hi[i], dlo=dist_lo[i], rng=rng[i], wd=ts[i].dayofweek,
                                         yr=ts[i].year, fc=fc[i]))
                        break
                for i in range(g, min(g + H, n - H)):
                    if not np.isnan(prior_min[i]) and cl[i] < prior_min[i]:
                        rows.append(dict(coin=c, w=w, kind="dn", i=i, fwd=cl[i + H] / cl[i] - 1,
                                         r60=r60[i], r20=r20p[i], r5=r5[i], vol20=vol20[i], vol120=vol120[i],
                                         dhi=dist_hi[i], dlo=dist_lo[i], rng=rng[i], wd=ts[i].dayofweek,
                                         yr=ts[i].year, fc=fc[i]))
                        break
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d["coin"].map(coin_mean)
    d["z"] = d["ex"] / d["coin"].map(coin_sd)
    def summ(g):
        return pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(), t=stats.ttest_1samp(g["ex"].dropna(), 0).statistic if len(g) > 2 else np.nan,
                              hit=(g["fwd"] > 0).mean()))
    out["by_kind"] = d.groupby("kind").apply(summ)
    out["kind_by_coin"] = d.groupby(["kind", "coin"]).apply(summ)
    out["kind_by_year"] = d.groupby(["kind", "yr"]).apply(summ)
    up = d[d.kind == "up"].dropna(subset=["r60"])
    up["q_r60"] = pd.qcut(up["r60"], 4, labels=False)
    out["up_by_r60_q"] = up.groupby("q_r60").apply(summ)
    up["q_dhi"] = pd.qcut(up["dhi"], 4, labels=False, duplicates="drop")
    out["up_by_breakdist_q"] = up.groupby("q_dhi").apply(summ)
    up["q_rng"] = pd.qcut(up["rng"], 4, labels=False)
    out["up_by_range_width_q"] = up.groupby("q_rng").apply(summ)
    up["vr"] = up["vol20"] / up["vol120"]
    up["q_vr"] = pd.qcut(up["vr"], 4, labels=False)
    out["up_by_volratio_q"] = up.groupby("q_vr").apply(summ)
    dn = d[d.kind == "dn"].dropna(subset=["r60"])
    dn["q_r60"] = pd.qcut(dn["r60"], 4, labels=False)
    out["dn_by_r60_q"] = dn.groupby("q_r60").apply(summ)
    gr = d[d.kind == "grid"].dropna(subset=["r60", "vol20", "dhi"])
    for col in ["r60", "r20", "r5", "dhi", "dlo", "vol20", "rng"]:
        gr["q"] = pd.qcut(gr[col], 5, labels=False, duplicates="drop")
        out["grid_by_" + col] = gr.groupby("q").apply(summ)
    out["grid_by_weekday"] = gr.groupby("wd").apply(summ)
    return out
