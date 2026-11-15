def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    fc_col = "debug_info.components.sma_cross.last_history_value"
    def samples(h):
        rows = []
        for coin, wins in bars.items():
            for w, df in wins.items():
                df = df.reset_index(drop=True)
                c = df["close"].values
                f = df["forecast"].values
                raw = df[fc_col].values if fc_col in df else np.full(len(df), np.nan)
                ts = pd.to_datetime(df["timestamp"])
                for i in range(0, len(df) - h, h):
                    past = c[i]/c[i-20]-1 if i >= 20 else np.nan
                    rows.append((coin, w, ts.iloc[i].year, f[i], raw[i], c[i+h]/c[i]-1, past))
        s = pd.DataFrame(rows, columns=["coin","w","year","f","raw","r","past20"])
        s["ex"] = s["r"] - s.groupby("coin")["r"].transform("mean")
        return s
    out = {}
    hz = []
    for h in [1,3,5,10,20,40]:
        s = samples(h)
        sl = stats.linregress(s["f"], s["ex"])
        on = s[s.f>0]["ex"]; off = s[s.f==0]["ex"]
        tt = stats.ttest_ind(on, off, equal_var=False)
        hz.append(dict(h=h, n=len(s), slope=sl.slope, t=sl.slope/sl.stderr, on_mean=on.mean(), off_mean=off.mean(), t_onoff=tt.statistic, n_on=len(on)))
    out["by_horizon"] = pd.DataFrame(hz)
    s = samples(10)
    def grp(g):
        on = g[g.f>0]["ex"]; off = g[g.f==0]["ex"]
        sl = stats.linregress(g["f"], g["ex"]) if g["f"].std()>0 else None
        return pd.Series(dict(n=len(g), n_on=len(on), on=on.mean(), off=off.mean(),
                              t=stats.ttest_ind(on,off,equal_var=False).statistic if len(on)>2 and len(off)>2 else np.nan,
                              slope_t=(sl.slope/sl.stderr) if sl is not None else np.nan))
    out["by_coin"] = s.groupby("coin").apply(grp)
    out["by_year"] = s.groupby("year").apply(grp)
    s["fb"] = pd.cut(s["f"], [-0.1,0,2,5,8,12,20.1])
    out["by_fbucket"] = s.groupby("fb")["ex"].agg(["count","mean","std", lambda x: (x>0).mean()])
    s["rawb"] = pd.qcut(s["raw"], 8, duplicates="drop")
    out["by_raw_spread"] = s.groupby("rawb")["ex"].agg(["count","mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    s["pastb"] = pd.qcut(s["past20"], 4)
    out["on_by_past20"] = s[s.f>0].groupby("pastb")["ex"].agg(["count","mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["off_by_past20"] = s[s.f==0].groupby("pastb")["ex"].agg(["count","mean"])
    return out
