import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            f = df["forecast"].values
            raw = df.get("debug_info.components.stretch.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            lr = np.r_[np.nan, np.diff(np.log(c))]
            vol30 = pd.Series(lr).rolling(30).std().values
            ts = pd.to_datetime(df["timestamp"])
            for h in [1, 3, 5, 10, 20]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, i=i, f=f[i], raw=raw[i],
                                     ret=c[i + h] / c[i] - 1, vol30=vol30[i],
                                     year=ts[i].year, day=ts[i].normalize()))
    d = pd.DataFrame(rows)
    d["mu"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["mu"]
    a = d[d.f != 0].copy()
    a["side"] = np.where(a.f > 0, "long", "short")
    a["sx"] = np.sign(a.f) * a.ex
    out = {}

    def tm(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    def slope(g):
        g = g.dropna(subset=["f", "ex"])
        if len(g) < 10: return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        r = stats.linregress(g.f, g.ex)
        return pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr})

    out["by_horizon_side_signed"] = a.groupby(["h", "side"])["sx"].apply(tm).unstack()
    out["by_horizon_slope"] = a.groupby("h").apply(slope)
    a5 = a[a.h == 5].copy()
    out["h5_coin_side"] = a5.groupby(["coin", "side"])["sx"].apply(tm).unstack()
    out["h5_year_side"] = a5.groupby(["year", "side"])["sx"].apply(tm).unstack()
    a5["absq"] = pd.qcut(a5.f.abs(), 4, labels=["q1", "q2", "q3", "q4"])
    out["h5_absq_side"] = a5.groupby(["absq", "side"])["sx"].apply(tm).unstack()
    # agitation: vol30 vs its median within coin (proxy)
    a5["agit"] = np.where(a5.vol30 > a5.groupby("coin").vol30.transform("median"), "agit", "calm")
    out["h5_agit_side"] = a5.groupby(["agit", "side"])["sx"].apply(tm).unstack()
    # raw stretch quartiles
    a5["rawq"] = pd.qcut(a5.raw, 6, duplicates="drop")
    out["h5_rawq_ex"] = a5.groupby("rawq")["ex"].apply(tm).unstack()
    a10 = a[a.h == 10].copy()
    a10["rawq"] = pd.qcut(a10.raw, 6, duplicates="drop")
    out["h10_rawq_ex"] = a10.groupby("rawq")["ex"].apply(tm).unstack()
    return out
