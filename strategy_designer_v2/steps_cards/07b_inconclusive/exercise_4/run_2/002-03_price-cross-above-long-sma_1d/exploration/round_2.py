def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    mu = {}
    for c, ws in bars.items():
        mu[c] = pd.concat([df["close"].pct_change().dropna() for df in ws.values()]).mean()
    H = 20
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            raw = df["debug_info.components.above_ma.last_history_value"].values
            sma = cl / (1 + raw / 100.0)
            above = raw > 0
            # age since close went above sma (bars), inside window
            age = np.full(len(df), np.nan); a = np.nan
            for i in range(len(df)):
                if np.isnan(raw[i]): a = np.nan
                elif above[i]:
                    a = (0 if (i == 0 or np.isnan(raw[i-1]) or not above[i-1]) and i > 0 and not np.isnan(raw[i-1]) else (a + 1 if not np.isnan(a) else np.nan))
                else: a = np.nan
                age[i] = a
            slope = pd.Series(sma).pct_change(20).values
            r20 = pd.Series(cl).pct_change(20).values
            vol = pd.Series(cl).pct_change().rolling(30).std().values
            for i in range(0, len(df) - H, H):
                rows.append(dict(coin=c, w=w, f=df["forecast"].iloc[i], raw=raw[i], age=age[i], slope=slope[i],
                                 r20=r20[i], vol=vol[i], alloc=df["postRebalance_current_allocation"].iloc[i],
                                 ex=cl[i+H]/cl[i]-1-H*mu[c]))
    g = pd.DataFrame(rows)
    def tt(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), med=x.median(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, hit=(x>0).mean()))
    out = {}
    pos = g[g.f > 0].copy()
    out["pos_skew_and_trim"] = pd.Series(dict(skew=stats.skew(pos.ex), mean=pos.ex.mean(),
        trim10=stats.trim_mean(pos.ex, 0.1), top5share=pos.ex.nlargest(5).sum()/pos.ex.sum()))
    pos["agebin"] = pd.cut(pos.age, [-1, 20, 60, 150, 10000], labels=["<=20d", "21-60d", "61-150d", ">150d"])
    out["pos_by_age"] = pos.groupby("agebin")["ex"].apply(tt).unstack()
    g["slopeq"] = pd.qcut(g.slope.rank(method="first"), 4, labels=["s1", "s2", "s3", "s4"])
    out["all_by_smaslope"] = g.groupby(["slopeq", g.f > 0])["ex"].apply(tt).unstack()
    out["pos_slope_sign"] = pos.groupby(pos.slope > 0)["ex"].apply(tt).unstack()
    pos["volq"] = pd.qcut(pos.vol.rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["pos_by_vol"] = pos.groupby("volq")["ex"].apply(tt).unstack()
    out["pos_by_r20sign"] = pos.groupby(pos.r20 > 0)["ex"].apply(tt).unstack()
    # book decomposition
    br = []
    for c, ws in bars.items():
        for w, df in ws.items():
            d = df[["timestamp", "close", "postRebalance_current_allocation"]].copy()
            d["day"] = pd.to_datetime(d.timestamp).dt.floor("D")
            d["nr"] = d.close.shift(-1)/d.close - 1
            d["gain"] = d.postRebalance_current_allocation * d.nr
            d["mkt"] = d.postRebalance_current_allocation * mu[c]
            br.append(d.dropna(subset=["nr"]))
    b = pd.concat(br)
    out["book_mkt_vs_timing"] = pd.Series(dict(mean_gain=b.gain.mean(), from_market=b.mkt.mean(), timing=b.gain.mean()-b.mkt.mean(), mean_alloc=b.postRebalance_current_allocation.mean()))
    return out
