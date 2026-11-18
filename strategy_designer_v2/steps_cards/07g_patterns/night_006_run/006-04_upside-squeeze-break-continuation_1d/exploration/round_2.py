import numpy as np, pandas as pd
from scipy import stats

def build(data,H,off=0):
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            cl=b.close; hi=b.high; lo=b.low; v=b.volume
            r1=cl.pct_change()
            f=pd.DataFrame({'coin':c,'win':w,'fwd':cl.shift(-H)/cl-1,
              'r1':r1,'r5':cl/cl.shift(5)-1,
              'vrat':v.rolling(5).mean()/v.rolling(30).mean(),
              'vrat1':v/v.rolling(30).mean(),
              'vol20':r1.rolling(20).std(),
              'yr':pd.to_datetime(b.timestamp).dt.year})
            rows.append(f.iloc[off::H])
    d=pd.concat(rows).dropna(subset=['fwd','vrat','r5'])
    d['ex']=d.fwd-d.groupby('coin').fwd.transform('mean')
    d['lv']=np.log(d.vrat)
    return d

def ols(x,y):
    r=stats.linregress(x,y); return r.slope, r.slope/r.stderr, len(x)

def explore(data):
    out={}
    hz=[]
    for H in [1,3,5,10]:
        for off in [0,1,2]:
            if off>=H: continue
            d=build(data,H,off)
            s,t,n=ols(d.lv,d.ex)
            rho,p=stats.spearmanr(d.lv,d.ex)
            # signed: volume surge times direction of 5d move
            d['sv']=d.lv*np.sign(d.r5)
            s2,t2,_=ols(d.sv,d.ex)
            hz.append(dict(H=H,off=off,n=n,slope_lv=s,t_lv=t,rho=rho,t_signed=t2))
    out['vrat_by_horizon_offset']=pd.DataFrame(hz).round(4)
    d=build(data,3,0)
    pc=[]
    for c,g in d.groupby('coin'):
        s,t,n=ols(g.lv,g.ex); rho,_=stats.spearmanr(g.lv,g.ex)
        pc.append(dict(coin=c,n=n,slope=s,t=t,rho=rho))
    out['vrat_by_coin']=pd.DataFrame(pc).round(4)
    py=[]
    for y,g in d.groupby('yr'):
        if len(g)<50: continue
        s,t,n=ols(g.lv,g.ex); py.append(dict(yr=y,n=n,slope=s,t=t))
    out['vrat_by_year']=pd.DataFrame(py).round(4)
    # split by direction of 5d move
    d['up']=d.r5>0
    sp=[]
    for u,g in d.groupby('up'):
        s,t,n=ols(g.lv,g.ex); sp.append(dict(up5=u,n=n,slope=s,t=t,mean_ex=g.ex.mean()))
    out['vrat_by_r5_sign']=pd.DataFrame(sp).round(4)
    # control for vol20 and r5
    x=d.dropna(subset=['vol20']).copy()
    X=np.column_stack([np.ones(len(x)),x.lv,x.r5,x.vol20])
    b,res,_,_=np.linalg.lstsq(X,x.ex.values,rcond=None)
    e=x.ex.values-X@b; s2=e@e/(len(x)-4); cov=s2*np.linalg.inv(X.T@X)
    out['multi_t_lv_r5_vol']=pd.Series(b/np.sqrt(np.diag(cov)),index=['c','lv','r5','vol20']).round(3)
    # quintiles of lv per coin
    d['q']=d.groupby('coin').lv.transform(lambda s: pd.qcut(s.rank(method='first'),5,labels=False))
    out['lv_quintiles']=d.groupby('q').agg(mean_ex=('ex','mean'),n=('ex','count'),lv=('lv','mean'),up_share=('fwd',lambda s:(s>0).mean())).round(4)
    # 1-day vol spike
    s,t,n=ols(np.log(d.vrat1.clip(lower=1e-6)),d.ex); out['vrat1_t']=round(t,3)
    return out
