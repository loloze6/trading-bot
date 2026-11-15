import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            raw = df.get("debug_info.components.sma_cross.last_history_value", pd.Series(np.nan, index=df.index)).values
            n = len(df)
            # bars since raw sign change
            sgn = np.sign(raw)
            since = np.full(n, np.nan); cnt = np.nan
            for i in range(n):
                if i > 0 and not np.isnan(sgn[i]) and sgn[i] == sgn[i-1]:
                    cnt = cnt + 1
                else:
                    cnt = 0 if i > 0 else np.nan
                since[i] = cnt
            for h in [5, 10, 20, 40]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, f=f[i], raw=raw[i], since=since[i],
                                     ret=c[i+h]/c[i]-1, year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby(["coin","h"])["ret"].transform("mean")
    out = {}
    # by horizon: slope t and on/off diff
    hz = []
    for h, g in d.groupby("h"):
        g = g.dropna(subset=["f"])
        s = stats.linregress(g["f"], g["ex"])
        on, off = g[g.f>0]["ex"], g[g.f==0]["ex"]
        hz.append(dict(h=h, n=len(g), slope=s.slope, t=s.slope/s.stderr, on_mean=on.mean(), off_mean=off.mean(),
                       t_on_off=stats.ttest_ind(on, off, equal_var=False).statistic,
                       raw_pos_off=((g.raw>0)&(g.f==0)).mean(), raw_neg_on=((g.raw<0)&(g.f>0)).mean()))
    out["by_horizon"] = pd.DataFrame(hz)
    g10 = d[d.h==10].dropna(subset=["f"]).copy()
    g10["fbin"] = pd.cut(g10["f"], [-0.1, 0, 5, 10, 15, 20.1])
    out["fbin_10"] = g10.groupby("fbin")["ex"].agg(["count","mean","std"])
    g10["rawbin"] = pd.qcut(g10["raw"], 6, duplicates="drop")
    out["rawbin_10"] = g10.groupby("rawbin")["ex"].agg(["count","mean"])
    def ct(g):
        on, off = g[g.f>0]["ex"], g[g.f==0]["ex"]
        return pd.Series(dict(n_on=len(on), on=on.mean(), off=off.mean(),
                              t=stats.ttest_ind(on, off, equal_var=False).statistic if len(on)>2 and len(off)>2 else np.nan))
    out["coin_10"] = g10.groupby("coin").apply(ct)
    out["year_10"] = g10.groupby("year").apply(ct)
    g10["sbin"] = pd.cut(g10["since"], [-1, 20, 60, 150, 400, 5000])
    out["since_raw_pos_10"] = g10[g10.raw>0].groupby("sbin")["ex"].agg(["count","mean","std"])
    out["since_raw_neg_10"] = g10[g10.raw<0].groupby("sbin")["ex"].agg(["count","mean","std"])
    return out
