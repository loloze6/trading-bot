def explore(data):
    import numpy as np, pandas as pd
    h = 10
    rows = []
    bars = data["bars"]
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values; o = df["open"].values
            hi = df["high"].values; lo = df["low"].values
            n = len(c)
            dep = df.get("debug_info.components.depth.last_history_value")
            s = pd.Series(c)
            ret1 = s.pct_change().values
            ret5 = s.pct_change(5).values
            ret20 = s.pct_change(20).values
            low10 = s.rolling(10).min().values
            for i in range(0, n - h, h):
                rng = hi[i] - lo[i]
                rows.append(dict(coin=coin, w=w, fc=df["forecast"].iloc[i],
                                 reg=df["regime"].iloc[i],
                                 depth=(dep.iloc[i] if dep is not None else np.nan),
                                 fwd=c[i + h] / c[i] - 1, ret1=ret1[i], ret5=ret5[i],
                                 ret20=ret20[i],
                                 atlow=(c[i] <= low10[i] * 1.0001) if not np.isnan(low10[i]) else np.nan,
                                 clpos=((c[i] - lo[i]) / rng) if rng > 0 else np.nan,
                                 year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                 ts=df["timestamp"].iloc[i]))
    R = pd.DataFrame(rows)
    R["ex"] = R["fwd"] - R.groupby("coin")["fwd"].transform("mean")
    btc = R[R.coin == "BTCUSD"][["ts", "fwd"]].rename(columns={"fwd": "btcfwd"})
    R = R.merge(btc, on="ts", how="left")
    R["exbtc"] = R["fwd"] - R["btcfwd"]
    def summ(g, col="ex"):
        x = g[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), med=x.median(), hit=(x > 0).mean(),
                              t=(x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan)))
    def clus(g, col="ex"):
        m = g.groupby("ts")[col].mean().dropna()
        return pd.Series(dict(nts=len(m), mean=m.mean(), t=m.mean() / m.std() * np.sqrt(len(m))))
    top = R[R.fc >= 10]
    act = R[R.fc >= 5]
    out = {}
    out["top_cluster_t"] = clus(top).to_frame().T
    out["top_ex_w2"] = summ(top[top.w != "w2"]).to_frame().T
    out["top_w2_btcfwd_mean"] = top[top.w == "w2"].btcfwd.mean()
    out["top_by_ret1_sign"] = top.groupby(top.ret1 > 0).apply(summ)
    out["top_by_atlow"] = top.groupby("atlow").apply(summ)
    out["top_by_clpos_half"] = top.groupby(top.clpos > 0.5).apply(summ)
    out["fc5_by_ret5_sign"] = act.groupby(act.ret5 > 0).apply(summ)
    out["fc5_by_ret5_sign_exbtc"] = act[act.coin != "BTCUSD"].groupby(act.ret5 > 0).apply(lambda g: summ(g, "exbtc"))
    out["fc5_ret5neg_cluster"] = clus(act[act.ret5 <= 0]).to_frame().T
    out["fc5_ret5neg_by_year"] = act[act.ret5 <= 0].groupby("year").apply(summ)
    out["fc5_ret5neg_by_coin"] = act[act.ret5 <= 0].groupby("coin").apply(summ)
    out["all_ret5neg_vs_pos_any_fc_inreg"] = R[R.reg == "mean_reversion"].groupby([R.fc >= 5, R.ret5 > 0]).apply(summ)
    out["top_btc_share_var"] = pd.Series(dict(corr=top[["fwd", "btcfwd"]].corr().iloc[0, 1],
                                              exbtc_std=top.exbtc.std(), ex_std=top.ex.std()))
    return out
