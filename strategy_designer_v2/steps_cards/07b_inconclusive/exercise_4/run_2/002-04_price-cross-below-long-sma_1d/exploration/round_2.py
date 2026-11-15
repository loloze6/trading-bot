def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    mu = {}
    for c in bars:
        mu[c] = pd.concat([df["close"].pct_change().dropna() for df in bars[c].values()]).mean()
    rows = []
    for H in [10, 20]:
        for c in bars:
            for w, df in bars[c].items():
                df = df.reset_index(drop=True)
                cl = df["close"].values.astype(float)
                dist = df["debug_info.components.below_ma.last_history_value"].values.astype(float)
                sma = cl / (1 + dist/100.0)
                al = df["postRebalance_current_allocation"].values.astype(float)
                below = (dist < 0).astype(int)
                run = np.zeros(len(df))
                for i in range(len(df)):
                    run[i] = (run[i-1]+1 if i>0 else 1) if below[i] else 0
                for i in range(0, len(df)-H, H):
                    if not (dist[i] < 0):
                        continue
                    ex = cl[i+H]/cl[i]-1 - H*mu[c]
                    slope = sma[i]/sma[i-20]-1 if i >= 20 else np.nan
                    r30 = cl[i]/cl[i-30]-1 if i >= 30 else np.nan
                    rows.append(dict(H=H, coin=c, ex=ex, slope=slope, r30=r30, run=run[i], al=al[i],
                                     dist=dist[i]))
    R = pd.DataFrame(rows)
    def ts(s):
        s = s.dropna(); n=len(s)
        return pd.Series({"n": n, "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(n)) if n>2 else np.nan,
                          "share_down": (s<0).mean()})
    out = {}
    for H in [10, 20]:
        X = R[R.H==H].copy()
        X["slope_sign"] = np.where(X.slope.isna(), "na", np.where(X.slope<0, "sma_falling", "sma_rising"))
        out[f"H{H}_by_sma_slope"] = X.groupby("slope_sign")["ex"].apply(ts).unstack()
        Y = X.dropna(subset=["slope"]).copy()
        Y["sq"] = pd.qcut(Y.slope, 4, labels=["fall_most","q2","q3","rise_most"])
        out[f"H{H}_by_slope_q"] = Y.groupby("sq")["ex"].apply(ts).unstack()
        Z = X.dropna(subset=["r30"]).copy()
        Z["rq"] = pd.qcut(Z.r30, 4, labels=["r30_low","q2","q3","r30_high"])
        out[f"H{H}_by_r30_q"] = Z.groupby("rq")["ex"].apply(ts).unstack()
        X["runb"] = pd.cut(X.run, [0,10,30,60,1000], labels=["<=10","11-30","31-60",">60"])
        out[f"H{H}_by_run"] = X.groupby("runb")["ex"].apply(ts).unstack()
    X = R[(R.H==10)].dropna(subset=["slope"])
    F = X[X.slope<0]
    out["H10_falling_prod_mean_t"] = ts(F.al*F.ex)
    out["H10_falling_by_coin"] = F.groupby("coin")["ex"].apply(ts).unstack()
    return out
