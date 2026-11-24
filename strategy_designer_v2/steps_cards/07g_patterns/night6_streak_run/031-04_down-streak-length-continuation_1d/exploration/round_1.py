def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]
            # signed streak
            st = np.zeros(n)
            for i in range(1, n):
                if r[i] > 0:
                    st[i] = st[i-1] + 1 if st[i-1] > 0 else 1
                elif r[i] < 0:
                    st[i] = st[i-1] - 1 if st[i-1] < 0 else -1
                else:
                    st[i] = 0
            rs = pd.Series(r)
            vol20 = rs.rolling(20).std().values
            ret5 = pd.Series(c).pct_change(5).values
            ret20 = pd.Series(c).pct_change(20).values
            hi20 = pd.Series(c).rolling(20).max().values
            lo20 = pd.Series(c).rolling(20).min().values
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, day=ts.iloc[i].floor("D"),
                                 wd=ts.iloc[i].dayofweek, yr=ts.iloc[i].year,
                                 fwd=c[i+H]/c[i]-1, st=st[i], r1=r[i], r5=ret5[i],
                                 r20=ret20[i], vol=vol20[i],
                                 pos20=(c[i]-lo20[i])/(hi20[i]-lo20[i]) if hi20[i] > lo20[i] else np.nan,
                                 fc=b["forecast"].iloc[i]))
    d = pd.DataFrame(rows)
    g = d.groupby("coin")["fwd"]
    d["drift"] = g.transform("mean"); d["usd"] = g.transform("std")
    d["u"] = (d["fwd"] - d["drift"])
    d["s"] = d["u"] / d["usd"]
    for col in ["r1", "r5", "r20", "vol", "pos20"]:
        d[col + "_q"] = d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False) if x.notna().sum() > 10 else np.nan)

    def summ(key):
        out = []
        for k, sub in d.dropna(subset=[key, "u"]).groupby(key):
            m = sub["u"].mean()
            dev = (sub["u"] - m).groupby(sub["day"]).sum()
            se = np.sqrt((dev**2).sum()) / len(sub)
            out.append(dict(k=k, n=len(sub), days=sub["day"].nunique(),
                            mean_u=round(m, 5), strength=round(sub["s"].mean(), 4), t=round(m/se, 2)))
        return pd.DataFrame(out)
    d["stc"] = d["st"].clip(-5, 5)
    res = {}
    res["drift_by_coin"] = d.groupby("coin")["fwd"].agg(["mean", "std", "count"]).round(4)
    res["by_streak"] = summ("stc")
    res["by_r1_q"] = summ("r1_q")
    res["by_r5_q"] = summ("r5_q")
    res["by_r20_q"] = summ("r20_q")
    res["by_vol_q"] = summ("vol_q")
    res["by_pos20_q"] = summ("pos20_q")
    res["by_weekday"] = summ("wd")
    res["by_year"] = summ("yr")
    # streak within vol regime: down streak >=3 vs others, per vol tercile
    d["longdown"] = (d["st"] <= -3).astype(int)
    d["vt"] = d["vol_q"].map({0: 0, 1: 0, 2: 1, 3: 2, 4: 2})
    d["vt_ld"] = d["vt"].astype(str) + "_" + d["longdown"].astype(str)
    res["vol_x_longdown"] = summ("vt_ld")
    # book
    days = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["w"] = w; days.append(x)
    D = pd.concat(days)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    res["book_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].mean().round(5)
    res["book_by_wd"] = D.groupby("wd")[["book_return", "coin_return"]].mean().round(5)
    return res
