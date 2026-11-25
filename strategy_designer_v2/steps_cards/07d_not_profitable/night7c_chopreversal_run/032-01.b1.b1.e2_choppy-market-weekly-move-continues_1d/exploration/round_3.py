def explore(data):
    import numpy as np, pandas as pd
    out = {}
    def tt(x):
        x = pd.Series(x).dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/x.std()*np.sqrt(len(x)) if len(x)>1 else np.nan))
    rows = []; P = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c)-7, 7):
                allr.append(c[i+7]/c[i]-1)
        drift = np.mean(allr); sd7 = np.std(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r1 = c.pct_change()
            er = (c-c.shift(30)).abs()/(c.diff().abs().rolling(30).sum())
            vol = r1.rolling(30).std()
            sc = (c/c.shift(7)-1)/(vol*np.sqrt(7))
            r30 = c/c.shift(30)-1
            a = b["postRebalance_current_allocation"].fillna(0)
            nr = c.shift(-1)/c-1
            P.append(pd.DataFrame(dict(coin=coin, w=w, wn=int(w[1:]), ts=b["timestamp"], a=a, gain=a*nr,
                                       regime=b["regime"], f=b["forecast"].fillna(0), sc=sc, er=er, r30=r30, nr=nr)))
            for i in range(0, len(c)-7, 7):
                rows.append(dict(coin=coin, w=w, er=er.iloc[i], sc=sc.iloc[i], fwd=c.iloc[i+7]/c.iloc[i]-1-drift,
                                 tot=c.iloc[i+7]/c.iloc[i]-1, sd7=sd7, r30=r30.iloc[i]))
    P = pd.concat(P)
    g = pd.DataFrame(rows).dropna(subset=["er","sc"])
    g["um"] = g.fwd*np.sign(g.sc); g["tm"] = g.tot*np.sign(g.sc)
    ch = g[g.er <= 0.3].copy()
    # ER bands inside chop
    ch["erb"] = pd.cut(ch.er, [0,0.1,0.2,0.3])
    out["raw_chop_by_er_band"] = ch.groupby("erb").um.apply(tt).unstack()
    # condition alone: undirected fwd (drift removed) on er<=0.2 vs 0.2-0.3, no signal
    out["condition_alone_undirected_fwd"] = ch.groupby("erb").fwd.apply(tt).unstack()
    # strength per case raw, |sc|>=1 vs below
    ch["big"] = ch.sc.abs() >= 1
    out["raw_chop_big_vs_small"] = ch.groupby("big").apply(lambda x: pd.Series(dict(n=len(x), um=x.um.mean(), tm=x.tm.mean(),
                    strength=(x.um/x.sd7).mean(), t=x.um.mean()/x.um.std()*np.sqrt(len(x))))).T
    # raw-sign held only in chop (er<=0.3), vs actual position: per-bar gain
    P = P.dropna(subset=["nr"])
    P["rawpos"] = np.where(P.er <= 0.3, np.sign(P.sc), 0)
    P["rawgain"] = P.rawpos*P.nr
    P["out_of_chop_held"] = (P.er > 0.3) & (P.a != 0)
    out["actual_held_out_of_chop"] = P.groupby("out_of_chop_held").agg(n=("gain","size"), gain=("gain","mean"))
    out["rawpos_gain"] = P.groupby("rawpos").agg(n=("rawgain","size"), gain=("rawgain","mean"))
    # deepest fall w16-w17: what was held
    F = P[P.wn.isin([16,17])]
    F = F.assign(side=np.sign(F.a))
    out["w16_17_by_side_regime"] = F.groupby(["regime","side"]).agg(n=("gain","size"), gain=("gain","mean"), r30=("r30","mean"), er=("er","mean"))
    out["w16_17_by_coin"] = F.groupby("coin").agg(gain=("gain","mean"), held_long=("a", lambda x:(x>0).mean()), held_short=("a", lambda x:(x<0).mean()), coin_ret=("nr","mean"))
    # shorts against a rising 30-day trend in chop: strength
    ch["against30"] = np.sign(ch.sc) != np.sign(ch.r30)
    out["raw_chop_sc_vs_30d_sign"] = ch.groupby("against30").um.apply(tt).unstack()
    return out
