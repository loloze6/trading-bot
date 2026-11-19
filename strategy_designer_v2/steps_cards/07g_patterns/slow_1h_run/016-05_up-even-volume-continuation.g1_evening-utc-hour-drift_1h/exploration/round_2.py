def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            ts=pd.to_datetime(b["timestamp"],utc=True)
            r1=b["close"].shift(-1)/b["close"]-1
            d=pd.DataFrame({"coin":c,"w":w,"bh":ts.dt.hour,"nh":(ts+pd.Timedelta(hours=1)).dt.hour,"yr":ts.dt.year,
                            "pos":b["postRebalance_current_allocation"].fillna(0),"r1":r1,"close":b["close"].values})
            lr=np.log(b["close"]).diff()
            d["vol7"]=lr.rolling(168).std()
            d["vol24"]=lr.rolling(24).std()
            d["past24"]=b["close"]/b["close"].shift(24)-1
            d["fut24"]=b["close"].shift(-24)/b["close"]-1
            d["fut48"]=b["close"].shift(-48)/b["close"]-1
            d["i"]=np.arange(len(d))
            d["gain"]=d.pos*d.r1
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    held=A[A.pos.abs()>1e-9]
    hold=pd.DataFrame({"n":held.groupby("bh").size(),"pos_mean":held.groupby("bh").pos.mean(),
                       "move_bp":held.groupby("bh").r1.mean()*1e4,"gain_bp":held.groupby("bh").gain.mean()*1e4})
    # 21-22 block (bars starting 21 and 22): return close of 20:00 bar -> close of 22:00 bar
    B=A[A.bh==20].copy()
    # recompute 2h ahead: need close at i+2
    out=[]
    for (c,w),d in A.groupby(["coin","w"]):
        d=d.copy(); d["f2"]=d.close.shift(-2)/d.close-1; out.append(d[d.bh==20])
    B=pd.concat(out).dropna(subset=["f2"])
    g=B.groupby("yr").f2
    blk_yr=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    g=B.groupby("coin").f2
    blk_coin=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count()))})
    Bv=B.dropna(subset=["vol7"]).copy()
    Bv["vq"]=Bv.groupby("coin").vol7.transform(lambda x: pd.qcut(x,5,labels=False))
    g=Bv.groupby("vq").f2
    blk_vol=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # 24h reversal: grid, scaled by vol
    G=A[(A.i%24==0)].dropna(subset=["past24","fut24","vol7"]).copy()
    G["z"]=G.past24/(G.vol7*np.sqrt(24))
    G["zq"]=pd.qcut(G.z,10,labels=False)
    g=G.groupby("zq").fut24
    rz=pd.DataFrame({"z_mean":G.groupby("zq").z.mean(),"fut_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    neg=G[G.z<0]
    sl=stats.linregress(neg.z,neg.fut24)
    pos=G[G.z>0]; sl2=stats.linregress(pos.z,pos.fut24)
    sl_df=pd.DataFrame({"slope":[sl.slope,sl2.slope],"t":[sl.slope/sl.stderr,sl2.slope/sl2.stderr],"n":[len(neg),len(pos)]},index=["down","up"])
    G["low"]=G.zq<=1
    lowyr=G[G.low].groupby("yr").fut24
    rev_yr=pd.DataFrame({"mean_bp":lowyr.mean()*1e4,"t":lowyr.mean()/(lowyr.std()/np.sqrt(lowyr.count())),"n":lowyr.count()})
    lowc=G[G.low].groupby("coin").fut24
    rev_coin=pd.DataFrame({"mean_bp":lowc.mean()*1e4,"t":lowc.mean()/(lowc.std()/np.sqrt(lowc.count()))})
    allm=G.fut24.mean()*1e4
    return {"hold_by_barhour":hold,"blk2122_yr":blk_yr,"blk2122_coin":blk_coin,"blk2122_vol":blk_vol,
            "rev24_z_dec":rz,"rev24_slopes":sl_df,"rev_low2dec_yr":rev_yr,"rev_low2dec_coin":rev_coin,"all_fut24_bp":allm}
