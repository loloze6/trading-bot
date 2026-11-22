def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []; grid = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            r1 = cl.shift(-1)/cl - 1
            pos = b["postRebalance_current_allocation"].astype(float)
            hi = cl.rolling(30, min_periods=30).max(); lo = cl.rolling(30, min_periods=30).min()
            rp = (cl-lo)/(hi-lo) - 0.5
            ret30 = cl/cl.shift(30)-1
            ret90 = cl/cl.shift(90)-1
            vol = cl.pct_change().rolling(30, min_periods=20).std()
            fwd10 = cl.shift(-10)/cl - 1
            df = pd.DataFrame({"coin":c,"wi":int(w[1:]),"gain":pos*r1,"pos":pos,"fc":b["forecast"].astype(float),
                               "rp":rp,"ret30":ret30,"ret90":ret90,"vol":vol,"fwd10":fwd10})
            rows.append(df); grid.append(df.iloc[::10])
    A = pd.concat(rows); G = pd.concat(grid).dropna(subset=["fwd10","fc"])
    G["ex"] = G["fwd10"] - G.groupby("coin")["fwd10"].transform("mean")
    A["side"] = np.sign(A["pos"])
    F = A[A.wi.isin([19,20,21])]
    out["fall windows w19-w21 gain by coin x side"] = F.groupby(["coin","side"])["gain"].sum().unstack()
    out["fall windows mean ret30, vol, side share"] = F.groupby("wi").agg(ret30=("ret30","mean"),vol=("vol","mean"),long_share=("side",lambda s:(s>0).mean()),gain=("gain","sum"))
    G["fc_b"] = pd.cut(G["fc"], [-21,-15,-8,0,8,15,21])
    G["r90s"] = np.where(G["ret90"]>0,"up90","down90")
    out["ex by fc bucket x 90d trend sign"] = G.groupby(["fc_b","r90s"])["ex"].agg(["count","mean"]).unstack()
    G["vol_q"] = pd.qcut(G["vol"],3,labels=["lowvol","mid","highvol"])
    out["ex by fc bucket x vol"] = G.groupby(["fc_b","vol_q"])["ex"].mean().unstack()
    A["fc_b"] = pd.cut(A["fc"], [-21,-15,-8,0,8,15,21])
    out["bar gain by fc bucket"] = A.groupby("fc_b")["gain"].agg(["count","mean","sum"])
    out["bar gain by vol x side"] = A.assign(vq=pd.qcut(A["vol"],3,labels=["lowvol","mid","highvol"])).groupby(["vq","side"])["gain"].agg(["count","mean","sum"]).unstack()
    # long-only from fc>0 graded: slope of ex on fc in fc>0 vs fc<0
    for nm, g in [("fc>0",G[G.fc>0]),("fc<0",G[G.fc<0])]:
        s = stats.linregress(g["fc"], g["ex"]); out["slope "+nm] = pd.Series({"n":len(g),"slope":s.slope,"t":s.slope/s.stderr})
    return out
