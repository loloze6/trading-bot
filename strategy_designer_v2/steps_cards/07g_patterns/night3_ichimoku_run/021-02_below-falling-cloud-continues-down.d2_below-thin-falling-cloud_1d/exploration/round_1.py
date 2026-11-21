def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(c)
            ten = (hi.rolling(9).max()+lo.rolling(9).min())/2
            kij = (hi.rolling(26).max()+lo.rolling(26).min())/2
            sa = ((ten+kij)/2).shift(26)
            sb = ((hi.rolling(52).max()+lo.rolling(52).min())/2).shift(26)
            top = np.maximum(sa, sb); bot = np.minimum(sa, sb); mid = (sa+sb)/2
            width = (top-bot)/c
            slope = mid/mid.shift(26)-1
            r1 = c.pct_change()
            vol = r1.rolling(26).std()
            past26 = c/c.shift(26)-1
            past7 = c/c.shift(7)-1
            hi52 = c/c.rolling(52).max()-1
            ma = c/c.rolling(52).mean()-1
            dist = np.where(c<bot, c/bot-1, np.where(c>top, c/top-1, 0.0))
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            for h in (7, 26):
                for t in range(0, n-h, h):
                    rows.append(dict(coin=coin, w=w, h=h, fwd=c[t+h]/c[t]-1, past26=past26[t], past7=past7[t],
                        vol=vol[t], width=width[t], slope=slope[t], hi52=hi52[t], ma=ma[t], dist=dist[t],
                        below=c[t]<bot[t] if pd.notna(bot[t]) else np.nan,
                        above=c[t]>top[t] if pd.notna(top[t]) else np.nan,
                        fc=b["forecast"][t]))
    df = pd.DataFrame(rows)
    # drift and usual move per coin per h
    g = df.groupby(["coin","h"])["fwd"]
    df["drift"] = g.transform("mean"); df["usual"] = g.transform("std")
    df["z"] = (df["fwd"]-df["drift"])/df["usual"]
    out = {}
    feats = ["past26","past7","vol","width","slope","hi52","ma","dist"]
    res = []
    for h in (7,26):
        d = df[df.h==h]
        for f in feats:
            x = d.dropna(subset=[f,"z"])
            # per coin rank to pool
            rk = x.groupby("coin")[f].rank(pct=True)
            rho, p = stats.spearmanr(rk, x["z"])
            q = pd.qcut(rk, 5, labels=False, duplicates="drop")
            m = x.groupby(q)["z"].mean()
            ncoin_pos = sum(stats.spearmanr(xx[f], xx["z"])[0] > 0 for _, xx in x.groupby("coin"))
            res.append(dict(h=h, feat=f, n=len(x), rho=rho, p=p, q1=m.iloc[0], q3=m.iloc[2], q5=m.iloc[-1], coins_pos=ncoin_pos))
    out["feature_vs_next_z"] = pd.DataFrame(res)
    # states at 26
    d = df[(df.h==26)].dropna(subset=["below","slope"])
    st = np.where(d.below & (d.slope<0), "below_fall", np.where(d.above & (d.slope>0), "above_rise", "other"))
    s = d.assign(st=st).groupby("st")
    out["states26"] = pd.DataFrame({"n": s.size(), "mean_ex": s.apply(lambda x: (x.fwd-x.drift).mean()),
        "z": s["z"].mean(), "t": s["z"].apply(lambda v: v.mean()/(v.std()/np.sqrt(len(v))))})
    # weekday daily book/coin returns
    dd = pd.concat([x.assign(coin=c_) for c_ in days for x in days[c_].values()])
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    out["weekday_coin"] = dd.groupby("wd")["coin_return"].agg(["mean","count", lambda v: v.mean()/(v.std()/np.sqrt(v.count()))])
    # returns after large daily moves (next day)
    bb = []
    for coin in days:
        for w, x in days[coin].items():
            x = x.reset_index(drop=True)
            r = x["coin_return"]; sd = r.std()
            bb.append(pd.DataFrame({"zr": r/sd, "nxt": r.shift(-1)/sd, "nxt7": (x["close"].shift(-7)/x["close"]-1)}))
    bb = pd.concat(bb).dropna()
    bb["b"] = pd.cut(bb.zr, [-99,-2,-1,0,1,2,99])
    out["after_daily_move"] = bb.groupby("b")[["nxt","nxt7"]].agg(["mean","count"])
    # book: daily book return by regime of position
    out["book_daily"] = pd.Series({"mean": dd.book_return.mean(), "sd": dd.book_return.std(), "n": dd.book_return.count()})
    return out
