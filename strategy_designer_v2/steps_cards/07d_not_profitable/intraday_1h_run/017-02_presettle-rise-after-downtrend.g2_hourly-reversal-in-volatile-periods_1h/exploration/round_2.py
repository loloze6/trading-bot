def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            cl=b["close"]
            lr=np.log(cl).diff()
            v24=lr.rolling(24).std()
            vavg=v24.rolling(720,min_periods=100).mean()
            vrel=v24/vavg
            d=pd.DataFrame({"coin":c,"win":w,"vrel":vrel})
            for k in [1,4,12,24]:
                d[f"s{k}"]=(cl/cl.shift(k)-1)/(vavg*np.sqrt(k))
            for h in [1,4,12,24]:
                d[f"r{h}"]=cl.shift(-h)/cl-1
            d["pos"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    # fade gain per situation k and horizon h, nonoverlap grid of h, by decile of |s|; signed = -sign(s)*r
    res=[]
    for k in [1,4,12,24]:
        for h in [4,12,24]:
            sub=D[D.pos%h==0].dropna(subset=[f"s{k}",f"r{h}"])
            g=-np.sign(sub[f"s{k}"])*sub[f"r{h}"]
            a=sub[f"s{k}"].abs()
            top=a>=a.quantile(0.9)
            top_hv=top&(sub.vrel>=sub.vrel.quantile(0.8))
            res.append({"k":k,"h":h,"all_mean":g.mean(),"all_t":g.mean()/g.std()*np.sqrt(len(g)),
                        "top10_mean":g[top].mean(),"top10_t":g[top].mean()/g[top].std()*np.sqrt(top.sum()),"n_top":int(top.sum()),
                        "top10_hv_mean":g[top_hv].mean(),"n_tophv":int(top_hv.sum()),
                        "corr_s_r":np.corrcoef(sub[f"s{k}"],sub[f"r{h}"])[0,1]})
    out["fade_by_k_h"]=pd.DataFrame(res)
    # 24h horizon, decile of s24 signed (not abs): mean forward 24h return
    sub=D[D.pos%24==0].dropna(subset=["s24","r24"])
    sub["dq"]=pd.qcut(sub.s24,10,labels=False)
    out["s24_decile_r24"]=sub.groupby("dq").agg(r24=("r24","mean"),s=("s24","mean"),n=("r24","size"))
    sub=D[D.pos%4==0].dropna(subset=["s4","r4"])
    sub["dq"]=pd.qcut(sub.s4,10,labels=False)
    out["s4_decile_r4"]=sub.groupby("dq").agg(r4=("r4","mean"),s=("s4","mean"),n=("r4","size"))
    return out
