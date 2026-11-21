def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}; sd = {}
    for coin, ws in bars.items():
        rets = []
        for w, b in ws.items():
            c = b["close"].values
            for i in range(0, len(c) - 26, 26):
                rets.append(c[i + 26] / c[i] - 1)
        drift[coin] = np.mean(rets); sd[coin] = np.std(rets)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            for i in range(0, n - 26, 26):
                if b.loc[i, "regime"] == "trending" and b.loc[i, "forecast"] < 0:
                    r = c[i + 26] / c[i] - 1
                    p26 = c[i] / c[i - 26] - 1 if i >= 26 else np.nan
                    r13 = c[i + 13] / c[i] - 1
                    rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b.loc[i, "timestamp"]).year,
                                     ex=-(r - drift[coin]), ex13=-(r13 - drift[coin] / 2),
                                     raw=b.loc[i, "debug_info.components.slow_fall.last_history_value"],
                                     past26=p26, strength=-(r - drift[coin]) / sd[coin]))
    d = pd.DataFrame(rows)
    med = d.raw.median()
    d["half"] = np.where(d.raw > med, "slow", "fast")
    def summ(g):
        k = len(g)
        return pd.Series(dict(n=k, mean_ex=g.ex.mean(),
                              t=g.ex.mean() / (g.ex.std(ddof=1) / np.sqrt(k)) if k > 2 else np.nan,
                              mean_ex13=g.ex13.mean(), strength=g.strength.mean()))
    out = {}
    out["half"] = d.groupby("half").apply(summ)
    out["half_by_year"] = d.groupby(["year", "half"]).apply(summ)
    out["half_by_coin"] = d.groupby(["coin", "half"]).apply(summ)
    sl = stats.linregress(np.log(d.raw), d.ex)
    out["reg_ex_on_lograw"] = pd.Series(dict(slope=sl.slope, t=sl.slope / sl.stderr, n=len(d)))
    dd = d.dropna(subset=["past26"])
    out["corr_raw_past26"] = stats.spearmanr(dd.raw, dd.past26)[0]
    dd = dd.copy()
    dd["q_past"] = pd.qcut(dd.past26.rank(method="first"), 3, labels=["deep_fall", "mid", "mild"])
    out["by_past26_tercile"] = dd.groupby("q_past").apply(summ)
    sl2 = stats.linregress(dd.past26, dd.ex)
    out["reg_ex_on_past26"] = pd.Series(dict(slope=sl2.slope, t=sl2.slope / sl2.stderr, n=len(dd)))
    return out
