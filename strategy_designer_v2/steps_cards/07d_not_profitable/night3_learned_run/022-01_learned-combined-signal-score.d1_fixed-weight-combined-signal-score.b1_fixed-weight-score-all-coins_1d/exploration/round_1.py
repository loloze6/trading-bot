def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; grid = []; dayrows = []
    comps = ["mom28","rev1","high90","vol30"]
    for coin, wins in data["bars"].items():
        # drift per coin over 5 bars on grid
        r5_all = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c)-5, 5)
            r5_all += list(c[idx+5]/c[idx]-1)
        drift5 = np.mean(r5_all) if r5_all else 0
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            nxt = np.r_[c[1:]/c[:-1]-1, np.nan]
            a = b["postRebalance_current_allocation"].values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            rows.append(pd.DataFrame({"coin":coin,"w":w,"yr":yr,"a":a,"fc":b["forecast"].values,"nxt":nxt,"gain":a*nxt}))
            idx = np.arange(0, len(c)-5, 5)
            g = pd.DataFrame({"coin":coin,"w":w,"yr":yr[idx],"fc":b["forecast"].values[idx],
                              "a":a[idx],"ex5":c[idx+5]/c[idx]-1-drift5})
            for k in comps:
                col = f"debug_info.components.{k}.post_pipeline_value"
                g[k] = b[col].values[idx] if col in b else np.nan
            grid.append(g)
        for w, d in data["days"][coin].items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=coin; dd["w"]=w
            dd["yr"]=pd.to_datetime(dd["day"]).dt.year
            dayrows.append(dd)
    B = pd.concat(rows); G = pd.concat(grid); D = pd.concat(dayrows).dropna()
    out["alloc"] = pd.Series({"mean_abs_alloc":B.a.abs().mean(),"mean_alloc":B.a.mean(),
        "share_long":(B.a>0).mean(),"share_short":(B.a<0).mean(),"mean_abs_fc":B.fc.abs().mean(),
        "gross_gain_per_bar":B.gain.mean(),"gain_long_bars":B.gain[B.a>0].mean(),"gain_short_bars":B.gain[B.a<0].mean(),
        "mean_coin_ret":B.nxt.mean()})
    Dm = D.groupby("day").agg(book=("book_return","mean"),coin=("coin_return","mean"))
    Dc = D.copy()
    out["book_days"] = pd.Series({"book_mean_daily":Dm.book.mean(),"hold_mean_daily":Dm.coin.mean(),
        "percoin_book_mean":D.book_return.mean(),"n_days":len(Dm)})
    out["by_year"] = D.groupby("yr").agg(book=("book_return","mean"),hold=("coin_return","mean"),n=("book_return","size"))
    out["by_coin"] = D.groupby("coin").agg(book=("book_return","mean"),hold=("coin_return","mean"))
    G = G.dropna(subset=["ex5"])
    G["q"] = pd.qcut(G.fc, 5, labels=False, duplicates="drop")
    out["by_fc_quintile"] = G.groupby("q").agg(fc=("fc","mean"),a=("a","mean"),ex5=("ex5","mean"),n=("ex5","size"))
    res = {}
    for k in comps:
        x = G[[k,"ex5"]].dropna()
        if len(x)>30:
            p = x[k]*x["ex5"]
            res[k] = {"corr":x[k].corr(x.ex5),"t_prod":p.mean()/(p.std()/np.sqrt(len(p))),"n":len(x),
                      "mean_abs":x[k].abs().mean()}
    out["components"] = pd.DataFrame(res).T
    out["comp_corr"] = G[comps].corr()
    # trades
    T = pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values() if len(t)])
    out["trades"] = T.groupby("side").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),
        net=("net_profit_loss_percent","mean"),dur_days=("duration_minutes",lambda x:(x/1440).mean()))
    return out
