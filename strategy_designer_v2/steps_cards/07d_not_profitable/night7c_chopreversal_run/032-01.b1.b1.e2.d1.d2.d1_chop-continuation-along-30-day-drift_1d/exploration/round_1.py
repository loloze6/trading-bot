def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # ---- book daily returns, chained in window order
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = sorted({w for c in coins for w in days[c]}, key=lambda s:int(s[1:]))
    rows=[]
    for w in wins:
        frames=[]
        for c in coins:
            if w in days[c]:
                d=days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c; frames.append(d)
        f=pd.concat(frames)
        g=f.groupby("day")[["book_return","coin_return"]].mean().reset_index()
        g["win"]=w; rows.append(g)
    B=pd.concat(rows).dropna().reset_index(drop=True)
    v=(1+B.book_return).cumprod(); peak=v.cummax(); dd=v/peak-1
    B["dd"]=dd
    i_tr=dd.idxmin(); i_pk=v[:i_tr+1].idxmax()
    out["deepest fall"]=pd.Series({"depth":dd.min(),"peak_win":B.win[i_pk],"trough_win":B.win[i_tr],"days":i_tr-i_pk,
        "coin chain over fall":(1+B.coin_return[i_pk+1:i_tr+1]).prod()-1})
    # top falls episodes: per window max dd
    out["per window"]=B.groupby("win").agg(book=("book_return","sum"),coin=("coin_return","sum"),mindd=("dd","min")).reindex(wins)
    # ---- per-bar features and pnl
    recs=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b.close
            r1=cl.pct_change()
            ret7=cl/cl.shift(7)-1; ret30=cl/cl.shift(30)-1
            er=(cl-cl.shift(30)).abs()/cl.diff().abs().rolling(30).sum()
            vol=r1.rolling(30).std()
            vol_long=r1.rolling(90,min_periods=60).std()
            fwd1=cl.shift(-1)/cl-1
            fwd7=cl.shift(-7)/cl-1
            pos=b.postRebalance_current_allocation
            d=pd.DataFrame({"coin":c,"win":w,"pos":pos,"pnl":pos*fwd1,"fc":b.forecast,"ret7":ret7,"ret30":ret30,"er":er,
                "scaled":ret7/(vol*np.sqrt(7)),"vr":vol/vol_long,"fwd7":fwd7,"idx":np.arange(len(b)),
                "r30s":ret30/(vol*np.sqrt(30)),"year":pd.to_datetime(b.timestamp).dt.year})
            recs.append(d)
    D=pd.concat(recs,ignore_index=True)
    D["side"]=np.sign(D.pos)
    out["pnl by side"]=D.groupby("side").pnl.agg(["count","mean","sum"])
    out["pnl by year x side"]=D[D.side!=0].groupby(["year","side"]).pnl.agg(["count","mean","sum"])
    H=D[D.side!=0].copy()
    H["absfc_q"]=pd.qcut(H.fc.abs(),4,labels=False,duplicates="drop")
    out["pnl by |fc| quartile"]=H.groupby("absfc_q").pnl.agg(["count","mean","sum","std"])
    H["vr_q"]=pd.qcut(H.vr,4,labels=False)
    out["pnl by vol ratio q"]=H.groupby("vr_q").pnl.agg(["count","mean","sum","std"])
    H["r30_q"]=pd.qcut(H.r30s.abs(),4,labels=False)
    out["pnl by |ret30 scaled| q"]=H.groupby("r30_q").pnl.agg(["count","mean","sum","std"])
    H["er_q"]=pd.qcut(H.er,4,labels=False)
    out["pnl by er q"]=H.groupby("er_q").pnl.agg(["count","mean","sum","std"])
    # grid cases: signal vs no-signal by feature
    G=D[(D.idx%7==0)].dropna(subset=["fwd7","ret7","ret30","er"]).copy()
    drift=G.groupby("coin").fwd7.mean(); G["un"]=G.fwd7-G.coin.map(drift)
    G["s"]=np.sign(G.ret7)*G.un
    G["sig"]=(G.er<0.3)&(np.sign(G.ret7)==np.sign(G.ret30))
    G["vr_q"]=pd.qcut(G.vr,3,labels=False)
    out["grid signed move sig x vr tercile"]=G.groupby(["sig","vr_q"]).s.agg(["count","mean","std"])
    G["side7"]=np.sign(G.ret7)
    out["grid signed move sig x side"]=G.groupby(["sig","side7"]).s.agg(["count","mean","std"])
    return out
