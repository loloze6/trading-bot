def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            c = b["close"].values
            n = len(c)
            fc = b["forecast"].fillna(0).values
            pos = b["postRebalance_current_allocation"].fillna(0).values
            raw = b["debug_info.components.calm_up.last_history_value"].values
            for t in range(n):
                f1 = c[t+1]/c[t]-1 if t+1 < n else np.nan
                f5 = c[t+5]/c[t]-1 if t+5 < n else np.nan
                f2_5 = c[t+5]/c[t+1]-1 if t+5 < n else np.nan
                f10 = c[t+10]/c[t]-1 if t+10 < n else np.nan
                rows.append(dict(coin=coin, w=w, t=t, grid=(t % 5 == 0), fc=fc[t], pos=pos[t], raw=raw[t],
                                 f1=f1, f5=f5, f2_5=f2_5, f10=f10))
    R = pd.DataFrame(rows)
    R["fb"] = pd.cut(R.fc, [-0.001, 0.0, 0.5, 2, 8, 20.01])
    G = R[R.grid]
    out["grid_by_fc_bucket"] = G.groupby("fb", observed=True).agg(n=("f5", "count"), f1=("f1", "mean"), f2_5=("f2_5", "mean"),
                                                   f5=("f5", "mean"), f10=("f10", "mean"), pos=("pos", "mean"))
    out["grid_coin_mean"] = pd.Series(dict(f1=G.f1.mean(), f5=G.f5.mean(), f10=G.f10.mean()))
    # raw component positive (graded) on grid, by raw quintile among positive
    P = G[G.raw > 0].copy()
    P["rq"] = pd.qcut(P.raw, 5, labels=False)
    out["grid_by_raw_quintile"] = P.groupby("rq").agg(n=("f5", "count"), raw=("raw", "mean"), f1=("f1", "mean"),
                                                     f5=("f5", "mean"), f10=("f10", "mean"), fc=("fc", "mean"))
    # share of time in market and decomposition
    allb = []
    for coin in data["days"]:
        for w, d in data["days"][coin].items():
            allb.append(d.assign(coin=coin, w=w))
    D = pd.concat(allb)
    out["active_share"] = pd.Series(dict(share_pos_gt_0_01=(R.pos > 0.01).mean(), mean_pos=R.pos.mean(),
                                         mean_pos_when_active=R.pos[R.pos > 0.01].mean()))
    # book drawdown chain
    dd = []
    for coin in data["days"]:
        eq = (1 + D[D.coin == coin].book_return.fillna(0)).cumprod()
        dd.append(dict(coin=coin, maxdd=(eq/eq.cummax()-1).min(), total=eq.iloc[-1]-1))
    out["dd"] = pd.DataFrame(dd)
    return out
