def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []; P = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - 7, 7):
                allr.append(c[i+7]/c[i]-1)
        drift = np.mean(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r1 = c.pct_change()
            er = (c - c.shift(30)).abs() / (c.diff().abs().rolling(30).sum())
            vol = r1.rolling(30).std()
            sc = (c/c.shift(7)-1)/(vol*np.sqrt(7))
            f = b["forecast"].fillna(0)
            a = b["postRebalance_current_allocation"].fillna(0)
            nr = c.shift(-1)/c-1
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"])/b["total_portfolio_value"]
            agree = np.sign(f) == np.sign(sc)
            P.append(pd.DataFrame(dict(coin=coin, w=w, a=a, gain=a*nr, gain_d=a*(nr-drift/7), fee=fee,
                                       regime=b["regime"], f=f, agree=agree, er=er, vol=vol)))
            for i in range(0, len(c)-7, 7):
                rows.append(dict(coin=coin, w=w, er=er.iloc[i], sc=sc.iloc[i], f=f.iloc[i],
                                 fwd=c.iloc[i+7]/c.iloc[i]-1-drift, vol=vol.iloc[i], reg=b["regime"].iloc[i]))
    P = pd.concat(P).dropna(subset=["gain"])
    P["side"] = np.sign(P["a"])
    # disagreement between standardised forecast sign and raw sign, held bars
    H = P[P.a != 0].copy()
    H["agree"] = np.sign(H["a"]) == np.sign(H["f"]).where(H.f != 0, np.sign(H["a"]))
    out["held_by_regime_side"] = H.groupby(["regime","side"]).agg(n=("gain","size"), gain=("gain","mean"), gain_drift_removed=("gain_d","mean"), fee=("fee","mean"))
    M = P[P.f != 0]
    out["mr_bars_by_sign_agree"] = M.groupby(["agree", np.sign(M.f)]).agg(n=("gain","size"), gain=("gain","mean"), gain_d=("gain_d","mean"))
    # grid: raw scaled signal, choppy (recomputed er<=0.3), cases with sign by raw
    g = pd.DataFrame(rows).dropna(subset=["er","sc"])
    g["um"] = g.fwd*np.sign(g.sc)
    chop = g[g.er <= 0.3]; nch = g[g.er > 0.3]
    def tt(x): return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/x.std()*np.sqrt(len(x))))
    out["raw_signal_chop_vs_not"] = pd.DataFrame({"chop": tt(chop.um), "not_chop": tt(nch.um)}).T
    chop = chop.copy(); chop["scq"] = pd.qcut(chop.sc.abs(), 4, labels=False)
    out["raw_chop_by_abs_sc_q"] = chop.groupby("scq").um.apply(tt).unstack()
    chop["volq"] = pd.qcut(chop.vol, 3, labels=False)
    out["raw_chop_by_volq"] = chop.groupby("volq").um.apply(tt).unstack()
    out["raw_chop_by_side"] = chop.groupby(np.sign(chop.sc)).um.apply(tt).unstack()
    # weighted by |sc|
    out["raw_chop_weighted_by_abs_sc"] = float((chop.um*chop.sc.abs()).sum()/chop.sc.abs().sum())
    # drawdown: book chain by window
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"]=coin; d["w"]=w; D.append(d)
    D = pd.concat(D).dropna(subset=["book_return"])
    bk = D.groupby(["w","day"]).agg(b=("book_return","mean"), h=("coin_return","mean")).reset_index()
    bk["wn"] = bk.w.str[1:].astype(int); bk = bk.sort_values(["wn","day"]).reset_index(drop=True)
    v = (1+bk.b).cumprod(); dd = v/v.cummax()-1
    trough = dd.idxmin(); peak = v[:trough+1].idxmax()
    seg = bk.iloc[peak:trough+1]
    out["deepest_fall"] = pd.Series(dict(depth=dd.min(), days=len(seg), windows=",".join(seg.w.unique()),
                                         book_sum=seg.b.sum(), hold_sum=seg.h.sum(), corr=seg.b.corr(seg.h)))
    out["dd_by_window"] = bk.assign(dd=dd).groupby("w").dd.min().sort_values().head(6)
    return out
