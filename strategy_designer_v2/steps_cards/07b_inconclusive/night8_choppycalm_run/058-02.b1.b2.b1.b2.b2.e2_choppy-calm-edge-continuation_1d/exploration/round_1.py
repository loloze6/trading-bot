import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    allgrid = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            hi = b["high"].astype(float).rolling(20).max()
            lo = b["low"].astype(float).rolling(20).min()
            pos = ((c - lo) / (hi - lo) - 0.5) * 2  # -1 bottom, +1 top
            raw = b.get("debug_info.components.range_pos.last_history_value")
            n = len(b)
            for h in (1, 3, 5, 10):
                for i in range(0, n - h, h):
                    allgrid.append((coin, w, h, c[i+h]/c[i]-1, None, None, None, i, b["timestamp"].iloc[i]))
                    if b["regime"].iloc[i] == "unknown" and b["forecast"].iloc[i] != 0:
                        rows.append(dict(coin=coin, w=w, h=h, ret=c[i+h]/c[i]-1, pos=pos.iloc[i],
                                         fc=b["forecast"].iloc[i],
                                         raw=(raw.iloc[i] if raw is not None else np.nan),
                                         day=b["timestamp"].iloc[i], year=pd.Timestamp(b["timestamp"].iloc[i]).year))
    g = pd.DataFrame(allgrid, columns=["coin","w","h","ret","a","b","c","i","day"])
    mean = g.groupby(["coin","h"])["ret"].mean()
    d = pd.DataFrame(rows)
    d["mu"] = [mean.loc[(a,h)] for a,h in zip(d.coin, d.h)]
    d["ex"] = d.ret - d.mu
    d["sgn"] = np.sign(d.fc)
    d["direx"] = d.ex * d.sgn
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out = {}
    def slope(sub, col="fc"):
        sub = sub.dropna(subset=[col,"ex"])
        if len(sub) < 10: return pd.Series({"n":len(sub)})
        r = stats.linregress(sub[col], sub["ex"])
        return pd.Series({"n": len(sub), "slope": r.slope, "t": r.slope/r.stderr})
    out["slope_by_h"] = d.groupby("h").apply(slope)
    out["slope_rawpos_by_h"] = d.groupby("h").apply(lambda s: slope(s, "raw"))
    d5 = d[d.h==5].copy()
    out["direx_by_side_h"] = d.groupby(["h","sgn"])["direx"].apply(tt).unstack()
    d5["q"] = pd.qcut(d5["raw"], 5, labels=False, duplicates="drop")
    out["ex_by_rawpos_q_h5"] = d5.groupby("q").agg(n=("ex","size"), raw=("raw","mean"), ex_pct=("ex", lambda x: 100*x.mean()), t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    d5["fq"] = pd.qcut(d5["fc"].abs(), 4, labels=False, duplicates="drop")
    out["direx_by_absfc_q_h5"] = d5.groupby("fq")["direx"].apply(tt).unstack()
    out["direx_by_window_h5"] = d5.groupby("w")["direx"].apply(tt).unstack()
    out["direx_by_year_h5"] = d5.groupby("year")["direx"].apply(tt).unstack()
    out["direx_by_coin_h5"] = d5.groupby("coin")["direx"].apply(tt).unstack()
    out["agree_fc_rawsign"] = float((np.sign(d5.fc)==np.sign(d5.raw)).mean())
    return out
