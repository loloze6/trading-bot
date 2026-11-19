def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,df in ws.items():
            allr.append((df["close"].shift(-1)/df["close"]-1).dropna())
        mu=pd.concat(allr).mean()
        for w,df in ws.items():
            c=df["close"].reset_index(drop=True)
            past=c/c.shift(1)-1
            vol720=past.rolling(720,min_periods=720).std()
            z=past/past.rolling(20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(c)),"past":past,"z":z,"vol":vol720,
                            "a":df["postRebalance_current_allocation"].values,
                            "turn":(df["postRebalance_current_allocation"]-df["previous_allocation"]).abs().values,
                            "pv":df["postRebalance_total_value"].values,"tv":df["total_portfolio_value"].values})
            for h in [1,2,4,8]:
                d[f"r{h}"]=c.shift(-h)/c-1
            d["ex"]=d.a*(d.r1-mu)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["med"]=D.groupby("coin")["vol"].transform("median")
    D["vg"]=np.where(D.vol.isna(),"na",np.where(D.vol>D.med,"high",np.where(D.vol<D.med,"low","eq")))
    def t(x): x=x.dropna(); return x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
    out={}
    # fee per bar implied
    fee=(D.tv-D.pv)/D.tv
    out["fee_per_bar_mean"]=float(fee.mean())
    out["gross_minus_fee"]=float(D.ex.mean()-fee.mean())
    # raw fade by |z| quintile and vol group
    D["fz"]=-D.z*D.r1/D.vol.where(D.vol>0)
    D["zq"]=pd.qcut(D.z.abs(),5,labels=False,duplicates="drop")
    E=D[D.vg.isin(["high","low"])]
    g=E.groupby(["zq","vg"]).ex.agg(["mean","count"]).unstack()
    out["ex_by_zq_vg"]=g
    # Welch t of high-low excess on top z quintile only
    top=E[E.zq==4]
    out["welch_topz_high_minus_low"]=float(stats.ttest_ind(top[top.vg=="high"].ex.dropna(),top[top.vg=="low"].ex.dropna(),equal_var=False).statistic)
    # horizon: non-overlapping fade -sign(past)*r_h, grid per window
    res={}
    for h in [1,2,4,8]:
        s=D[D.pos%h==0]
        x=(-np.sign(s.past)*s[f"r{h}"]).dropna()
        res[h]={"mean":x.mean(),"n":len(x),"t":t(x)}
    out["fade_sign_by_horizon"]=pd.DataFrame(res).T
    # vol-normalized fade slope: regress r1/vol on z, by vol group
    reg={}
    for vg in ["high","low"]:
        s=E[E.vg==vg].dropna(subset=["z","r1"])
        y=s.r1/s.vol
        lr=stats.linregress(s.z,y)
        reg[vg]={"slope":lr.slope,"t":lr.slope/lr.stderr,"n":len(s)}
    out["slope_r1overvol_on_z"]=pd.DataFrame(reg).T
    return out
