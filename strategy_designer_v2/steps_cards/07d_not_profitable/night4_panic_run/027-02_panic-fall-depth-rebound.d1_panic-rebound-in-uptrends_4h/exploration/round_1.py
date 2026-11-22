import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    out = {}
    # basic book stats
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            t = trades[c].get(w) if isinstance(trades[c], dict) else None
            ntr = 0 if t is None else len(t)
            act = (b["postRebalance_current_allocation"].abs() > 1e-9).mean()
            panic = (b["regime"] == "mean_reversion").mean()
            fpos = (b["forecast"] > 0).mean()
            rows.append(dict(coin=c, win=w, trades=ntr, active=act, panic=panic, fpos=fpos,
                             alloc_mean_when_in=b.loc[b["postRebalance_current_allocation"].abs()>1e-9,"postRebalance_current_allocation"].abs().mean()))
    df = pd.DataFrame(rows)
    out["by_coin"] = df.groupby("coin")[["trades","active","panic","fpos","alloc_mean_when_in"]].agg({"trades":"sum","active":"mean","panic":"mean","fpos":"mean","alloc_mean_when_in":"mean"})
    # trades summary
    tl = []
    for c in trades:
        for w, t in trades[c].items():
            if t is None or len(t)==0: continue
            tt = t.copy(); tt["coin"]=c; tt["win"]=w; tl.append(tt)
    T = pd.concat(tl) if tl else pd.DataFrame()
    if len(T):
        T["dur_days"]=T["duration_minutes"]/1440
        out["trades_summary"] = pd.Series({"n":len(T),"mean_net":T["net_profit_loss_percent"].mean(),
            "median_net":T["net_profit_loss_percent"].median(),"win_share":(T["net_profit_loss_percent"]>0).mean(),
            "mean_dur_days":T["dur_days"].mean(),"mean_entry_fc":T["entry_forecast"].mean()})
    # recompute panic and forward 84 returns on grid, graded by ratio and by 90d sign, fall depth
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            rng = (b["high"]-b["low"])/b["close"]
            r6 = rng.rolling(6).mean(); r180 = rng.rolling(180).mean()
            ratio = r6/r180
            fall6 = b["close"]/b["close"].shift(6)-1
            ret540 = b["close"]/b["close"].shift(540)-1
            ret84 = b["close"]/b["close"].shift(84)-1
            fwd = b["close"].shift(-84)/b["close"]-1
            usual6 = (b["close"]/b["close"].shift(6)-1).abs().rolling(180).mean()
            n=len(b)
            for g0 in range(0, n-84, 84):
                cell = slice(g0, g0+84)
                rr = ratio.iloc[cell]
                if rr.isna().all(): continue
                i = rr.idxmax()
                recs.append(dict(coin=c, win=w, ratio=rr.max(), fall=fall6.iloc[i]/usual6.iloc[i] if usual6.iloc[i]>0 else np.nan,
                                 ret540=ret540.iloc[i], ret84=ret84.iloc[i], fwd=fwd.iloc[i], fc=b["forecast"].iloc[i]))
    R = pd.DataFrame(recs).dropna(subset=["fwd","ratio"])
    drift = R.groupby("coin")["fwd"].transform("mean")  # approximate drift per coin
    R["unus"] = R["fwd"]-drift
    R["rbin"] = pd.cut(R["ratio"],[0,1.5,2,2.5,3,100])
    def summ(g):
        return pd.Series({"n":len(g),"mean_unus":g["unus"].mean(),"t":g["unus"].mean()/(g["unus"].std()/np.sqrt(len(g))) if len(g)>2 else np.nan})
    out["cell_max_ratio_bins"] = R.groupby("rbin").apply(summ)
    S = R[(R["ratio"]>=2)&(R["fall"]<0)]
    S = S.assign(up90=S["ret540"]>0)
    out["ratio2_falling_by_90d_sign"] = S.groupby("up90").apply(summ)
    S2 = S.assign(fallq=pd.qcut(-S["fall"],3,labels=["shallow","mid","deep"]))
    out["ratio2_falling_by_fall_depth"] = S2.groupby("fallq").apply(summ)
    S3 = R[(R["ratio"]>=2)&(R["fall"]<0)].assign(up14=lambda x: x["ret84"]>0)
    out["ratio2_falling_by_prior14d"] = S3.groupby("up14").apply(summ)
    S4 = R[(R["ratio"]>=3)&(R["fall"]<0)].assign(up90=lambda x: x["ret540"]>0)
    out["ratio3_falling_by_90d_sign"] = S4.groupby("up90").apply(summ)
    return out
