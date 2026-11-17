import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            r1 = b.close.shift(-1)/b.close-1
            al = b.postRebalance_current_allocation
            rows.append(pd.DataFrame({"coin":c,"w":w,"al":al,"g":al*r1,"r1":r1,"f":b.forecast,
                "dist":b["debug_info.components.dist_high.last_history_value"],
                "zd":b["debug_info.components.dist_high.post_pipeline_value"]}))
    B = pd.concat(rows).dropna(subset=["r1"])
    B["side"] = np.sign(B.al).map({1:"long",-1:"short",0:"flat"})
    out["by_side"] = B.groupby("side").agg(share=("g","size"),gain_mean=("g","mean"),gain_sum=("g","sum"),al=("al","mean"),r1=("r1","mean")).assign(share=lambda x:x.share/len(B)).round(5)
    out["abs_alloc_quantiles"] = B.al.abs().quantile([.1,.25,.5,.75,.9,.99]).round(4)
    out["corr_zd_dist"] = B[["zd","dist","f"]].corr().round(3)
    # raw distance graded at the top, 7d grid
    G = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            fwd = b.close.shift(-7)/b.close-1
            idx = np.arange(0,len(b),7)
            G.append(pd.DataFrame({"coin":c,"fwd":fwd.iloc[idx].values,"dist":b["debug_info.components.dist_high.last_history_value"].iloc[idx].values,
                "zd":b["debug_info.components.dist_high.post_pipeline_value"].iloc[idx].values,"f":b.forecast.iloc[idx].values}))
    G = pd.concat(G).dropna(subset=["fwd","dist"])
    G["exc"] = G.fwd - G.groupby("coin").fwd.transform("mean")
    bins = [-101,-60,-40,-25,-15,-8,-3,0.01]
    G["db"] = pd.cut(G.dist,bins)
    t = G.groupby("db",observed=True).agg(n=("exc","size"),exc=("exc","mean"),sd=("exc","std"),f=("f","mean"),zd=("zd","mean"))
    t["t"]=t.exc/(t.sd/np.sqrt(t.n)); out["raw_dist_bins"]=t.drop(columns="sd").round(4)
    # forecast sign vs raw dist near high
    G["near"] = G.dist>-15
    out["near_high_forecast_sign"] = G.groupby("near").agg(n=("f","size"),share_f_pos=("f",lambda x:(x>0).mean()),exc=("exc","mean")).round(4)
    # spearman of raw dist and zd vs exc
    out["spearman"] = pd.Series({"dist":stats.spearmanr(G.dist,G.exc)[0],"zd":stats.spearmanr(G.zd,G.exc,nan_policy="omit")[0]}).round(4)
    return out
