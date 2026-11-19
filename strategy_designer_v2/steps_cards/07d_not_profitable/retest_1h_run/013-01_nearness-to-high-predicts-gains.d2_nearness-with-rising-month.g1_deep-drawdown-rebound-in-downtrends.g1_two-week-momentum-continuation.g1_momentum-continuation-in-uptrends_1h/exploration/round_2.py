def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; coins = list(bars.keys())
    wins = sorted({w for c in coins for w in bars[c].keys()}, key=lambda s: int(s[1:]))
    recs = []
    for c in coins:
        for w, b in bars[c].items():
            cl = b["close"].values.astype(float); n = len(cl)
            al = b["postRebalance_current_allocation"].values.astype(float)
            hr = np.r_[np.diff(cl)/cl[:-1], np.nan]
            lr = np.r_[np.nan, np.diff(np.log(cl))]
            vol7 = pd.Series(lr).rolling(168).std().values
            vol60 = pd.Series(lr).rolling(1440).std().values
            r60 = pd.Series(cl).pct_change(1440).values
            r14 = pd.Series(cl).pct_change(336).values
            r3 = pd.Series(cl).pct_change(72).values
            hi = pd.Series(b["high"].values).rolling(336).max().values
            day = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            recs.append(pd.DataFrame(dict(coin=c, win=w, day=day, gain=al*hr, alloc=al,
                r60=r60, r14=r14, r3=r3, vr=vol7/vol60, vol=vol7, dist=cl/hi-1)))
    h = pd.concat(recs, ignore_index=True).dropna(subset=["gain"])
    h["widx"] = h.win.str[1:].astype(int)
    act = h[h.alloc.abs() > 1e-6]
    def calmar(hh, mask=None):
        g = hh.gain.where(mask, 0.0) if mask is not None else hh.gain
        x = hh.assign(g=g)
        cd = x.groupby(["widx","coin","day"]).g.apply(lambda z: (1+z).prod()-1)
        d = cd.groupby(level=[0,2]).mean().sort_index()
        v = (1+d).cumprod(); dd = (v/v.cummax()-1).min()
        yr = v.iloc[-1]**(365/len(d))-1
        return pd.Series({"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),"sharpe":d.mean()/d.std()*np.sqrt(365)})
    out["base_nofee"] = calmar(h)
    q = act[["r60","vr","vol","r3","dist"]].quantile([.6,.8])
    out["quantiles_active"] = q
    out["cut_r60_top20"] = calmar(h, ~(h.r60 > q.loc[.8,"r60"]))
    out["cut_r60_top40"] = calmar(h, ~(h.r60 > q.loc[.6,"r60"]))
    out["cut_vr_top20"] = calmar(h, ~(h.vr > q.loc[.8,"vr"]))
    out["cut_vol_top20"] = calmar(h, ~(h.vol > q.loc[.8,"vol"]))
    out["cut_r3_bottom20"] = calmar(h, ~(h.r3 < act.r3.quantile(.2)))
    # hourly gain of active bars by bucket, with t (hourly, many)
    def tab(col):
        x = act.dropna(subset=[col]).copy()
        x["b"] = pd.qcut(x[col], 5, labels=False, duplicates="drop")
        return x.groupby("b").agg(lo=(col,"min"), hi=(col,"max"), n=("gain","size"),
            mean_bp=("gain", lambda z: z.mean()*1e4), sd_bp=("gain", lambda z: z.std()*1e4),
            alloc=("alloc","mean"))
    for col in ["r60","vr","r3"]:
        out["hourly_by_"+col] = tab(col)
    # deepest fall w8-w10: contributions by coin and states
    f = h[(h.widx>=8)&(h.widx<=10)]
    out["fall_w8_10_by_coin"] = f.groupby("coin").agg(sumgain=("gain","sum"), alloc=("alloc","mean"),
        r60=("r60","median"), vr=("vr","median"))
    return out
