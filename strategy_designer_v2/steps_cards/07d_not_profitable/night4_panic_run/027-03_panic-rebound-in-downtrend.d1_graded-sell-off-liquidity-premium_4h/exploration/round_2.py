import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    G = []; Bd = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; rng = (b["high"]-b["low"])/cl
            r6 = cl/cl.shift(6)-1
            z = r6/ r6.abs().rolling(180).mean()
            rr = rng.rolling(6).mean()/rng.rolling(180).mean()
            r180 = cl/cl.shift(180)-1
            r540 = cl/cl.shift(540)-1
            ma540 = cl/cl.rolling(540).mean()-1
            f84 = cl.shift(-84)/cl-1
            df = pd.DataFrame({"coin":c,"w":w,"z":z,"rr":rr,"r180":r180,"r540":r540,"ma540":ma540,"f84":f84,
                               "al":b["postRebalance_current_allocation"]})
            G.append(df.iloc[::84])
            # daily book view
            ts = pd.to_datetime(b["timestamp"]); day = ts.dt.floor("D")
            v = b["postRebalance_total_value"]
            dd = pd.DataFrame({"day":day,"v":v,"cl":cl,"al":df["al"],"ma540":ma540,"r180":r180,"rr":rr}).groupby("day").last()
            dd["br"] = dd["v"].pct_change(); dd["cr"] = dd["cl"].pct_change()
            for k in ["al","ma540","r180","rr"]: dd[k+"_prev"] = dd[k].shift(1)
            dd["coin"]=c; dd["w"]=w
            Bd.append(dd)
    G = pd.concat(G)
    drift = G.groupby("coin")["f84"].transform("mean")
    G["ex"] = G["f84"]-drift
    G = G.dropna(subset=["ex","z","rr"])
    def summ(x):
        return pd.Series({"n":len(x),"ex_mean":x["ex"].mean(),"t":x["ex"].mean()/(x["ex"].std()/np.sqrt(len(x))) if len(x)>2 else np.nan,
                          "f84":x["f84"].mean()})
    out["grid_all"] = summ(G).round(4)
    S = G[(G["z"]<0)&(G["rr"]>1)].copy()
    S["sev"] = -S["z"]*S["rr"]
    out["situation_by_severity"] = S.groupby(pd.qcut(S["sev"],5),observed=True).apply(summ).round(4)
    S2 = S.dropna(subset=["ma540"])
    out["situation_by_price_vs_90d_mean"] = S2.groupby(pd.qcut(S2["ma540"],5),observed=True).apply(summ).round(4)
    G2 = G.dropna(subset=["ma540"])
    out["all_grid_by_price_vs_90d_mean"] = G2.groupby(pd.qcut(G2["ma540"],5),observed=True).apply(summ).round(4)
    out["situation_by_r180"] = S.dropna(subset=["r180"]).pipe(lambda s: s.groupby(pd.qcut(s["r180"],5),observed=True).apply(summ)).round(4)
    # daily book: where are losses
    B = pd.concat(Bd).dropna(subset=["br","ma540_prev"])
    B["below"] = B["ma540_prev"]<0
    out["daily_by_price_vs_90d"] = B.groupby(pd.qcut(B["ma540_prev"],5),observed=True).agg(
        n=("br","size"),book=("br","mean"),coin=("cr","mean"),book_sd=("br","std"),al=("al_prev","mean")).round(5)
    out["daily_by_rr"] = B.dropna(subset=["rr_prev"]).pipe(lambda s:s.groupby(pd.qcut(s["rr_prev"],5),observed=True).agg(
        n=("br","size"),book=("br","mean"),coin=("cr","mean"),book_sd=("br","std"),al=("al_prev","mean"))).round(5)
    # worst 5% book days per coin: conditions
    q = B["br"].quantile(0.05)
    W = B[B["br"]<=q]
    out["worst_days_conditions"] = pd.DataFrame({"worst":W[["al_prev","ma540_prev","r180_prev","rr_prev"]].median(),
                                                 "all":B[["al_prev","ma540_prev","r180_prev","rr_prev"]].median()}).round(4)
    out["worst_days_share_below90d"] = float(W["below"].mean())
    out["all_days_share_below90d"] = float(B["below"].mean())
    return out
