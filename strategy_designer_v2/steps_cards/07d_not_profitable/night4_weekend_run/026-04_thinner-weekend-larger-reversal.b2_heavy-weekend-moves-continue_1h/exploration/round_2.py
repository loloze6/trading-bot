def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]
    def tt(x):
        x = pd.Series(x).dropna()
        return pd.Series(dict(mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>1 else np.nan, n=len(x)))
    # drift per coin, 48 and 120 bar non-overlapping
    drift = {}
    for c in bars:
        for h in [48, 120]:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                for k in range(0, len(cl) - h, h):
                    rs.append(cl[k+h]/cl[k]-1)
            drift[(c, h)] = np.mean(rs)
    # all Sunday 23:00 bars, recomputed from prices, gated or not
    cs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values; v = b["volume"].values
            rv = pd.Series(np.log(cl)).diff().rolling(720, min_periods=240).std().values
            idx = np.where((ts.dt.dayofweek == 6) & (ts.dt.hour == 23))[0]
            for k in idx:
                if k < 168: continue
                m = cl[k]/cl[k-48]-1; s = np.sign(m)
                if s == 0: continue
                vr = v[k-47:k+1].mean()/v[k-167:k-47].mean()
                # prior-week (weekday) move, signed
                pw = s*(cl[k-48]/cl[k-168]-1)
                rec = dict(coin=c, wn=int(w[1:]), m=m, am=abs(m), vr=vr, pw=pw,
                           am_vol=abs(m)/(rv[k]*np.sqrt(48)) if rv[k] > 0 else np.nan,
                           f=b["forecast"].iloc[k])
                for h in [48, 120]:
                    rec[f"u{h}"] = s*(cl[k+h]/cl[k]-1 - drift[(c, h)]) if k+h < len(cl) else np.nan
                cs.append(rec)
    C = pd.DataFrame(cs)
    C["gated"] = C["vr"] > 1
    out["u48_u120_by_gate"] = pd.concat({g: pd.DataFrame({"u48": tt(x["u48"]), "u120": tt(x["u120"])}).T
                                         for g, x in C.groupby("gated")})
    out["u120_by_vr_q_all"] = C.groupby(pd.qcut(C["vr"], 5, labels=False))["u120"].apply(tt).unstack()
    out["u120_by_amvol_q_all"] = C.groupby(pd.qcut(C["am_vol"], 5, labels=False))["u120"].apply(tt).unstack()
    out["u48_by_amvol_q_all"] = C.groupby(pd.qcut(C["am_vol"], 5, labels=False))["u48"].apply(tt).unstack()
    out["u120_by_priorweek_sign_gated"] = C[C.gated].groupby(np.sign(C.loc[C.gated, "pw"]))["u120"].apply(tt).unstack()
    out["u120_by_priorweek_sign_all"] = C.groupby(np.sign(C["pw"]))["u120"].apply(tt).unstack()
    # trades: worst ones and losses in w22-24
    T = pd.concat([t.assign(coin=c, wn=int(w[1:])) for c in data["trades"] for w, t in data["trades"][c].items() if len(t)])
    T["loss"] = T["net_profit_loss_percent"]
    out["trades_by_coin"] = T.groupby("coin")["loss"].agg(["count", "mean", "min", "sum"])
    out["trades_w22_24_by_coin"] = T[T.wn >= 22].groupby("coin")["loss"].agg(["count", "mean", "sum"])
    out["trade_net_quantiles"] = T["loss"].quantile([0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
    out["trade_duration_h_quantiles"] = (T["duration_minutes"]/60).quantile([0.1, 0.5, 0.9, 0.99])
    out["share_trades_worse_than_-15pct"] = (T["loss"] < -15).mean()
    # book daily: share of sum of returns from worst days; days in position
    dd = []
    for c in days:
        for w, d in days[c].items():
            x = d[["day", "book_return"]].copy(); x["w"] = w; dd.append(x)
    B = pd.concat(dd).groupby(["w", "day"])["book_return"].mean().dropna()
    out["book_daily"] = pd.Series(dict(mean=B.mean(), std=B.std(), share_days_nonzero=(B.abs() > 1e-9).mean(),
                                       sum_worst10=B.nsmallest(10).sum(), sum_all=B.sum(),
                                       mean_nonzero=B[B.abs() > 1e-9].mean()))
    return out
