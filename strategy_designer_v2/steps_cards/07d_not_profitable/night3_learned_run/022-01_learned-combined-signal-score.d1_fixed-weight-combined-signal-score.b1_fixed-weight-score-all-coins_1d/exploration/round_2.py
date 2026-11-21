def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    grid = []; rows = []
    for coin, wins in data["bars"].items():
        r5_all = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c)-5, 5)
            r5_all += list(c[idx+5]/c[idx]-1)
        drift5 = np.mean(r5_all) if r5_all else 0
        r1 = []
        for w, b in wins.items():
            c = b["close"].values; r1 += list(c[1:]/c[:-1]-1)
        drift1 = np.mean(r1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            nxt = np.r_[c[1:]/c[:-1]-1, np.nan]
            a = b["postRebalance_current_allocation"].values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            rows.append(pd.DataFrame({"coin":coin,"yr":yr,"a":a,"nxt":nxt,"drift1":drift1,
                "m":b["debug_info.components.mom28.post_pipeline_value"].values}))
            idx = np.arange(0, len(c)-5, 5)
            g = pd.DataFrame({"coin":coin,"yr":yr[idx],"fc":b["forecast"].values[idx],"a":a[idx],
                "r5":c[idx+5]/c[idx]-1,"ex5":c[idx+5]/c[idx]-1-drift5,"drift5":drift5,
                "m":b["debug_info.components.mom28.post_pipeline_value"].values[idx],
                "h":b["debug_info.components.high90.post_pipeline_value"].values[idx],
                "rv":b["debug_info.components.rev1.post_pipeline_value"].values[idx],
                "v":b["debug_info.components.vol30.post_pipeline_value"].values[idx]})
            grid.append(g)
    B = pd.concat(rows).dropna(subset=["nxt"]); G = pd.concat(grid).dropna(subset=["ex5"])
    B["gain"]=B.a*B.nxt; B["mkt"]=B.a*B.drift1; B["timing"]=B.gain-B.mkt
    out["gain_split"] = pd.Series({"gain":B.gain.mean(),"from_market":B.mkt.mean(),"timing":B.timing.mean(),
        "long_bar_gain":B.gain[B.a>0].mean()*(B.a>0).mean(),"short_bar_gain":B.gain[B.a<0].mean()*(B.a<0).mean(),
        "short_market":B.mkt[B.a<0].mean()*(B.a<0).mean()})
    out["short_gain_by_year"] = B[B.a<0].groupby("yr").agg(gain=("gain","mean"),n=("gain","size"))
    G["mh"] = (G.m+G.h)/2
    G["q_mh"] = pd.qcut(G.mh,5,labels=False,duplicates="drop")
    out["mh_quintile"] = G.groupby("q_mh").agg(mh=("mh","mean"),ex5=("ex5","mean"),r5=("r5","mean"),n=("ex5","size"))
    p = G.mh/10*G.ex5; p2 = G.fc/10*G.ex5
    out["t_compare"] = pd.Series({"t_mh":p.mean()/(p.std()/np.sqrt(len(p))),"t_fc":p2.mean()/(p2.std()/np.sqrt(len(p2))),
        "n":len(G),"corr_mh_fc":G.mh.corr(G.fc),"sd_fc":G.fc.std(),"sd_mh":G.mh.std()})
    G["q_v"] = pd.qcut(G.v,5,labels=False,duplicates="drop")
    out["vol_quintile"] = G.groupby("q_v").agg(v=("v","mean"),ex5=("ex5","mean"),r5=("r5","mean"),absr5=("r5",lambda x:x.abs().mean()))
    G["neg"]=G.fc<0
    out["neg_cases"] = G.groupby("neg").agg(r5=("r5","mean"),ex5=("ex5","mean"),drift=("drift5","mean"),a=("a","mean"),n=("r5","size"))
    return out
