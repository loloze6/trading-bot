def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            nxt = c.shift(-1)/c - 1
            pos = b["postRebalance_current_allocation"].fillna(0)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            z = r1/vol20
            ret20 = c/c.shift(20)-1
            ret5 = c/c.shift(5)-1
            ret60 = c/c.shift(60)-1
            volrat = vol20/ r1.rolling(60).std()
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            df = pd.DataFrame({"coin":coin,"w":w,"pos":pos,"nxt":nxt,"z":z,"ret20":ret20,"ret5":ret5,"ret60":ret60,
                               "volrat":volrat,"fee":fee,"fc":b["forecast"],"wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                               "year":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    cm = d.groupby("coin")["nxt"].mean()
    d["ex"] = d["nxt"] - d["coin"].map(cm)
    d["g"] = d["pos"]*d["nxt"]
    d["gex"] = d["pos"]*d["ex"]
    act = d[d["pos"]>0].copy()
    out["overall"] = pd.Series({"active_share":(d.pos>0).mean(),"mean_pos_active":act.pos.mean(),
        "gross_per_bar":d.g.mean(),"fee_per_bar":d.fee.mean(),"timing_per_bar":d.gex.mean(),
        "market_per_bar":(d.pos*d.coin.map(cm)).mean(),"active_nxt_mean":act.nxt.mean(),"n_active":len(act)})
    # by trend state at entry
    def grp(col, q=5):
        a = act.dropna(subset=[col]).copy()
        a["b"] = pd.qcut(a[col], q, labels=False, duplicates="drop")
        return a.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=("ex","size"),mean_ex=("ex","mean"),
                                  gain=("g","sum"),t=("ex",lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    out["by_ret20"] = grp("ret20")
    out["by_ret60"] = grp("ret60")
    out["by_ret5"] = grp("ret5")
    out["by_volrat"] = grp("volrat")
    out["by_z"] = grp("z")
    out["by_wd"] = act.groupby("wd").agg(n=("ex","size"),mean_ex=("ex","mean"),gain=("g","sum"))
    out["by_year"] = act.groupby("year").agg(n=("ex","size"),mean_ex=("ex","mean"),gain=("g","sum"))
    out["by_coin"] = act.groupby("coin").agg(n=("ex","size"),mean_ex=("ex","mean"),gain=("g","sum"),fee=("fee","sum"))
    out["fee_total_vs_gross"] = pd.Series({"sum_gross":d.g.sum(),"sum_fee":d.fee.sum()})
    # book days: drawdowns
    dd=[]
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin,w=w))
    D = pd.concat(dd)
    br = D.groupby(["w","day"])["book_return"].mean().dropna()
    cr = D.groupby(["w","day"])["coin_return"].mean().dropna()
    out["book_daily"] = pd.Series({"mean":br.mean(),"sd":br.std(),"sharpe":br.mean()/br.std()*np.sqrt(365),
                                   "hold_mean":cr.mean(),"hold_sharpe":cr.mean()/cr.std()*np.sqrt(365)})
    eq = (1+br).cumprod()
    ddn = eq/eq.cummax()-1
    out["maxdd"] = ddn.min()
    bw = br.groupby(level=0).apply(lambda x: (1+x).prod()-1)
    out["book_by_window"] = pd.DataFrame({"book":bw,"hold":cr.groupby(level=0).apply(lambda x:(1+x).prod()-1)})
    return out
