import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 5, 10]
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            f = df["forecast"].fillna(0).values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r1 = pd.Series(cl).pct_change()
            z = (r1 / r1.rolling(20).std()).values
            r20 = (pd.Series(cl) / pd.Series(cl).shift(20) - 1).values
            dep = df["debug_info.components.depth90.last_history_value"].values
            for g in range(0, n, 5):
                for t in range(g, min(g + 5, n)):
                    prev = f[t - 1] if t > 0 else 0
                    if f[t] <= -2 and f[t] < prev - 1e-9:
                        if t + 5 >= n: break
                        rec = dict(coin=c, year=yr[t], f=f[t], z=z[t], dep=dep[t], r20=r20[t])
                        for h in H:
                            if t + h < n:
                                rec[f"u{h}"] = -(cl[t + h] / cl[t] - 1 - drift[(c, h)])
                        rows.append(rec)
                        break
    d = pd.DataFrame(rows)
    def summ(x, col="u5"):
        v = x[col].dropna()
        return pd.Series({"n": len(v), "mean": v.mean(), "t": v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan})
    out = {}
    out["depth_quartile_edges"] = d["dep"].quantile([0, .25, .5, .75, 1])
    q25 = d["dep"].quantile(.25)
    out["excl_deepest_u5"] = summ(d[d["dep"] > q25])
    out["excl_deepest_u10"] = summ(d[d["dep"] > q25], "u10")
    out["deepest_u5"] = summ(d[d["dep"] <= q25])
    d["dq"] = pd.qcut(d["dep"], 4, labels=["deepest", "q2", "q3", "shallowest"])
    out["deepest_share_by_year"] = d.groupby("year")["dq"].apply(lambda s: (s == "deepest").mean())
    out["by_year_excl_deepest_u5"] = d[d["dep"] > q25].groupby("year").apply(summ)
    out["by_coin_excl_deepest_u5"] = d[d["dep"] > q25].groupby("coin").apply(summ)
    d["r20s"] = np.where(d["r20"] < 0, "r20<0", "r20>=0")
    out["by_r20sign_u5"] = d.groupby("r20s").apply(summ)
    sl = stats.linregress(d["dep"].dropna(), d.loc[d["dep"].notna(), "u5"])
    out["slope_dep_u5"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr})
    x = d.dropna(subset=["dep", "u10"])
    sl = stats.linregress(x["dep"], x["u10"])
    out["slope_dep_u10"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr})
    out["share_cases_z_gt_2"] = (d["z"] > 2).mean()
    return out
