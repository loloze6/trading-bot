def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    fcol = "forecast"
    dcol = "debug_info.components.above_ma.last_history_value"
    # pooled mean daily return per coin
    mu = {}
    for c in bars:
        rs = []
        for w, df in bars[c].items():
            r = df["close"].pct_change().dropna()
            rs.append(r)
        mu[c] = pd.concat(rs).mean()
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in [5, 10, 20, 40, 60]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=c, win=w, year=yr[i], h=h,
                                     f=df[fcol].iloc[i], d=df[dcol].iloc[i] if dcol in df else np.nan,
                                     ex=cl[i+h]/cl[i]-1 - h*mu[c]))
    R = pd.DataFrame(rows)
    out = {}
    def summ(g):
        return pd.Series(dict(n=len(g), mean=g.ex.mean(), median=g.ex.median(),
                              share_pos=(g.ex > 0).mean(),
                              t=g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g) > 2 else np.nan))
    # by horizon, active vs flat
    R["act"] = R.f > 0
    out["by_h_act"] = R.groupby(["h", "act"]).apply(summ)
    tt = []
    for h, g in R.groupby("h"):
        a = g[g.act].ex; b = g[~g.act].ex
        tt.append(dict(h=h, diff=a.mean()-b.mean(), t=stats.ttest_ind(a, b, equal_var=False).statistic))
    out["act_minus_flat"] = pd.DataFrame(tt)
    R20 = R[R.h == 20]
    A = R20[R20.act]
    out["h20_active_by_coin"] = A.groupby("coin").apply(summ)
    out["h20_active_by_year"] = A.groupby("year").apply(summ)
    A = A.copy()
    A["fq"] = pd.qcut(A.f, 4, labels=False, duplicates="drop")
    out["h20_active_by_fq"] = A.groupby("fq").apply(summ)
    D = R20.dropna(subset=["d"]).copy()
    D["dq"] = pd.qcut(D.d, 5, labels=False, duplicates="drop")
    out["h20_by_raw_distance_q"] = D.groupby("dq").apply(lambda g: pd.concat([summ(g), pd.Series(dict(dmean=g.d.mean()))]))
    R60 = R[(R.h == 60)].dropna(subset=["d"]).copy()
    R60["dq"] = pd.qcut(R60.d, 5, labels=False, duplicates="drop")
    out["h60_by_raw_distance_q"] = R60.groupby("dq").apply(summ)
    return out
