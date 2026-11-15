def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    dc = "debug_info.components.below_ma.last_history_value"
    # coin mean daily return pooled over windows
    mdr = {}
    for c in bars:
        rs = []
        for w, df in bars[c].items():
            rs.append(df["close"].pct_change().dropna())
        mdr[c] = pd.concat(rs).mean()
    rows = []
    for h in [1, 3, 5, 10, 20, 40]:
        for c in bars:
            for w, df in bars[c].items():
                df = df.reset_index(drop=True)
                cl = df["close"].values
                n = len(df)
                # 20d past return and sma200 slope proxy (distance change over 20 bars)
                for i in range(0, n - h, h):
                    d = df[dc].iloc[i] if dc in df else np.nan
                    a = df["postRebalance_current_allocation"].iloc[i]
                    f = df["forecast"].iloc[i]
                    r = cl[i + h] / cl[i] - 1
                    ex = r - h * mdr[c]
                    p20 = cl[i] / cl[i - 20] - 1 if i >= 20 else np.nan
                    dd20 = d - df[dc].iloc[i - 20] if (i >= 20 and dc in df) else np.nan
                    rows.append(dict(h=h, coin=c, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                     d=d, a=a, f=f, ex=ex, prod=a * ex, p20=p20, dd20=dd20))
    R = pd.DataFrame(rows)
    out = {}
    def tt(s):
        s = s.dropna()
        return pd.Series(dict(n=len(s), mean=s.mean(), t=s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan))
    act = R[R.f < 0]
    # by horizon: excess return of coin while below (negative = fall), and prod
    out["by_h_below_ex"] = act.groupby("h")["ex"].apply(tt).unstack()
    out["by_h_above_ex"] = R[(R.f == 0) & (R.d > 0)].groupby("h")["ex"].apply(tt).unstack()
    a10 = act[act.h == 10]
    out["h10_by_coin"] = a10.groupby("coin")["prod"].apply(tt).unstack()
    out["h10_by_year"] = a10.groupby("year")["prod"].apply(tt).unstack()
    a10 = a10.copy()
    a10["dq"] = pd.qcut(a10["d"], 4, labels=False)
    out["h10_by_depth_q_ex"] = a10.groupby("dq").agg(dmean=("d", "mean"), n=("ex", "size"), ex=("ex", "mean"))
    a10["p20s"] = np.sign(a10["p20"])
    out["h10_by_p20sign_ex"] = a10.groupby("p20s")["ex"].apply(tt).unstack()
    a10["dds"] = np.sign(a10["dd20"])
    out["h10_by_dd20sign_ex"] = a10.groupby("dds")["ex"].apply(tt).unstack()
    a20 = act[act.h == 20].copy()
    a20["p20s"] = np.sign(a20["p20"])
    out["h20_by_p20sign_ex"] = a20.groupby("p20s")["ex"].apply(tt).unstack()
    a5 = act[act.h == 5].copy()
    a5["p20s"] = np.sign(a5["p20"])
    out["h5_by_p20sign_ex"] = a5.groupby("p20s")["ex"].apply(tt).unstack()
    return out
