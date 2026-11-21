def explore(data):
    import numpy as np, pandas as pd
    bars=data["bars"]; days=data["days"]
    out={}
    G=[]
    for c in bars:
        dr={}
        for h in (18,36,72):
            v=[]
            for w,b in bars[c].items():
                cl=b["close"].values; idx=np.arange(0,len(cl)-h,h)
                v+=list(cl[idx+h]/cl[idx]-1)
            dr[h]=(np.mean(v),np.std(v))
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values; hi=b["high"].values; lo=b["low"].values
            s=pd.Series(cl)
            r42=s.pct_change(42).values; r180=s.pct_change(180).values
            hh=pd.Series(hi).shift(1).rolling(12).max().values
            mr=pd.Series(hi-lo).rolling(180).mean().values
            brk=(cl-hh)/mr
            vol=s.pct_change().rolling(42).std().values
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            for h in (18,36,72):
                for i in range(0,len(cl)-h,h):
                    if np.isnan(r42[i]) or np.isnan(vol[i]) or vol[i]==0: continue
                    G.append((c,w,yr[i],h,(cl[i+h]/cl[i]-1-dr[h][0]),(cl[i+h]/cl[i]-1-dr[h][0])/dr[h][1],r42[i],r42[i]/(vol[i]*np.sqrt(42)),r180[i],brk[i]))
    G=pd.DataFrame(G,columns=["c","w","yr","h","u","st","r42","r42z","r180","brk"])
    def summ(d):
        n=len(d); return pd.Series({"n":n,"mean":d.u.mean(),"t":d.u.mean()/(d.u.std()/np.sqrt(n)),"strength":d.st.mean()})
    for h in (18,72):
        g=G[G.h==h].copy()
        g["q"]=pd.qcut(g.r42z.rank(method="first"),6,labels=False)
        out[f"grid{h}_by_r42z_sextile"]=g.groupby("q").apply(summ).join(g.groupby("q").r42z.mean())
        p=g[g.r42>0].copy()
        p["bq"]=pd.qcut(p.brk.rank(method="first"),4,labels=False)
        out[f"grid{h}_r42pos_by_break_q"]=p.groupby("bq").apply(summ).join(p.groupby("bq").brk.mean())
        out[f"grid{h}_corr"]=pd.Series({"r42z_u":g.r42z.corr(g.u,method="spearman"),"brk_u_r42pos":p.brk.corr(p.u,method="spearman"),"r180_u":g.r180.corr(g.u,method="spearman")})
    g=G[(G.h==18)].copy(); g["q"]=pd.qcut(g.r42z.rank(method="first"),3,labels=False)
    top=g[g.q==2]
    out["grid18_top_r42z_by_coin"]=top.groupby("c").apply(summ)
    out["grid18_top_r42z_by_year"]=top.groupby("yr").apply(summ)
    D=pd.concat([d.assign(c=c,w=w) for c in days for w,d in days[c].items()])
    D["yr"]=pd.to_datetime(D["day"]).dt.year
    bk=D.groupby(["w","day"]).book_return.mean().dropna()
    out["book_daily"]=pd.Series({"mean":bk.mean(),"sharpe":bk.mean()/bk.std()*np.sqrt(365),"top5pct_days_share_of_sum":bk.sort_values(ascending=False).head(int(len(bk)*0.05)).sum()/bk.sum()})
    yy=D.groupby(["yr","w","day"]).book_return.mean().dropna().groupby(level=0)
    out["book_by_year"]=pd.DataFrame({"mean":yy.mean(),"sharpe":yy.mean()/yy.std()*np.sqrt(365),"n":yy.size()})
    return out
