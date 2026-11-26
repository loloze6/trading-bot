def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    allret = {}
    for coin, ws in data["bars"].items():
        rs = []
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            rs.append(r.dropna())
            nxt = c.shift(-1) / c - 1
            sd = r.rolling(30).std()
            rng = (b["high"] - b["low"]) / c
            width = rng / sd
            low = (b["high"] - c) / (b["high"] - b["low"])
            for i in range(len(b) - 1):
                if b["forecast"].iloc[i] > 0:
                    rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                     day=str(pd.Timestamp(b["timestamp"].iloc[i]).date()),
                                     fc=b["forecast"].iloc[i], nxt=nxt.iloc[i], width=width.iloc[i],
                                     low=low.iloc[i], dayret=r.iloc[i]))
        allret[coin] = pd.concat(rs).mean()
    d = pd.DataFrame(rows)
    d["ex"] = d["nxt"] - d["coin"].map(allret)
    d["prod"] = d["width"] * d["low"]
    out = {}
    out["n_cases"] = len(d)
    out["fc_describe"] = d["fc"].describe()
    out["fc_nunique"] = d["fc"].nunique()
    def summ(g):
        return pd.Series(dict(n=len(g), mean=g["ex"].mean(), t=g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 1 else np.nan, hit=(g["ex"] > 0).mean()))
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    out["by_window"] = d.groupby("w").apply(summ)
    d["wq"] = pd.qcut(d["width"], 3, labels=["w_lo", "w_mid", "w_hi"])
    d["pq"] = pd.qcut(d["prod"], 3, labels=["p_lo", "p_mid", "p_hi"])
    d["dq"] = pd.qcut(d["dayret"], 3, labels=["fall_big", "fall_mid", "fall_small"])
    out["by_width_tercile"] = d.groupby("wq").apply(summ)
    out["by_prod_tercile"] = d.groupby("pq").apply(summ)
    out["by_dayret_tercile"] = d.groupby("dq").apply(summ)
    out["corr_ex"] = pd.Series(dict(width=stats.spearmanr(d["width"], d["ex"], nan_policy="omit")[0],
                                    prod=stats.spearmanr(d["prod"], d["ex"], nan_policy="omit")[0],
                                    fc=stats.spearmanr(d["fc"], d["ex"], nan_policy="omit")[0],
                                    dayret=stats.spearmanr(d["dayret"], d["ex"], nan_policy="omit")[0]))
    out["overall"] = summ(d)
    out["median_trim"] = pd.Series(dict(median=d["ex"].median(), mean_ex_top5=d["ex"].clip(upper=d["ex"].quantile(0.95)).mean()))
    return out
