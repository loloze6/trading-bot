def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; trades = data["trades"]
    g = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True); cl = b["close"].values; n = len(b)
            s = pd.Series(cl); r1 = s.pct_change(); vol30 = r1.rolling(30, min_periods=20).std()
            sr = s.pct_change(7)/(vol30*np.sqrt(7)); r30 = s.pct_change(30); r60 = s.pct_change(60)
            hi30 = s.rolling(30, min_periods=20).max(); lo30 = s.rolling(30, min_periods=20).min()
            pos = (s - lo30)/(hi30 - lo30)
            H = 14
            for i in range(0, n-H, H):
                g.append(dict(coin=c, win=w, day=str(pd.to_datetime(b["timestamp"].iloc[i]).date()),
                              fwd=cl[i+H]/cl[i]-1, sr=sr.iloc[i], r30=r30.iloc[i], r60=r60.iloc[i], pos=pos.iloc[i],
                              inp=b["regime"].iloc[i]=="unknown", fc=b["forecast"].iloc[i]))
    g = pd.DataFrame(g)
    g["ex"] = g.fwd - g.groupby("coin").fwd.transform("mean")
    def s2(d):
        if len(d) < 3: return pd.Series(dict(n=len(d), mean_ex=d.ex.mean(), t=np.nan, days=d.day.nunique()))
        dd = d.groupby("day").ex.sum(); m = d.ex.mean()
        se = np.sqrt((dd - dd.mean()*0 - m*d.groupby("day").size()).pow(2).sum())/len(d)
        return pd.Series(dict(n=len(d), mean_ex=m, t=m/se if se > 0 else np.nan, days=d.day.nunique()))
    P = g[g.inp].copy()
    P["sig"] = np.where(P.fc > 0, np.where(P.sr > 0.5, "strong", "weak"), "none")
    out["in profile by signal class"] = P.groupby("sig").apply(s2)
    out["in profile by signal and r30 sign"] = P.groupby(["sig", P.r30 > 0]).apply(s2)
    out["in profile by signal and range position (top half)"] = P.groupby(["sig", P.pos > 0.5]).apply(s2)
    out["in profile by signal and r60 sign"] = P.dropna(subset=["r60"]).groupby(["sig", P.r60 > 0]).apply(s2)
    out["in profile strong signal by window"] = P[P.sig == "strong"].groupby("win").apply(s2)
    out["in profile weak signal by window"] = P[P.sig == "weak"].groupby("win").apply(s2)
    # trades: entry raw sr > 0.5 vs not, by window, book pnl
    rows = []
    for c in trades:
        for w, t in trades[c].items():
            if not len(t): continue
            b = bars[c][w].reset_index(drop=True); ts = pd.to_datetime(b["timestamp"])
            s = b["close"]; vol30 = s.pct_change().rolling(30, min_periods=20).std()
            sr = s.pct_change(7)/(vol30*np.sqrt(7)); r30 = s.pct_change(30)
            for _, tr in t.iterrows():
                ie = ts.searchsorted(pd.to_datetime(tr["entry_time"]), side="right")-1
                if ie < 0: continue
                a = abs(b["postRebalance_current_allocation"].iloc[ie])
                rows.append(dict(win=w, net=tr["net_profit_loss_percent"], strong=sr.iloc[ie] > 0.5,
                                 r30pos=r30.iloc[ie] > 0, pnl=tr["net_profit_loss_percent"]*a))
    T = pd.DataFrame(rows)
    out["trades by strong, book pnl"] = T.groupby("strong").agg(n=("net","size"), mean=("net","mean"), pnl=("pnl","sum"), hit=("net", lambda x: (x>0).mean()))
    out["trades by strong and r30>0"] = T.groupby(["strong","r30pos"]).agg(n=("net","size"), mean=("net","mean"), pnl=("pnl","sum"))
    out["trades strong pnl by window"] = T[T.strong].groupby("win").pnl.sum()
    out["trades weak pnl by window"] = T[~T.strong].groupby("win").pnl.sum()
    return out
