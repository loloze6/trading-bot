def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            s = pd.Series(c)
            r1 = s.pct_change()
            vol = r1.rolling(20, min_periods=10).std().values
            p26 = (s/s.shift(26)-1).values
            p7 = (s/s.shift(7)-1).values
            p3 = (s/s.shift(3)-1).values
            ma = (s/s.rolling(30, min_periods=15).mean()-1).values
            hi30 = (s/s.rolling(30, min_periods=15).max()-1).values
            fc = b["forecast"].astype(float).values
            reg = (b["regime"].astype(str)=="trending").values
            for h in (7, 26):
                for t in range(0, n-h, h):
                    rows.append(dict(coin=coin, w=w, h=h, fwd=c[t+h]/c[t]-1, p26=p26[t], p7=p7[t], p3=p3[t],
                                     vol=vol[t], ma=ma[t], hi30=hi30[t], fc=fc[t], reg=reg[t]))
    df = pd.DataFrame(rows)
    out["n_rows"] = pd.Series({"rows": len(df), "rows_h26": int((df.h==26).sum()), "reg_h26": int(df[df.h==26].reg.sum())})
    g = df.groupby(["coin","h"])["fwd"]
    df["drift"] = g.transform("mean"); df["usual"] = g.transform("std")
    df["z"] = (df["fwd"]-df["drift"])/df["usual"]
    res = []
    for h in (7,26):
        d = df[df.h==h]
        for f in ["p26","p7","p3","vol","ma","hi30"]:
            try:
                x = d.dropna(subset=[f,"z"]).copy()
                x["rk"] = x.groupby("coin")[f].rank(pct=True)
                rho, p = stats.spearmanr(x["rk"], x["z"])
                lo = x[x.rk<=0.2]["z"]; hi = x[x.rk>0.8]["z"]
                tt = stats.ttest_ind(hi, lo, equal_var=False)[0]
                cp = 0
                for _, xx in x.groupby("coin"):
                    if len(xx) > 5 and stats.spearmanr(xx[f], xx["z"])[0] > 0: cp += 1
                res.append(dict(h=h, feat=f, n=len(x), rho=rho, p=p, z_low20=lo.mean(), z_top20=hi.mean(),
                                t_top_minus_low=tt, coins_pos=cp))
            except Exception as e:
                res.append(dict(h=h, feat=f, n=-1))
    out["feature_vs_next_z"] = pd.DataFrame(res)
    try:
        d = df[df.h==26]
        k = d.groupby("reg").agg(n=("z","size"), z=("z","mean"), ex=("fwd", lambda v: np.nan))
        k["ex"] = d.groupby("reg").apply(lambda x: (x.fwd-x.drift).mean())
        k["t"] = d.groupby("reg")["z"].apply(lambda v: v.mean()/(v.std()/np.sqrt(len(v))))
        out["regime26"] = k
        # in regime: by past26 tercile
        dr = d[d.reg].dropna(subset=["p26"]).copy()
        dr["q"] = pd.qcut(dr.p26.rank(method="first"), 3, labels=["low","mid","high"])
        out["reg_by_past26"] = dr.groupby("q")["z"].agg(["mean","count", lambda v: v.mean()/(v.std()/np.sqrt(len(v)))])
    except Exception as e:
        out["regime_err"] = str(e)[:100]
    try:
        dd = pd.concat([x.assign(coin=c_, w=w_) for c_ in days for w_, x in days[c_].items()])
        dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
        out["weekday"] = dd.groupby("wd").agg(coin_mean=("coin_return","mean"), book_mean=("book_return","mean"), n=("coin_return","count"))
        dd["yr"] = pd.to_datetime(dd["day"]).dt.year
        out["year"] = dd.groupby("yr").agg(coin_mean=("coin_return","mean"), book_mean=("book_return","mean"), n=("coin_return","count"))
        bw = dd.groupby("w")["book_return"].agg(["mean","std","count"])
        out["book_by_window_summary"] = pd.Series({"win_pos": int((bw["mean"]>0).sum()), "win_neg": int((bw["mean"]<0).sum())})
    except Exception as e:
        out["days_err"] = str(e)[:100]
    try:
        bb = []
        for coin in days:
            for w, x in days[coin].items():
                x = x.reset_index(drop=True)
                r = x["coin_return"].astype(float); sd = r.std()
                cl = x["close"].astype(float)
                bb.append(pd.DataFrame({"zr": r/sd, "nxt": r.shift(-1)/sd, "nxt7": (cl.shift(-7)/cl-1)}))
        bb = pd.concat(bb).dropna()
        bb["b"] = pd.cut(bb.zr, [-99,-2,-1,0,1,2,99]).astype(str)
        out["after_daily_move"] = bb.groupby("b").agg(nxt=("nxt","mean"), nxt7=("nxt7","mean"), n=("nxt","count"))
    except Exception as e:
        out["move_err"] = str(e)[:100]
    try:
        tr = pd.concat([x.assign(coin=c_) for c_ in data["trades"] for x in data["trades"][c_].values() if len(x)])
        tr["d"] = tr["duration_minutes"]/1440
        out["trades"] = pd.Series({"n": len(tr), "mean_net": tr.net_profit_loss_percent.mean(),
            "median_net": tr.net_profit_loss_percent.median(), "share_win": (tr.net_profit_loss_percent>0).mean(),
            "mean_days": tr.d.mean(), "rho_absfc_net": stats.spearmanr(tr.entry_forecast.abs(), tr.net_profit_loss_percent)[0]})
        out["trades_by_coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["mean","count"])
    except Exception as e:
        out["trades_err"] = str(e)[:100]
    return out
