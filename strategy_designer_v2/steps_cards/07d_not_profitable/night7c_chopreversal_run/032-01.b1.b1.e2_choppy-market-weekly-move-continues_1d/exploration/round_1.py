def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []      # grid cases
    dayrows = []   # daily book rows
    for coin, wins in data["bars"].items():
        # drift: mean 7-bar return on grid over all windows
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - 7, 7):
                allr.append(c[i+7]/c[i]-1)
        drift = np.mean(allr)
        sd7 = np.std(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            # efficiency ratio 30
            er = (c - c.shift(30)).abs() / r1.abs().mul(c.shift(1)).rolling(30).sum()
            er2 = (c - c.shift(30)).abs() / (c.diff().abs().rolling(30).sum())
            vol = r1.rolling(30).std()
            sc = (c/c.shift(7)-1)/(vol*np.sqrt(7))
            ret30 = c/c.shift(30)-1
            f = b["forecast"].fillna(0)
            alloc = b["postRebalance_current_allocation"].fillna(0)
            for i in range(0, len(c)-7, 7):
                rows.append(dict(coin=coin, w=w, er=er2.iloc[i], sc=sc.iloc[i], f=f.iloc[i],
                                 fwd=c.iloc[i+7]/c.iloc[i]-1-drift, sd7=sd7, alloc=alloc.iloc[i],
                                 vol=vol.iloc[i], ret30=ret30.iloc[i], regime=b["regime"].iloc[i]))
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"] = coin; d["w"] = w
            dayrows.append(d)
    g = pd.DataFrame(rows)
    D = pd.concat(dayrows)
    # book by side: allocation at day end
    for coin, wins in data["bars"].items():
        pass
    # per-bar position gain by side
    pr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            a = b["postRebalance_current_allocation"].fillna(0)
            nr = b["close"].shift(-1)/b["close"]-1
            v = b["postRebalance_total_value"]
            fee = (b["total_portfolio_value"] - v)/b["total_portfolio_value"]
            pr.append(pd.DataFrame(dict(coin=coin, w=w, a=a, gain=a*nr, fee=fee, regime=b["regime"],
                                        f=b["forecast"].fillna(0), nr=nr)))
    P = pd.concat(pr).dropna(subset=["gain"])
    P["side"] = np.sign(P["a"])
    out["gain_by_side"] = P.groupby("side").agg(n=("gain","size"), mean_gain=("gain","mean"), fee=("fee","mean"), mean_abs_a=("a",lambda x: x.abs().mean()))
    out["gain_by_regime"] = P.groupby("regime").agg(n=("gain","size"), mean_gain=("gain","mean"), fee=("fee","mean"), held=("a",lambda x:(x!=0).mean()))
    out["total_fee_per_bar"] = float(P["fee"].mean())
    out["gross_gain_per_bar"] = float(P["gain"].mean())
    # cases in choppy grid
    ch = g[(g.f != 0)].copy()
    ch["dir"] = np.sign(ch["f"])
    ch["um"] = ch["fwd"]*ch["dir"]
    ch["q"] = pd.qcut(ch["f"].abs(), 5, labels=False)
    out["unusual_by_absF_quintile"] = ch.groupby("q").agg(n=("um","size"), mean=("um","mean"), t=("um", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    out["unusual_by_side"] = ch.groupby("dir").agg(n=("um","size"), mean=("um","mean"), t=("um", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    ch["erq"] = pd.qcut(ch["er"], 4, labels=False)
    out["unusual_by_er_quartile"] = ch.groupby("erq").agg(n=("um","size"), er=("er","mean"), mean=("um","mean"), t=("um", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    ch["volq"] = pd.qcut(ch["vol"], 4, labels=False)
    out["unusual_by_vol_quartile"] = ch.groupby("volq").agg(n=("um","size"), vol=("vol","mean"), mean=("um","mean"), t=("um", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    ch["scq"] = pd.qcut(ch["sc"].abs(), 5, labels=False)
    out["unusual_by_abs_rawscaled"] = ch.groupby("scq").agg(n=("um","size"), sc=("sc",lambda x:x.abs().mean()), mean=("um","mean"), t=("um", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    # sign agreement raw vs forecast
    out["share_f_sign_eq_raw_sign"] = float((np.sign(ch["f"])==np.sign(ch["sc"])).mean())
    # by sign of raw scaled vs side, using raw sign
    ch["rdir"] = np.sign(ch["sc"])
    ch["umr"] = ch["fwd"]*ch["rdir"]
    out["unusual_by_raw_side"] = ch.groupby("rdir").agg(n=("umr","size"), mean=("umr","mean"), t=("umr", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    # book daily: worst windows
    D2 = D.dropna(subset=["book_return"])
    bk = D2.groupby(["w","day"]).agg(b=("book_return","mean"), h=("coin_return","mean")).reset_index()
    out["by_window"] = bk.groupby("w").agg(book_mean=("b","mean"), hold_mean=("h","mean"), book_sd=("b","std"), hold_sd=("h","std"))
    return out
