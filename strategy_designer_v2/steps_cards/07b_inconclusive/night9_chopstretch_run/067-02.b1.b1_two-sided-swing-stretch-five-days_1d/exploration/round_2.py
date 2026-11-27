import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c); f = df["forecast"].values
            raw = df["debug_info.components.stretch.last_history_value"].values
            lr = np.r_[np.nan, np.diff(np.log(c))]
            vol30 = pd.Series(lr).rolling(30).std().values
            vol90 = pd.Series(lr).rolling(90, min_periods=60).median().values
            ts = pd.to_datetime(df["timestamp"])
            h = 5
            for i in range(0, n - h, h):
                rows.append(dict(coin=coin, win=w, i=i, f=f[i], raw=raw[i], ret=c[i+h]/c[i]-1,
                                 vol30=vol30[i], ret10=(c[i]/c[i-10]-1) if i >= 10 else np.nan,
                                 year=ts[i].year, day=ts[i].normalize()))
    d = pd.DataFrame(rows)
    d["mu"] = d.groupby("coin")["ret"].transform("mean")
    d["ex"] = d.ret - d.mu
    a = d[d.f != 0].copy()
    a["side"] = np.where(a.f > 0, "long", "short")
    a["sx"] = np.sign(a.f) * a.ex
    a["agit"] = np.where(a.vol30 > a.groupby("coin").vol30.transform("median"), "agit", "calm")
    out = {}
    def tm(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    def slope(g, col="f"):
        g = g.dropna(subset=[col, "ex"])
        if len(g) < 10: return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        r = stats.linregress(g[col], g.ex)
        return pd.Series({"n": len(g), "slope": r.slope, "t": r.slope/r.stderr})
    s = a[a.side == "short"]
    out["short_slope_by_agit"] = s.groupby("agit").apply(slope)
    out["long_slope_by_agit"] = a[a.side == "long"].groupby("agit").apply(slope)
    out["slope_by_agit_all"] = a.groupby("agit").apply(slope)
    s2 = s.copy(); s2["q"] = pd.qcut(s2.raw, 3, labels=["deep", "mid", "shallow"])
    out["short_rawtercile_agit"] = s2.groupby(["agit", "q"])["sx"].apply(tm).unstack()
    out["short_agit_year"] = s[s.agit == "agit"].groupby("year")["sx"].apply(tm).unstack()
    out["short_agit_coin"] = s[s.agit == "agit"].groupby("coin")["sx"].apply(tm).unstack()
    out["short_agit_raw_ret_total"] = s[s.agit == "agit"].assign(tot=-s.ret)["tot"].pipe(tm)
    out["short_side_window_t"] = s.groupby("win")["sx"].apply(tm).unstack()
    return out
