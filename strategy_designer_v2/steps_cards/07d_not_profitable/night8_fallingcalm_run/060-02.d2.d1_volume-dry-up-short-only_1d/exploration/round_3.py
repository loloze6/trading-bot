def explore(data):
    import numpy as np, pandas as pd
    out={}
    coins=list(data["bars"].keys())
    wins=sorted(data["bars"][coins[0]].keys(), key=lambda w:int(w[1:]))
    def tt(s):
        s=s.dropna(); return s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan
    rows=[]
    for c in coins:
        for w in wins:
            d=data["days"][c].get(w)
            if d is None: continue
            t=d[["day","book_return","coin_return"]].copy(); t["day"]=t.day.astype(str).str[:10]; t["coin"]=c; t["w"]=w
            rows.append(t)
    D=pd.concat(rows)
    B=D.groupby(["w","day"]).agg(br=("book_return","mean")).reset_index()
    B["wn"]=B.w.str[1:].astype(int); B=B.sort_values(["wn","day"]).dropna(subset=["br"]).reset_index(drop=True)
    v=(1+B.br).cumprod(); dd=v/v.cummax()-1
    i=int(np.argmin(dd.values)); pk=int(np.argmax(v.values[:i+1]))
    fall=set(zip(B.w.values[pk+1:i+1],B.day.values[pk+1:i+1]))
    Df=D[[(a,b) in fall for a,b in zip(D.w,D.day)]]
    out["fall by coin (book_return sum/6)"]=Df.groupby("coin").book_return.sum()/6
    out["fall by window"]=Df.groupby("w").book_return.sum()/6
    held=[]; cs=[]
    for c in coins:
        drs=[]
        for w in wins:
            b=data["bars"][c].get(w)
            if b is None: continue
            cl=b.close.values
            for k in range(0,len(cl)-5,5): drs.append(cl[k+5]/cl[k]-1)
        drift=np.mean(drs)
        for w in wins:
            b=data["bars"][c].get(w)
            if b is None: continue
            b=b.reset_index(drop=True); cl=b.close; r1=cl.pct_change()
            ret60=cl/cl.shift(60)-1; ret10=cl/cl.shift(10)-1
            off30=cl/cl.rolling(30).min()-1
            f=b.forecast; alloc=b.postRebalance_current_allocation
            g=(cl.shift(-1)/cl-1)*alloc
            day=b.timestamp.astype(str).str[:10]
            held.append(pd.DataFrame({"g":g,"alloc":alloc,"f":f,"ret60":ret60,"off30":off30,"w":w,"coin":c,"day":day}))
            fv=f.values; n=len(b)
            for k in range(0,n-5,5):
                for j in range(k,min(k+5,n-5)):
                    if fv[j]<=-2:
                        cs.append(dict(u=drift-(cl[j+5]/cl[j]-1),f=fv[j],ret60=ret60[j],off30=off30[j],w=w,fall=(w,day[j]) in fall)); break
    H=pd.concat(held); H=H[H.alloc.abs()>1e-9].dropna(subset=["g"])
    H["infall"]=[(a,b) in fall for a,b in zip(H.w,H.day)]
    out["held in fall vs not"]=H.groupby("infall").agg(mean_g=("g","mean"),n=("g","size"),f=("f","mean"),ret60=("ret60","mean"),off30=("off30","mean"))
    H["fb"]=pd.cut(H.f,[-21,-13.5,-6.5,0.1])
    out["held gain by forecast"]=H.groupby("fb").agg(mean_g=("g","mean"),sd=("g","std"),n=("g","size"),share_in_fall=("infall","mean"))
    C=pd.DataFrame(cs)
    C["fb"]=pd.cut(C.f,[-21,-13.5,-6.5,0.1])
    out["cases fall vs not"]=C.groupby("fall").agg(mean_u=("u","mean"),n=("u","size"),f=("f","mean"),off30=("off30","mean"))
    for col in ["ret60","off30"]:
        x=C.dropna(subset=[col]).copy(); x["b"]=pd.qcut(x[col],3,labels=False)
        out["cases by "+col]=x.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),mean_u=("u","mean"),n=("u","size"),t=("u",tt))
    # approximate book using only strong forecasts: gain days with f<=-13.5 (others 0)
    for lab,thr in [("all",0),("f<=-6.5",-6.5),("f<=-13.5",-13.5)]:
        h=H.copy(); h.loc[h.f>thr if thr<0 else h.f>1e9,"g"]=0
        bd=h.groupby(["w","day"]).g.sum()/6
        bd=bd.reset_index(); bd["wn"]=bd.w.str[1:].astype(int); bd=bd.sort_values(["wn","day"])
        vv=(1+bd.g).cumprod(); ddd=(vv/vv.cummax()-1).min()
        out["approx book "+lab]=pd.Series({"sum":bd.g.sum(),"maxdd":ddd,"ratio":bd.g.sum()/abs(ddd)})
    return out
