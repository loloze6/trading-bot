def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    h = 10
    rows = []
    bars = data["bars"]
    # BTC 200-day trend per window for market context
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            dep = df.get("debug_info.components.depth.last_history_value")
            r1 = pd.Series(c).pct_change()
            vol20 = r1.rolling(20).std().values
            ret5 = pd.Series(c).pct_change(5).values
            ret20 = pd.Series(c).pct_change(20).values
            for i in range(0, n - h, h):
                rows.append(dict(coin=coin, w=w, i=i, fc=df["forecast"].iloc[i],
                                 reg=df["regime"].iloc[i],
                                 depth=(dep.iloc[i] if dep is not None else np.nan),
                                 fwd=c[i + h] / c[i] - 1, vol20=vol20[i],
                                 ret5=ret5[i], ret20=ret20[i],
                                 year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                 ts=df["timestamp"].iloc[i]))
    R = pd.DataFrame(rows)
    R["ex"] = R["fwd"] - R.groupby("coin")["fwd"].transform("mean")
    # market (BTC) forward return at same timestamp
    btc = R[R.coin == "BTCUSD"][["ts", "fwd"]].rename(columns={"fwd": "btcfwd"})
    R = R.merge(btc, on="ts", how="left")
    R["exbtc"] = R["fwd"] - R["btcfwd"]
    def summ(g, col="ex"):
        x = g[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), med=x.median(),
                              hit=(x > 0).mean(),
                              t=(x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan)))
    top = R[R.fc >= 10]
    act = R[R.fc > 0]
    out = {}
    out["all_top"] = summ(top).to_frame().T
    out["top_by_coin"] = top.groupby("coin").apply(summ)
    out["top_by_year"] = top.groupby("year").apply(summ)
    out["top_by_window"] = top.groupby("w").apply(summ)
    R["fb"] = pd.cut(R.fc, [-0.1, 0, 2, 5, 10, 15, 20.1])
    out["inreg_buckets"] = R[R.reg == "mean_reversion"].groupby("fb").apply(summ)
    out["top_vs_btc"] = summ(top[top.coin != "BTCUSD"], "exbtc").to_frame().T
    out["top_by_ret5_sign"] = top.groupby(top.ret5 > 0).apply(summ)
    out["top_by_ret20_q"] = top.groupby(pd.qcut(top.ret20, 3, duplicates="drop")).apply(summ)
    out["top_by_vol_q"] = top.groupby(pd.qcut(top.vol20, 3, duplicates="drop")).apply(summ)
    out["top_by_btcfwd_sign"] = top.groupby(top.btcfwd > 0).apply(summ)
    out["top_std_vs_all"] = pd.Series(dict(top_std=top.fwd.std(), all_std=R.fwd.std(),
                                           act_std=act.fwd.std()))
    out["top_n_distinct_ts"] = top.ts.nunique()
    out["top_by_depth_q"] = top.groupby(pd.qcut(top.depth, 3, duplicates="drop")).apply(summ)
    return out
