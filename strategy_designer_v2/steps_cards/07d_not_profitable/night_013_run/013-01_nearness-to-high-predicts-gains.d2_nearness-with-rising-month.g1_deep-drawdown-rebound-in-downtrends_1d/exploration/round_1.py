import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    days = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            x = d[["day","book_return","coin_return"]].copy(); x["coin"]=c; x["w"]=w
            days.append(x)
    D = pd.concat(days)
    P = D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    P["wn"] = P["w"].str[1:].astype(int)
    P = P.sort_values(["wn","day"]).dropna()
    out["per_window"] = P.groupby("wn").agg(book_mean=("book_return","mean"), coin_mean=("coin_return","mean"), n=("book_return","size"))
    # book chain and drawdown
    v = (1+P["book_return"]).cumprod().values
    dd = v/np.maximum.accumulate(v)-1
    P["dd"]=dd
    out["max_dd"] = float(dd.min())
    i = int(np.argmin(dd)); peak = int(np.argmax(v[:i+1]))
    out["dd_peak_trough_windows"] = f"{P['wn'].iloc[peak]}->{P['wn'].iloc[i]}, days {i-peak}"
    out["book_coin_corr"] = float(P[["book_return","coin_return"]].corr().iloc[0,1])
    # bar-level analysis
    rows=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r30 = cl/cl.shift(30)-1
            hi60 = cl.rolling(60,min_periods=20).max()
            depth = cl/hi60-1
            r7p = cl/cl.shift(7)-1
            r90 = cl/cl.shift(90)-1
            fwd7 = cl.shift(-7)/cl-1
            fwd1 = cl.shift(-1)/cl-1
            alloc = b["postRebalance_current_allocation"]
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            df = pd.DataFrame(dict(coin=c,w=w,pos=np.arange(len(b)),r30=r30,depth=depth,r7p=r7p,r90=r90,
                                   fwd7=fwd7,fwd1=fwd1,alloc=alloc,fc=b["forecast"],fee=fee,regime=b["regime"],
                                   vol=b["sizing_realised_vol"]))
            rows.append(df)
    B = pd.concat(rows)
    cm = B[B.pos%7==0].groupby("coin")["fwd7"].mean()
    B["ex7"] = B["fwd7"]-B["coin"].map(cm)
    B["gain"] = B["alloc"]*B["fwd1"]
    out["gain_mean_per_bar"] = float(B["gain"].mean())
    out["fee_mean_per_bar"] = float(B["fee"].mean())
    out["share_bars_long"] = float((B["alloc"]>0.01).mean())
    G = B[(B.pos%7==0)&B.fwd7.notna()&(B.regime=="mean_reversion")].copy()
    G["fc_t"] = pd.qcut(G["fc"].rank(method="first"),3,labels=["lo","mid","hi"])
    out["ex7_by_fc_tercile"] = G.groupby("fc_t")["ex7"].agg(["mean","count"])
    G["dep_t"] = pd.qcut(G["depth"].rank(method="first"),3,labels=["deep","mid","shallow"])
    out["ex7_by_depth_tercile"] = G.groupby("dep_t")["ex7"].agg(["mean","count"])
    G["r7_t"] = pd.qcut(G["r7p"].rank(method="first"),3,labels=["fall","mid","rise"])
    G["r90_t"] = pd.qcut(G["r90"].rank(method="first"),3,labels=["bear","mid","bull"])
    out["ex7_by_r90_depth"] = G.groupby(["r90_t","dep_t"])["ex7"].mean().unstack()
    out["ex7_by_r7_depth"] = G.groupby(["r7_t","dep_t"])["ex7"].mean().unstack()
    # all grid bars, non-regime
    A = B[(B.pos%7==0)&B.fwd7.notna()].copy()
    A["inreg"]=A.r30<0
    out["ex7_inreg_vs_not"] = A.groupby("inreg")["ex7"].agg(["mean","count"])
    A["dep_t"] = pd.qcut(A["depth"].rank(method="first"),4,labels=["q1deep","q2","q3","q4near"])
    out["ex7_all_by_depth_regime"] = A.groupby(["inreg","dep_t"])["ex7"].mean().unstack()
    out["corr_depth_ex7_by_r90t"] = G.groupby("r90_t").apply(lambda g: pd.Series(stats.pearsonr(g.depth,g.ex7)[0:2],index=["r","p"]))
    # gain by r90 state at bar level
    B["r90_t"]=pd.qcut(B["r90"],3,labels=["bear","mid","bull"])
    out["gain_by_r90"] = B[B.alloc>0.01].groupby("r90_t")[["gain","fwd1"]].mean()
    return out
