def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    fc_vals = []
    rows = []
    allrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            f = b["forecast"].astype(float)
            fc_vals.append(f[f < 0])
            r = c.pct_change()
            vol = r.rolling(20).std()
            hi = c.shift(1).rolling(20).max()
            bo = c > hi
            # failed breakout: breakout 1..3 bars ago, close back below that bar's old high
            fail = pd.Series(False, index=c.index); depth = pd.Series(np.nan, index=c.index)
            for k in (1, 2, 3):
                oh = hi.shift(k)
                m = bo.shift(k).fillna(False).astype(bool) & (c < oh)
                d = (oh - c) / c / vol
                depth = depth.where(~(m & depth.isna()), d)
                fail |= m
            fwd = c.shift(-5) / c - 1
            ret20 = c / c.shift(20) - 1
            ret60 = c / c.shift(60) - 1
            n = len(c)
            for i in range(0, n - 5, 5):
                # first failed-breakout bar in grid cell
                cell = range(i, min(i + 5, n - 5))
                j = next((t for t in cell if fail.iloc[t]), None)
                allrows.append(dict(coin=coin, fwd=fwd.iloc[i], vol=vol.iloc[i], ret20=ret20.iloc[i], ret60=ret60.iloc[i]))
                if j is not None and not np.isnan(fwd.iloc[j]):
                    rows.append(dict(coin=coin, w=w, fwd=fwd.iloc[j], vol=vol.iloc[j], depth=depth.iloc[j],
                                     ret20=ret20.iloc[j], ret60=ret60.iloc[j], fc=f.iloc[j],
                                     year=pd.Timestamp(b["timestamp"].iloc[j]).year))
    fc = pd.concat(fc_vals)
    out["forecast_neg_describe"] = fc.describe()
    out["share_forecast_eq_-20"] = float((fc <= -19.99).mean())
    A = pd.DataFrame(allrows); D = pd.DataFrame(rows)
    drift = A.groupby("coin")["fwd"].mean()
    D["unus"] = -(D["fwd"] - D["coin"].map(drift))
    D["tot"] = -D["fwd"]
    def summ(g):
        x = g["unus"].dropna()
        return pd.Series(dict(n=len(x), mean_unus=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, mean_tot=g["tot"].mean()))
    out["all_cases"] = summ(D)
    out["by_coin"] = D.groupby("coin").apply(summ)
    out["by_year"] = D.groupby("year").apply(summ)
    for col in ["vol", "depth", "ret20", "ret60"]:
        q = pd.qcut(D[col], 4, labels=False, duplicates="drop")
        out["by_q_" + col] = D.groupby(q).apply(summ)
    # baseline: non-case all grid bars by ret60 quartile (unusual short-move)
    A["unus"] = -(A["fwd"] - A["coin"].map(drift)); A["tot"] = -A["fwd"]
    out["baseline_by_q_ret60"] = A.groupby(pd.qcut(A["ret60"], 4, labels=False)).apply(summ)
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d[["book_return", "coin_return"]].copy(); x["w"] = w; x["year"] = pd.to_datetime(d["day"]).dt.year
            dd.append(x)
    dd = pd.concat(dd)
    out["book_by_year"] = dd.groupby("year")[["book_return", "coin_return"]].mean()
    T = pd.concat([t for wins in data["trades"].values() for t in wins.values()])
    out["trades"] = pd.Series(dict(n=len(T), mean_gross=T["profit_loss_percent"].mean(), mean_net=T["net_profit_loss_percent"].mean(),
                                  win=(T["profit_loss_percent"] > 0).mean(), mean_days=T["duration_minutes"].mean()/1440))
    return out
