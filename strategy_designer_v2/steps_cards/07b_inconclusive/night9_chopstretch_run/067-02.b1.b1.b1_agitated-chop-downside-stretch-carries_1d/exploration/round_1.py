def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for H in [1, 3, 5, 10]:
            allr = []
            for w, df in wins.items():
                c = df["close"].reset_index(drop=True)
                idx = np.arange(0, len(c) - H, H)
                allr.extend((c.values[idx + H] / c.values[idx] - 1).tolist())
            drift[(coin, H)] = np.mean(allr)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r = c.pct_change()
            sma = c.rolling(20).mean()
            sd = r.rolling(20).std()
            st = (c / sma - 1) / sd
            ts = pd.to_datetime(df["timestamp"])
            for H in [1, 3, 5, 10]:
                idx = np.arange(0, len(c) - H, H)
                fwd = c.values[idx + H] / c.values[idx] - 1
                for k, i in enumerate(idx):
                    rows.append(dict(coin=coin, w=w, H=H, year=ts.iloc[i].year,
                                     day=ts.iloc[i].normalize(), reg=df["regime"].iloc[i],
                                     st=st.iloc[i], fwd=fwd[k], ex=fwd[k] - drift[(coin, H)]))
    d = pd.DataFrame(rows).dropna(subset=["st"])
    d["inprof"] = d["reg"] == "unknown"
    def summ(g):
        x = g["ex"]; 
        n = len(x)
        t = x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan
        rho = stats.spearmanr(g["st"], g["fwd"])[0] if n > 5 else np.nan
        return pd.Series(dict(n=n, mean_ex=x.mean(), t=t, mean_fwd=g["fwd"].mean(), spearman_st_fwd=rho))
    d["side"] = np.where(d["st"] < 0, "below", "above")
    out = {}
    out["by_H_profile_side"] = d.groupby(["H", "inprof", "side"]).apply(summ)
    d5 = d[(d.H == 5) & d.inprof]
    out["in_prof_H5_by_coin_side"] = d5.groupby(["coin", "side"]).apply(summ)
    out["in_prof_H5_by_year_side"] = d5.groupby(["year", "side"]).apply(summ)
    d5b = d5[d5.side == "below"].copy()
    d5b["q"] = pd.qcut(d5b["st"], 3, labels=["deep", "mid", "shallow"])
    out["in_prof_H5_below_terciles"] = d5b.groupby("q").apply(summ)
    dall = d[(d.H == 5)].copy()
    dall["q"] = pd.qcut(dall["st"], 5, labels=False)
    out["all_bars_H5_by_stretch_quintile_inprof"] = dall.groupby(["inprof", "q"]).apply(summ)
    out["regime_counts"] = d[d.H == 1]["reg"].value_counts()
    return out
