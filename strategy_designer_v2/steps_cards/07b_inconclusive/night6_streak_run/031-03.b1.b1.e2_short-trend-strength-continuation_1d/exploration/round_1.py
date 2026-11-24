import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["debug_info.components.scaled_rise.post_pipeline_value"].astype(float).values
            r1 = pd.Series(c).pct_change()
            sd = r1.rolling(60, min_periods=40).std().values
            r10 = pd.Series(c).pct_change(10).values
            z = r10 / (sd * np.sqrt(10))
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            for h in [1, 3, 5, 10, 20]:
                for i in range(0, n - h, h):
                    rows.append((coin, w, h, i, yr[i], f[i], z[i], c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows, columns=["coin", "w", "h", "i", "yr", "f", "z", "ret"])
    d["drift"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["drift"]
    out = {}

    # slope t by horizon, f > 0
    res = []
    for h in [1, 3, 5, 10, 20]:
        s = d[(d.h == h) & (d.f > 0)].dropna(subset=["f", "ex"])
        sl = stats.linregress(s.f, s.ex)
        top = s[s.f >= s.f.quantile(0.8)].ex
        res.append((h, len(s), sl.slope * 10, sl.slope / sl.stderr, s.ex.mean(), top.mean(),
                    top.mean() / top.std() * np.sqrt(len(top))))
    out["by_horizon_fpos"] = pd.DataFrame(
        res, columns=["h", "n", "slope_per10", "t_ols", "mean_ex", "top20_ex", "top20_t"])

    s5 = d[(d.h == 5)].dropna(subset=["z", "ex"]).copy()
    s5["zq"] = pd.qcut(s5.z, 10, labels=False)
    out["h5_ex_by_z_decile_all"] = s5.groupby("zq").agg(
        z=("z", "mean"), n=("ex", "size"), ex=("ex", "mean"),
        t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))

    p = d[(d.h == 5) & (d.f > 0)].dropna(subset=["f", "ex"]).copy()
    p["fq"] = pd.qcut(p.f, 5, labels=False, duplicates="drop")
    out["h5_ex_by_f_quintile"] = p.groupby("fq").agg(
        f=("f", "mean"), n=("ex", "size"), ex=("ex", "mean"),
        t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))

    def slope_t(g):
        if len(g) < 30:
            return pd.Series({"n": len(g), "slope_per10": np.nan, "t": np.nan, "mean_ex": g.ex.mean()})
        sl = stats.linregress(g.f, g.ex)
        return pd.Series({"n": len(g), "slope_per10": sl.slope * 10,
                          "t": sl.slope / sl.stderr, "mean_ex": g.ex.mean()})

    out["h5_by_coin"] = p.groupby("coin").apply(slope_t)
    out["h5_by_year"] = p.groupby("yr").apply(slope_t)
    return out
