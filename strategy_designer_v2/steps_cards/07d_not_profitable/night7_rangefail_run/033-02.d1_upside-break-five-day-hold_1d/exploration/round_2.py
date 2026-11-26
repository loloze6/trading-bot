def explore(data):
    import numpy as np, pandas as pd
    out = {}
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; hi = b["high"]; lo = b["low"]
            prevhi = hi.shift(1).rolling(20).max()
            prevlo = lo.shift(1).rolling(20).min()
            dist = cl / prevhi - 1
            brk = dist > 0
            fresh = brk & ~brk.shift(1, fill_value=False)
            r = cl.pct_change()
            fwd1 = cl.shift(-1) / cl - 1
            fwd5 = cl.shift(-5) / cl - 1
            # bars since last fresh break
            idx = pd.Series(np.where(fresh, np.arange(len(b)), np.nan)).ffill()
            since = np.arange(len(b)) - idx
            # level of the broken high at the last fresh break
            brokenhi = pd.Series(np.where(fresh, prevhi, np.nan)).ffill()
            below_old = cl < brokenhi
            ret60 = cl / cl.shift(60) - 1
            ret20 = cl / cl.shift(20) - 1
            vol30 = r.rolling(30).std(); vol60 = r.rolling(60).std()
            rangepos = (cl - prevlo) / (prevhi - prevlo)
            pos = b["postRebalance_current_allocation"]
            df = pd.DataFrame(dict(coin=c, w=w, wn=int(w[1:]), i=np.arange(len(b)), day=pd.to_datetime(b["timestamp"]).dt.floor("D"),
                                   dist=dist, brk=brk, fresh=fresh, fwd1=fwd1, fwd5=fwd5, since=since,
                                   below_old=below_old, ret60=ret60, ret20=ret20, vr=vol30 / vol60,
                                   pos=pos, pnl=pos * fwd1, r=r, wid=(prevhi - prevlo) / cl))
            recs.append(df)
    X = pd.concat(recs, ignore_index=True)
    grid = X[X.i % 5 == 0]
    drift = grid.fwd5.mean()
    X["u5"] = X.fwd5 - drift
    H = X[X.pos.abs() > 0].copy()
    # held pnl by days since fresh break
    out["held_pnl_by_since"] = H.groupby(H.since.clip(upper=7))["pnl"].agg(["mean", "count", "sum"])
    # held pnl by whether close back below the broken high, after day 0
    H1 = H[H.since >= 1]
    out["held_pnl_since1_by_below_old"] = H1.groupby("below_old")["pnl"].agg(["mean", "count", "sum"])
    # trend sign
    X["trend"] = pd.cut(X.ret60, [-9, -0.10, 0.10, 99], labels=["falling", "choppy", "rising"])
    H = X[X.pos.abs() > 0].copy()
    out["held_pnl_by_trend"] = H.groupby("trend", observed=True)["pnl"].agg(["mean", "count", "sum"])
    C = X[X.fresh & X.fwd5.notna()].copy()
    def tt(s):
        return pd.Series(dict(mean=s.mean(), n=len(s), t=s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan))
    out["fresh_u5_by_trend"] = C.groupby("trend", observed=True)["u5"].apply(tt).unstack()
    N = grid[~grid.brk & grid.fwd5.notna()].copy()
    N["u5"] = N.fwd5 - drift
    N["trend"] = pd.cut(N.ret60, [-9, -0.10, 0.10, 99], labels=["falling", "choppy", "rising"])
    out["nonbreak_u5_by_trend"] = N.groupby("trend", observed=True)["u5"].apply(tt).unstack()
    # fresh cases by range width (squeeze before break)
    C["wq"] = pd.qcut(C.wid, 3, labels=False)
    out["fresh_u5_by_width"] = C.groupby("wq")["u5"].apply(tt).unstack()
    N["wq"] = pd.qcut(N.wid, 3, labels=False)
    out["nonbreak_u5_by_width"] = N.groupby("wq")["u5"].apply(tt).unstack()
    # fresh cases: next day failed back below old high -> remaining 4-day move
    X["fwd4_from1"] = X.groupby(["coin", "w"])["fwd5"].shift(-1)  # not exact; compute directly
    rows = []
    for (c, w), g in X.groupby(["coin", "w"]):
        g = g.reset_index(drop=True)
        for k in np.where(g.fresh.values)[0]:
            if k + 5 < len(g):
                c0 = (1 + g.fwd1.iloc[k]);  # close k+1 / close k
                d1_fail = g.below_old.iloc[k + 1]
                rem = (1 + g.fwd5.iloc[k]) / c0 - 1
                rows.append(dict(fail=d1_fail, rem=rem, d1=g.fwd1.iloc[k]))
    F = pd.DataFrame(rows)
    out["after_day1_fail_remaining4d"] = F.groupby("fail")[["rem", "d1"]].agg(["mean", "count"])
    # drawdown episodes of the book: deepest
    D = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return"]].copy(); dd["wn"] = int(w[1:]); dd["coin"] = c; D.append(dd)
    D = pd.concat(D); D["day"] = pd.to_datetime(D.day)
    B = D.groupby(["wn", "day"])["book_return"].mean().reset_index().sort_values(["wn", "day"]).dropna()
    v = (1 + B.book_return).cumprod().values
    B["dd"] = v / np.maximum.accumulate(v) - 1
    # mark days in drawdown deeper than 3%
    deep = B[B.dd < -0.03][["wn", "day"]]
    Xd = X.copy(); Xd["dayk"] = Xd.day
    M = Xd.merge(deep, left_on=["wn", "dayk"], right_on=["wn", "day"], suffixes=("", "_y"))
    Hm = M[M.pos.abs() > 0]
    out["in_deep_dd_held"] = pd.Series(dict(n_days=len(deep), held_bars=len(Hm), pnl_mean=Hm.pnl.mean(),
                                            share_since_ge2=(Hm.since >= 2).mean(), share_below_old=Hm.below_old.mean(),
                                            share_rising=(Hm.ret60 > 0.1).mean(), mean_pos=Hm.pos.mean()))
    out["all_held"] = pd.Series(dict(share_since_ge2=(H.since >= 2).mean(), share_below_old=H.below_old.mean(),
                                     share_rising=(H.ret60 > 0.1).mean(), mean_pos=H.pos.mean()))
    out["deep_dd_days_by_window"] = deep.groupby("wn").size()
    return out
