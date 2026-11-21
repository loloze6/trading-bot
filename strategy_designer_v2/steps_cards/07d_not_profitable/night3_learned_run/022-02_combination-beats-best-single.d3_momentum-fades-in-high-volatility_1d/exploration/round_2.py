def explore(data):
    import numpy as np, pandas as pd
    out={}
    rows=[]
    for coin, ws in data["bars"].items():
        fw=[]
        for w,b in ws.items():
            c=b["close"].reset_index(drop=True)
            fw.append((c.shift(-20)/c-1).iloc[::20].dropna())
        drift=pd.concat(fw).mean(); usual=pd.concat(fw).std()
        for w,b in ws.items():
            b=b.reset_index(drop=True); c=b["close"]; r1=c.pct_change()
            v30=r1.rolling(30).std()
            df=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(b)),
              "r28":c/c.shift(28)-1,"r90":c/c.shift(90)-1,"r5":c/c.shift(5)-1,
              "near":c/c.rolling(60).max()-1,"v30":v30,
              "x":(c.shift(-20)/c-1-drift),"xz":(c.shift(-20)/c-1-drift)/usual,
              "pos":b["postRebalance_current_allocation"],"fc":b["forecast"]})
            rows.append(df)
    d=pd.concat(rows)
    g=d[d.i%20==0].dropna(subset=["x"])
    def sig(col):
        h=g.dropna(subset=[col]).copy()
        s=np.sign(h[col]-h.groupby("coin")[col].transform("median"))
        p=s*h.x
        return pd.Series({"n":len(p),"mean":p.mean(),"t":p.mean()/p.std()*np.sqrt(len(p))})
    out["signed_20d_unusual_by_situation"]=pd.DataFrame({c:sig(c) for c in ["r28","r90","r5","near","v30"]}).T
    h=g.dropna(subset=["r28"]).copy()
    h["side"]=np.where(h.r28>0,"after_rise","after_fall")
    h["sx"]=np.sign(h.r28)*h.x
    out["momentum_by_side"]=h.groupby("side").agg(n=("sx","size"),mean=("sx","mean"),raw_fwd=("x","mean"))
    # book: long vs short days
    b=d.copy(); b["nxt"]=b.groupby(["coin","w"])["r28"].transform(lambda s:s)
    gains=[]
    for coin,ws in data["bars"].items():
        for w,bb in ws.items():
            bb=bb.reset_index(drop=True)
            r=bb["close"].shift(-1)/bb["close"]-1
            gp=bb["postRebalance_current_allocation"]*r
            gains.append(pd.DataFrame({"gp":gp,"pos":bb["postRebalance_current_allocation"]}))
    G=pd.concat(gains).dropna()
    G["side"]=np.where(G.pos>0.01,"long",np.where(G.pos<-0.01,"short","flat"))
    out["bar_gain_by_side"]=G.groupby("side").agg(n=("gp","size"),mean_gain=("gp","mean"),sum_gain=("gp","sum"),mean_abs_pos=("pos",lambda x:x.abs().mean()))
    # trades
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()])
    out["trades_by_side"]=T.groupby("side").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda x:(x>0).mean()))
    # drawdown of pooled book (chain daily mean in window order)
    D=pd.concat([dd.assign(coin=c,w=w) for c,ws in data["days"].items() for w,dd in ws.items()])
    D["wn"]=D.w.str[1:].astype(int)
    m=D.groupby(["wn","day"]).book_return.mean().reset_index().sort_values(["wn","day"])
    eq=(1+m.book_return.fillna(0)).cumprod(); dd=eq/eq.cummax()-1
    m["dd"]=dd.values
    out["deepest_fall_by_window"]=m.groupby("wn").agg(book_mean=("book_return","mean"),min_dd=("dd","min")).sort_values("min_dd").head(8)
    return out
