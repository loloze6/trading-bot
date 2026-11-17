def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    recs=[]
    for c, ws in data["bars"].items():
        for w, b_ in ws.items():
            s=b_["close"].reset_index(drop=True); cl=s.values
            r1=s.pct_change().values
            al=b_["postRebalance_current_allocation"].values
            nxt=np.r_[cl[1:]/cl[:-1]-1, np.nan]
            fwd2=np.r_[cl[2:]/cl[:-2]-1,[np.nan,np.nan]]
            ma=(s/s.rolling(50,min_periods=20).mean()-1).values
            r30=(s/s.shift(30)-1).values
            sd=pd.Series(r1).rolling(60,min_periods=20).std().values
            recs.append(pd.DataFrame(dict(coin=c,w=w,wn=int(w[1:]),pos=np.arange(len(cl)),r1=r1,z=r1/sd,f=b_["forecast"].values,al=al,gain=al*nxt,nxt=nxt,fwd2=fwd2,ma=ma,r30=r30)))
    B=pd.concat(recs).dropna(subset=["nxt","ma","r30","z"])
    B["tr"]=pd.qcut(B.ma,3,labels=["down","mid","up"])
    B["dir"]=np.where(B.r1<0,"fall","rise")
    out["gain by trend, all bars (n,alloc,gain,sum share)"]=B.groupby("tr").agg(n=("gain","size"),alloc=("al","mean"),gain=("gain","mean"),gsum=("gain","sum")).round(5)
    # worst dd windows 1-3: what held
    W=B[B.wn<=3]
    out["w1-3 gain by trend x dir"]=W.groupby(["tr","dir"]).agg(n=("gain","size"),alloc=("al","mean"),gain=("gain","mean"),gsum=("gain","sum")).round(4)
    # graded: signed z * trend interaction on exc2, grid
    g=B[B.pos%2==0].dropna(subset=["fwd2"]).copy()
    g["exc2"]=g.fwd2-g.groupby("coin").fwd2.transform("mean")
    g["r30q"]=pd.qcut(g.r30,5,labels=False)
    out["exc2 big rises by 30d return quintile"]=g[(g.dir=="rise")&(g.z>1)].groupby("r30q").agg(n=("exc2","size"),exc2=("exc2","mean"),t=("exc2",lambda x:x.mean()/x.std()*np.sqrt(len(x)))).round(5)
    out["exc2 big falls by 30d return quintile"]=g[(g.dir=="fall")&(g.z<-1)].groupby("r30q").agg(n=("exc2","size"),exc2=("exc2","mean"),t=("exc2",lambda x:x.mean()/x.std()*np.sqrt(len(x)))).round(5)
    # interaction regression: exc2 ~ f + f*sign(ma)
    g["fs"]=g.f*np.sign(g.ma)
    X=np.c_[np.ones(len(g)),g.f,g.fs]; y=g.exc2.values
    beta,res,_,_=np.linalg.lstsq(X,y,rcond=None)
    e=y-X@beta; s2=e@e/(len(y)-3); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["exc2~f+f*sign(ma) beta,t"]=pd.DataFrame({"beta":beta,"t":beta/se},index=["c","f","f*sign(ma)"])
    # simulated: drop positions when price below 50d ma -> daily pooled
    B["day"]=B.groupby(["coin","w"]).pos.transform(lambda x:x)
    for name,mask in [("all",np.ones(len(B),bool)),("only above ma",B.ma>0),("skip rises below ma",~((B.ma<0)&(B.dir=="rise")))]:
        gg=B.gain.where(mask,0.0)
        P=pd.DataFrame({"wn":B.wn,"pos":B.pos,"g":gg}).groupby(["wn","pos"]).g.mean().sort_index()
        eq=(1+P).cumprod(); mdd=(eq/eq.cummax()-1).min(); yr=eq.iloc[-1]**(365/len(P))-1
        out[f"sim {name}: sharpe,yr,mdd,calmar"]=str(np.round([P.mean()/P.std()*np.sqrt(365),yr,mdd,yr/-mdd],4))
    return out
