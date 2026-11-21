def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; trd = []; fc = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            pos = b["postRebalance_current_allocation"].fillna(0).values.astype(float)
            r1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            gross = pos*r1
            fee = (b["postRebalance_total_value"]-b["total_portfolio_value"]).values/b["total_portfolio_value"].values
            turnover = np.abs(b["allocation_change"].fillna(0).values.astype(float)) if "allocation_change" in b else np.abs(np.diff(np.r_[0,pos]))
            rows.append(dict(coin=coin, w=w, bars=len(b), gross=np.nansum(gross), fee=np.nansum(fee),
                             turnover=np.nansum(turnover), meanpos=np.nanmean(pos), inpos=np.mean(pos>0)))
            f = b["forecast"].fillna(0).values
            for h in [2,4,8,24]:
                idx = np.arange(0, len(c)-h, 2)
                fr = c[idx+h]/c[idx]-1
                fc.append(pd.DataFrame(dict(coin=coin,h=h,f=f[idx],fr=fr)))
        for w, t in data["trades"][coin].items():
            if len(t): trd.append(t.assign(coin=coin))
    R = pd.DataFrame(rows)
    g = R.groupby("coin")[["gross","fee","turnover"]].sum()
    g["net"] = g.gross+g.fee
    g["bars"] = R.groupby("coin").bars.sum()
    out["gross_vs_fee_by_coin"] = g
    out["fee_per_turnover"] = float(R.fee.sum()/R.turnover.sum())
    out["mean_pos"] = float(np.average(R.meanpos, weights=R.bars))
    T = pd.concat(trd)
    T["fq"] = pd.qcut(T.entry_forecast.rank(method="first"), 5, labels=False)
    out["trades_by_fq"] = T.groupby("fq").agg(n=("side","size"), f=("entry_forecast","mean"),
        pl=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"),
        comm=("total_commission","mean"), dur_h=("duration_minutes", lambda x: x.mean()/60))
    T["dur_b"] = pd.cut(T.duration_minutes/60, [0,1,2,4,8,24,1e9])
    out["trades_by_dur"] = T.groupby("dur_b").agg(n=("side","size"), pl=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"))
    F = pd.concat(fc)
    F["ex"] = F.fr - F.groupby(["coin","h"]).fr.transform("mean")
    F["bk"] = np.where(F.f<=0, -1, 0)
    pos = F.f>0
    F.loc[pos,"bk"] = F[pos].groupby(["coin","h"]).f.transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False)+0)
    out["fwd_excess_bp_by_bucket_h"] = (F.groupby(["bk","h"]).ex.mean()*1e4).unstack()
    out["n_by_bucket"] = F[F.h==2].groupby("bk").size()
    return out
