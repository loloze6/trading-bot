def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    # book daily chain
    wins = sorted({w for c in coins for w in days[c]}, key=lambda s:int(s[1:]))
    chain=[]
    for w in wins:
        dfs=[days[c][w].set_index("day")["book_return"] for c in coins if w in days[c]]
        m=pd.concat(dfs,axis=1).mean(axis=1).dropna()
        chain.append(pd.DataFrame({"w":w,"r":m.values}))
    ch=pd.concat(chain,ignore_index=True)
    v=(1+ch.r).cumprod(); dd=v/v.cummax()-1
    ch["dd"]=dd.values
    out["dd_by_window"]=ch.groupby("w").agg(ret=("r",lambda x:(1+x).prod()-1),mindd=("dd","min"),worstday=("r","min")).reindex(wins)
    # cases
    rows=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b.timestamp)
            cl=b.close.values; vol=b.volume.values
            lr=np.log(cl); r1=np.diff(lr,prepend=np.nan)
            idx=np.where((ts.dt.weekday==6)&(ts.dt.hour==23))[0]
            for i in idx:
                if i<168+48 or i+12>=len(b): continue
                wk=cl[i]/cl[i-48]-1
                vr=vol[i-47:i+1].mean()/max(vol[i-167:i-47].mean(),1e-12)
                pw=cl[i-48]/cl[i-168]-1
                rv=np.nanstd(r1[max(1,i-720):i+1])*np.sqrt(48)
                f=b.forecast.iloc[i]
                fwd=cl[i+12]/cl[i]-1
                path=cl[i+1:i+13]/cl[i]-1
                s=np.sign(wk)
                rows.append(dict(c=c,w=w,yr=ts.iloc[i].year,wk=wk,vr=vr,pw=pw,rv=rv,f=f,
                    fwd=fwd,s=s,sfwd=s*fwd,mae=(s*path).min(),z=abs(wk)/rv,
                    alloc=b.postRebalance_current_allocation.iloc[i]))
    d=pd.DataFrame(rows)
    d["heavy"]=d.vr>=1
    h=d[d.heavy&(d.f!=0)].copy()
    def st(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out["heavy_vs_light_signed"]=d.groupby("heavy").sfwd.apply(st).unstack()
    h["side"]=np.where(h.s>0,"long","short")
    out["by_side"]=h.groupby("side").sfwd.apply(st).unstack()
    out["by_coin"]=h.groupby("c").sfwd.apply(st).unstack()
    out["by_year"]=h.groupby("yr").sfwd.apply(st).unstack()
    h["agree"]=np.sign(h.pw)==h.s
    out["by_prevweek_agree"]=h.groupby("agree").sfwd.apply(st).unstack()
    d["agree"]=np.sign(d.pw)==d.s
    out["light_by_agree"]=d[~d.heavy].groupby("agree").sfwd.apply(st).unstack()
    h["zq"]=pd.qcut(h.z,4,labels=False); out["by_zq"]=h.groupby("zq").sfwd.apply(st).unstack()
    h["vq"]=pd.qcut(h.vr,4,labels=False); out["by_vrq"]=h.groupby("vq").sfwd.apply(st).unstack()
    h["rvq"]=pd.qcut(h.rv,4,labels=False); out["by_rvq"]=h.groupby("rvq").sfwd.apply(st).unstack()
    h["fq"]=pd.qcut(h.f.abs(),4,labels=False); out["by_absf_q"]=h.groupby("fq").agg(sf=("sfwd","mean"),alloc=("alloc",lambda x:x.abs().mean()),n=("sfwd","size"))
    out["mae_quantiles"]=h.mae.quantile([.05,.1,.25,.5])
    for k in [-0.02,-0.03,-0.05]:
        hit=h.mae<=k
        out[f"stop{k}"]=pd.Series({"hits":hit.sum(),"fwd_if_hit":h.sfwd[hit].mean(),"capped_mean":np.where(hit,k,h.sfwd).mean()})
    # trades
    tr=pd.concat([t.assign(c=c) for c in coins for w,t in data["trades"][c].items()],ignore_index=True)
    out["trades"]=tr.groupby("side").net_profit_loss_percent.agg(["count","mean","std","min"])
    out["dur_q"]=tr.duration_minutes.quantile([.1,.5,.9])
    return out
