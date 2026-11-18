import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [3,5,10,20]
    rows = []
    coinmean = {}
    for c, wins in bars.items():
        for h in H:
            r = []
            for w, df in wins.items():
                cl = df["close"].values
                idx = np.arange(0, len(cl)-h, h)
                r += list(cl[idx+h]/cl[idx]-1)
            coinmean[(c,h)] = np.nanmean(r)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; hi = df["high"].values; lo = df["low"].values
            n = len(df)
            fc = df.get("debug_info.components.width.post_pipeline_value")
            raw = df.get("debug_info.components.width.last_history_value")
            trend = (df["regime"] == "trending").values
            last = -999
            for t in range(n):
                if not trend[t] or t - last < 10: continue
                if t + 10 >= n: continue
                last = t
                ph = hi[max(0,t-20):t].max() if t>0 else np.nan
                pl = lo[max(0,t-20):t].min() if t>0 else np.nan
                d = dict(coin=c, win=w, year=pd.Timestamp(df["timestamp"].iloc[t]).year,
                         fc=fc.iloc[t] if fc is not None else np.nan,
                         raw=raw.iloc[t] if raw is not None else np.nan,
                         brk=(cl[t]/ph-1) if t>0 else np.nan,
                         vol=df["volume"].iloc[t]/df["volume"].iloc[max(0,t-20):t].mean() if t>0 else np.nan)
                for h in H:
                    d[f"x{h}"] = cl[t+h]/cl[t]-1-coinmean[(c,h)] if t+h < n else np.nan
                rows.append(d)
    s = pd.DataFrame(rows)
    def slope(df, x, y):
        d = df[[x,y]].dropna()
        if len(d) < 8: return (len(d), np.nan, np.nan)
        r = stats.linregress(d[x], d[y])
        return (len(d), r.slope, r.slope/r.stderr)
    out = {}
    hz = []
    for h in H:
        n, b, t = slope(s, "fc", f"x{h}")
        n2, b2, t2 = slope(s, "raw", f"x{h}")
        n3, b3, t3 = slope(s, "brk", f"x{h}")
        n4, b4, t4 = slope(s, "vol", f"x{h}")
        m = s[f"x{h}"].dropna()
        hz.append(dict(h=h, n=n, t_fc=t, t_raw=t2, t_brk=t3, t_volratio=t4,
                       mean_excess=m.mean(), t_mean=m.mean()/(m.std()/np.sqrt(len(m)))))
    out["by_horizon"] = pd.DataFrame(hz)
    g = []
    for c, d in s.groupby("coin"):
        n, b, t = slope(d, "fc", "x10"); m = d["x10"].dropna()
        g.append(dict(coin=c, n=n, slope=b, t=t, mean_x10=m.mean(), t_mean=m.mean()/(m.std()/np.sqrt(len(m)))))
    out["by_coin"] = pd.DataFrame(g)
    g = []
    for c, d in s.groupby("year"):
        n, b, t = slope(d, "fc", "x10"); m = d["x10"].dropna()
        g.append(dict(year=c, n=n, slope=b, t=t, mean_x10=m.mean()))
    out["by_year"] = pd.DataFrame(g)
    s["q"] = pd.qcut(s["fc"], 5, labels=False, duplicates="drop")
    out["fc_quintiles"] = s.groupby("q").agg(n=("x10","count"), fc=("fc","mean"), raw=("raw","mean"),
                                            x10=("x10","mean"), x20=("x20","mean"), x5=("x5","mean"))
    s["bq"] = pd.qcut(s["brk"], 5, labels=False, duplicates="drop")
    out["brk_quintiles"] = s.groupby("bq").agg(n=("x10","count"), brk=("brk","mean"), x5=("x5","mean"),
                                              x10=("x10","mean"), x20=("x20","mean"))
    out["corr_fc_raw"] = float(s[["fc","raw"]].corr().iloc[0,1])
    return out
