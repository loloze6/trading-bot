import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r30 = cl/cl.shift(30)-1
            hi60 = cl.rolling(60,min_periods=20).max()
            depth = cl/hi60-1
            r90 = cl/cl.shift(90)-1
            fwd7 = cl.shift(-7)/cl-1
            fwd1 = cl.shift(-1)/cl-1
            alloc = b["postRebalance_current_allocation"]
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            rows.append(pd.DataFrame(dict(coin=c,w=w,pos=np.arange(len(b)),r30=r30,depth=depth,r90=r90,
                        fwd7=fwd7,fwd1=fwd1,alloc=alloc,fc=b["forecast"],fee=fee,regime=b["regime"])))
    B = pd.concat(rows)
    cm = B[B.pos%7==0].groupby("coin")["fwd7"].mean()
    B["ex7"] = B["fwd7"]-B["coin"].map(cm)
    G = B[(B.pos%7==0)&B.fwd7.notna()&(B.regime=="mean_reversion")].dropna(subset=["depth","ex7"]).copy()
    def slope_t(x,y):
        r = stats.linregress(x,y); return pd.Series(dict(slope=r.slope,t=r.slope/r.stderr,n=len(x)))
    res = {}
    res["fc_all"] = slope_t(G.fc,G.ex7)
    res["negdepth_all"] = slope_t(-G.depth,G.ex7)
    Gb = G[G.r90<0]; Gu = G[G.r90>=0]
    res["negdepth_r90neg"] = slope_t(-Gb.depth,Gb.ex7)
    res["negdepth_r90pos"] = slope_t(-Gu.depth,Gu.ex7)
    res["fc_r90neg"] = slope_t(Gb.fc,Gb.ex7)
    res["fc_r90pos"] = slope_t(Gu.fc,Gu.ex7)
    out["slopes"] = pd.DataFrame(res).T
    out["corr_fc_negdepth"] = float(np.corrcoef(G.fc,-G.depth)[0,1])
    out["ex7_by_r90sign"] = G.groupby(G.r90<0)["ex7"].agg(["mean","count"])
    # bar-level gains by r90 sign while long
    L = B[B.alloc>0.01].copy()
    L["gain"]=L.alloc*L.fwd1
    L["r90neg"]=L.r90<0
    out["gain_by_r90sign"] = L.groupby("r90neg").agg(gain=("gain","mean"),fee=("fee","mean"),n=("gain","size"),alloc=("alloc","mean"))
    # per window: share of long bars with r90>=0 and window gain
    L["wn"]=L.w.str[1:].astype(int)
    out["gain_by_r90sign_per_year_bucket"] = L.groupby([pd.cut(L.wn,[0,6,12,18,24]),"r90neg"])["gain"].sum().unstack()
    # hypothetical: position = -depth scaled, only r90<0 & r30<0, daily mean
    H = B.dropna(subset=["depth","fwd1","r30","r90"]).copy()
    H["hpos"] = np.where((H.r30<0)&(H.r90<0), -H.depth/0.3, 0.0).clip(0,2)
    H["hg"]=H.hpos*H.fwd1
    H["actual"]=H.alloc*H.fwd1
    out["hyp_vs_actual_bar"] = pd.Series(dict(hyp_mean=H.hg.mean(), hyp_sd=H.hg.std(), act_mean=H.actual.mean(), act_sd=H.actual.std(),
                                              hyp_share_in=(H.hpos>0).mean(), hold_mean=H.fwd1.mean()))
    return out
