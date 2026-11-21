def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, ws in data["bars"].items():
        # normal drift over 20 bars, grid, all windows
        fw_all=[]
        for w, b in ws.items():
            c=b["close"].reset_index(drop=True)
            f=c.shift(-20)/c-1
            fw_all.append(f.iloc[::20].dropna())
        drift=pd.concat(fw_all).mean(); usual=pd.concat(fw_all).std()
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r1=c.pct_change()
            r28=c/c.shift(28)-1
            v30=r1.rolling(30).std()
            vexp=v30.expanding(10).mean()
            vrat=v30/vexp
            r5=c/c.shift(5)-1
            f20=c.shift(-20)/c-1
            f5=c.shift(-5)/c-1
            yr=pd.to_datetime(b["timestamp"]).dt.year
            df=pd.DataFrame({"coin":coin,"w":w,"r28z":r28/(v30*np.sqrt(28)),"r28":r28,"vrat":vrat,
                "r5z":r5/(v30*np.sqrt(5)),"x20":(f20-drift)/usual,"x20raw":f20-drift,"f5":f5,
                "fc":b["forecast"],"pos":b["postRebalance_current_allocation"],"yr":yr,"pos_i":np.arange(len(b))})
            rows.append(df)
    d=pd.concat(rows)
    g=d[(d.pos_i%20==0)].dropna(subset=["x20","r28z"])
    out={}
    g["q"]=pd.qcut(g.r28z,5,labels=False)
    out["x20_by_r28z_quintile"]=g.groupby("q").agg(n=("x20","size"),mean_x20raw=("x20raw","mean"),mean_xz=("x20","mean"))
    g2=g.dropna(subset=["vrat"]).copy()
    g2["vq"]=pd.qcut(g2.vrat,3,labels=["calm","mid","wild"])
    g2["s"]=np.sign(g2.r28z)
    g2["signed"]=g2.s*g2.x20raw
    out["signed_momentum_by_vol"]=g2.groupby("vq").agg(n=("signed","size"),mean=("signed","mean"),t=("signed",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    g["signed"]=np.sign(g.r28z)*g.x20raw
    out["signed_momentum_by_year"]=g.groupby("yr").agg(n=("signed","size"),mean=("signed","mean"),t=("signed",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    out["signed_momentum_by_coin"]=g.groupby("coin").agg(n=("signed","size"),mean=("signed","mean"))
    out["corr_r28z_x20_spearman"]=float(stats.spearmanr(g.r28z,g.x20).correlation)
    # book
    br=[]
    for coin, ws in data["days"].items():
        for w,dd in ws.items():
            br.append(dd.assign(coin=coin,w=w))
    D=pd.concat(br)
    D["yr"]=pd.to_datetime(D["day"]).dt.year
    out["book_by_year"]=D.groupby("yr").agg(book=("book_return","mean"),coin=("coin_return","mean"))
    # gain by position sign
    d["nxt"]=d.groupby(["coin","w"])["r28"].shift(0)
    return out
