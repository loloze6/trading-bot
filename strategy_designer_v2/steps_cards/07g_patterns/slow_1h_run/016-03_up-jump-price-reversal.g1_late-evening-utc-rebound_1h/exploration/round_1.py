def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    out = {}
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            b["hour"] = ts.dt.hour.values
            b["wd"] = ts.dt.weekday.values
            cl = b["close"].values
            b["r1"] = np.r_[cl[1:]/cl[:-1]-1, np.nan]
            b["r2"] = pd.Series(cl).shift(-2).values/cl-1
            b["r24f"] = pd.Series(cl).shift(-24).values/cl-1
            b["p24"] = cl/pd.Series(cl).shift(24).values-1
            lr = np.log(pd.Series(cl)).diff()
            b["vol24"] = lr.rolling(24).std().values
            b["maxabs24"] = lr.abs().rolling(24).max().values
            b["absum24"] = lr.abs().rolling(24).sum().values
            b["pos"] = np.arange(len(b))
            b["gain"] = b["postRebalance_current_allocation"].values*b["r1"]
            b["coin"] = c; b["w"] = w
            rows.append(b[["coin","w","hour","wd","r1","r2","r24f","p24","vol24","maxabs24","absum24","pos","gain","forecast","postRebalance_current_allocation","total_portfolio_value","postRebalance_total_value"]])
    A = pd.concat(rows, ignore_index=True)
    # hourly return by hour (all bars, 1-bar returns non overlapping)
    g = A.groupby("hour")["r1"]
    out["r1_by_hour_bps"] = pd.DataFrame({"mean_bps": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()})
    # position gain and fee by hour
    A["fee"] = (A["total_portfolio_value"]-A["postRebalance_total_value"])/A["total_portfolio_value"]
    gh = A.groupby("hour").agg(gain_bps=("gain", lambda x: x.mean()*1e4), fee_bps=("fee", lambda x: x.mean()*1e4), alloc=("postRebalance_current_allocation","mean"))
    out["gain_fee_by_hour"] = gh[(gh.alloc.abs()>1e-6)|(gh.fee_bps.abs()>1e-4)]
    out["total_gain_vs_fee_bps_per_bar"] = f"gain {A.gain.mean()*1e4:.4f}, fee {A.fee.mean()*1e4:.4f}"
    # decision bars hour 19: r2 by quintile of p24, per coin
    D = A[A.hour==19].dropna(subset=["p24","r2"]).copy()
    D["q"] = D.groupby("coin")["p24"].transform(lambda x: pd.qcut(x,5,labels=False))
    gq = D.groupby("q")["r2"]
    out["h19_r2_by_p24_quintile"] = pd.DataFrame({"bps": gq.mean()*1e4, "t": gq.mean()/(gq.std()/np.sqrt(gq.count())), "n": gq.count()})
    # same at all hours: r2 by p24 quintile vs hour, correlation (non-overlapping even positions)
    E = A[(A.pos%2==0)].dropna(subset=["p24","r2"])
    res = []
    for h, x in E.groupby("hour"):
        r, p = stats.spearmanr(x.p24, x.r2); res.append((h, r, len(x)))
    out["spearman_p24_r2_by_hour_evenpos"] = pd.DataFrame(res, columns=["hour","rho","n"]).set_index("hour")
    # 24h horizon: p24 vs r24f, grid every 24 bars, by jumpiness
    G = A[A.pos%24==0].dropna(subset=["p24","r24f","maxabs24","absum24"]).copy()
    G["jump"] = G.maxabs24/G.absum24
    G["jq"] = pd.qcut(G.jump,3,labels=False)
    res=[]
    for jq,x in G.groupby("jq"):
        sl = stats.linregress(x.p24, x.r24f); res.append((jq, sl.slope, sl.slope/sl.stderr, len(x)))
    out["slope_r24f_on_p24_by_jumpiness_tercile"] = pd.DataFrame(res, columns=["jq","slope","t","n"])
    # by vol level hourly
    A2 = A.dropna(subset=["vol24","r1"]).copy()
    A2["vq"] = A2.groupby("coin")["vol24"].transform(lambda x: pd.qcut(x,5,labels=False))
    gv = A2.groupby("vq")["r1"]
    out["r1_by_vol_quintile"] = pd.DataFrame({"bps": gv.mean()*1e4, "t": gv.mean()/(gv.std()/np.sqrt(gv.count()))})
    # weekday daily
    dd = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["wd"] = pd.to_datetime(d["day"]).dt.weekday; d["coin"]=c; dd.append(d)
    DD = pd.concat(dd)
    gw = DD.groupby("wd")
    out["daily_by_weekday_bps"] = pd.DataFrame({"coin": gw.coin_return.mean()*1e4, "book": gw.book_return.mean()*1e4, "t_coin": gw.coin_return.mean()/(gw.coin_return.std()/np.sqrt(gw.coin_return.count()))})
    # trades
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values()])
    out["trades"] = T.groupby("coin").agg(n=("side","size"), pl=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), dur=("duration_minutes","median"))
    return out
