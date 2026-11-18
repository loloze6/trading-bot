import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [10, 20]
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
            cl = df["close"].values; vol = df["volume"].values
            n = len(df)
            fc = df.get("debug_info.components.width.post_pipeline_value")
            trend = (df["regime"] == "trending").values
            last = -999
            for t in range(n):
                if not trend[t] or t - last < 10: continue
                if t + 10 >= n: continue
                last = t
                d = dict(coin=c, win=w, fc=fc.iloc[t] if fc is not None else np.nan,
                         r60=cl[t]/cl[t-60]-1 if t >= 60 else np.nan,
                         r20=cl[t]/cl[t-20]-1 if t >= 20 else np.nan,
                         vr=vol[max(0,t-5):t].mean()/vol[max(0,t-60):t].mean() if t >= 20 else np.nan)
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
    g = []
    for name, cond in [("r60>0", s.r60 > 0), ("r60<=0", s.r60 <= 0),
                       ("vr_high", s.vr > s.vr.median()), ("vr_low", s.vr <= s.vr.median()),
                       ("r20_high", s.r20 > s.r20.median()), ("r20_low", s.r20 <= s.r20.median())]:
        d = s[cond]
        for h in H:
            n, b, t = slope(d, "fc", f"x{h}")
            m = d[f"x{h}"].dropna()
            g.append(dict(split=name, h=h, n=n, slope=b, t=t, mean=m.mean(),
                          t_mean=m.mean()/(m.std()/np.sqrt(len(m)))))
    out["splits"] = pd.DataFrame(g)
    out["n_by_window_mean"] = float(s.groupby(["coin","win"]).size().mean())
    sd = s["x10"].std()
    out["x10_sd"] = float(sd)
    out["fc_sd"] = float(s["fc"].std())
    return out
