def explore(data):
    import numpy as np, pandas as pd
    out = {}
    COST = 0.0022
    recs = []; ctrl = []
    for coin, wd in data["bars"].items():
        for w, b in wd.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values.astype(float)
            r = pd.Series(c).pct_change()
            ratio = (r.rolling(20).std()/r.rolling(60).std()).values
            ret20 = (pd.Series(c)/pd.Series(c).shift(20)-1).values
            a = b["postRebalance_current_allocation"].fillna(0).values
            ap = b["previous_allocation"].fillna(0).values
            n = len(b)
            # bar pnl net, and which Sunday case it belongs to
            caseid = np.full(n, -1)
            for i in range(n):
                if ts.iloc[i].weekday()==6 and b["forecast"].iloc[i]!=0 and not np.isnan(b["forecast"].iloc[i]):
                    for k in range(i, min(i+3, n)):
                        caseid[k] = i
            for i in range(n-1):
                g = a[i]*(c[i+1]/c[i]-1) - abs(a[i]-ap[i])*COST/2
                ci = caseid[i]
                recs.append(dict(coin=coin, wn=int(w[1:]), day=ts.iloc[i].normalize(), g=g,
                                 ratio=ratio[ci] if ci>=0 else np.nan,
                                 sret=(ret20[ci]*np.sign(b["forecast"].iloc[ci])) if ci>=0 else np.nan,
                                 side=np.sign(b["forecast"].iloc[ci]) if ci>=0 else 0))
            # control: non-Sunday bars, bet against 1-day move, by ratio
            for i in range(60, n-2):
                if ts.iloc[i].weekday()!=6 and i % 2 == 0:
                    s = -np.sign(r.iloc[i])
                    ctrl.append(dict(ratio=ratio[i], s=s*(c[i+2]/c[i]-1), wd=ts.iloc[i].weekday()))
    R = pd.DataFrame(recs)
    qs = R["ratio"].dropna().quantile([0.2,0.4,0.6,0.8]).values
    def book(mask):
        x = R.copy(); x.loc[~mask, "g"] = 0.0
        d = x.groupby(["wn","day"])["g"].mean().reset_index().sort_values(["wn","day"])
        v = (1+d["g"]).cumprod(); dd = (v/v.cummax()-1).min()
        yr = v.iloc[-1]**(365/len(d))-1
        return pd.Series({"sharpe": d["g"].mean()/d["g"].std()*np.sqrt(365), "yearly": yr, "maxdd": dd, "calmar": yr/abs(dd)})
    allm = pd.Series(True, index=R.index)
    out["books"] = pd.DataFrame({
        "all": book(allm),
        "ratio>=q40": book(R["ratio"]>=qs[1]),
        "ratio>=q60": book(R["ratio"]>=qs[2]),
        "ratio>=q80": book(R["ratio"]>=qs[3]),
        "ratio<q20_or>=q60": book((R["ratio"]<qs[0])|(R["ratio"]>=qs[2])),
        "against_trend_sret<0": book(R["sret"]<0),
    }).T
    # drawdown of full book: pnl by ratio bucket inside the deepest falls
    d = R.groupby(["wn","day"])["g"].mean().reset_index().sort_values(["wn","day"]).reset_index(drop=True)
    v = (1+d["g"]).cumprod(); peak = v.cummax(); dd = v/peak-1
    trough = dd.idxmin(); pk = v.iloc[:trough+1].idxmax()
    sel = d.iloc[pk:trough+1][["wn","day"]]
    X = R.merge(sel, on=["wn","day"])
    X["rq"] = pd.cut(X["ratio"], [-np.inf]+list(qs)+[np.inf], labels=False)
    out["deepest_fall_pnl_by_ratio_q"] = X.groupby("rq")["g"].agg(["count","sum"])
    out["deepest_fall_pnl_by_side"] = X.groupby("side")["g"].agg(["count","sum"])
    out["deepest_fall_len_days"] = int(trough-pk)
    Cc = pd.DataFrame(ctrl).dropna()
    Cc["rq"] = pd.cut(Cc["ratio"], [-np.inf]+list(qs)+[np.inf], labels=False)
    out["control_weekday_reversal_by_ratio_q"] = Cc.groupby("rq")["s"].agg(n="size", mean="mean",
        t=lambda s: s.mean()/(s.std()/np.sqrt(len(s))))
    return out
