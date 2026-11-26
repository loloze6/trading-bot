import numpy as np, pandas as pd
from scipy import stats

def _ct(df, col, tcol='ts'):
    d = df.dropna(subset=[col])
    if len(d) < 3: return (np.nan, np.nan, len(d), 0)
    m = d[col].mean()
    s = (d[col]-m).groupby(d[tcol]).sum()
    D = len(s)
    if D < 2: return (m, np.nan, len(d), D)
    se = np.sqrt((s**2).sum()*D/(D-1))/len(d)
    return (m, m/se if se>0 else np.nan, len(d), D)

def explore(data):
    bars = data["bars"]; out = {}
    # ---------- A: 7-day forward on vol-scaled past 30-day return, trailing vol only
    rows=[]
    for c, wins in bars.items():
        for w, b in wins.items():
            cl=b['close'].values; ts=pd.to_datetime(b['timestamp']).values
            r1=np.r_[np.nan, cl[1:]/cl[:-1]-1]
            yr=pd.Timestamp(ts[0]).year
            for i in range(0,len(cl),7):
                if i+7>=len(cl) or i<30: continue
                v=np.nanstd(r1[i-29:i+1])
                rows.append(dict(coin=c,w=w,ts=ts[i],yr=pd.Timestamp(ts[i]).year,
                                 fwd=cl[i+7]/cl[i]-1, p30=cl[i]/cl[i-30]-1, p7=cl[i]/cl[i-7]-1,
                                 v=v))
    A=pd.DataFrame(rows)
    A['ex']=A['fwd']-A.groupby('coin')['fwd'].transform('mean')
    A['s30']=A['p30']/(A['v']*np.sqrt(30)); A['s7']=A['p7']/(A['v']*np.sqrt(7))
    A['exs']=A['ex']/(A['v']*np.sqrt(7))  # strength-like
    res=[]
    for nm in ['s30','s7']:
        A['q']=pd.qcut(A[nm],5,labels=False)
        for q,s in A.groupby('q'):
            m,t,n,D=_ct(s,'ex'); res.append(dict(sig=nm,q=q,x=s[nm].mean(),mean_ex=m,t=t,n=n,days=D))
        sl=stats.linregress(A[nm],A['exs']); res.append(dict(sig=nm,q='slope_strength',x=np.nan,mean_ex=sl.slope,t=sl.slope/sl.stderr,n=len(A),days=A.ts.nunique()))
    out['A_mom7_quintiles']=pd.DataFrame(res)
    res=[]
    for c,s in A.groupby('coin'):
        sl=stats.linregress(s['s30'],s['exs']); res.append(dict(coin=c,slope=sl.slope,t=sl.slope/sl.stderr,n=len(s)))
    out['A_mom7_by_coin']=pd.DataFrame(res)
    res=[]
    for y,s in A.groupby('yr'):
        sl=stats.linregress(s['s30'],s['exs']); res.append(dict(yr=y,slope=sl.slope,t=sl.slope/sl.stderr,n=len(s)))
    out['A_mom7_by_year']=pd.DataFrame(res)
    # ---------- B: next-day after large daily move, scaled by trailing 30-day vol
    dl=[]
    for c,wins in bars.items():
        for w,b in wins.items():
            cl=b['close'].values; ts=pd.to_datetime(b['timestamp']).values
            r=pd.Series(np.r_[np.nan, cl[1:]/cl[:-1]-1])
            v=r.rolling(30,min_periods=20).std().shift(1)
            d=pd.DataFrame(dict(coin=c,w=w,ts=ts,r=r,z=r/v,yr=pd.to_datetime(ts).year))
            d['n1']=r.shift(-1); d['n3']=(pd.Series(cl).shift(-3)/pd.Series(cl)-1)
            dl.append(d)
    B=pd.concat(dl,ignore_index=True).dropna(subset=['z'])
    B['ex1']=B['n1']-B.groupby('coin')['r'].transform('mean')
    B['zb']=pd.cut(B['z'],[-99,-3,-2,-1,1,2,3,99])
    res=[]
    for zb,s in B.groupby('zb',observed=True):
        m,t,n,D=_ct(s,'ex1'); res.append(dict(zbin=str(zb),mean_ex1=m,t=t,n=n))
    sl=stats.linregress(B.dropna(subset=['ex1'])['z'].clip(-5,5),B.dropna(subset=['ex1'])['ex1'])
    res.append(dict(zbin='slope',mean_ex1=sl.slope,t=sl.slope/sl.stderr,n=len(B)))
    out['B_nextday_trailvol']=pd.DataFrame(res)
    res=[]
    for c,s in B.groupby('coin'):
        s=s.dropna(subset=['ex1']); sl=stats.linregress(s['z'].clip(-5,5),s['ex1']); res.append(dict(coin=c,slope=sl.slope,t=sl.slope/sl.stderr))
    out['B_by_coin']=pd.DataFrame(res)
    # ---------- C: book's largest days: what the coins did before
    dl=[]
    for c,wins in data['days'].items():
        for w,d in wins.items():
            d=d.copy(); d['coin']=c; d['w']=w; dl.append(d)
    Dd=pd.concat(dl,ignore_index=True)
    book=Dd.groupby('day')['book_return'].mean().dropna()
    hold=Dd.groupby('day')['coin_return'].mean()
    q=book.quantile([0.01,0.99])
    out['C_book_tail']=pd.DataFrame({'n_top':[(book>=q[0.99]).sum()],'sum_top_1pct':[book[book>=q[0.99]].sum()],
        'sum_bottom_1pct':[book[book<=q[0.01]].sum()],'sum_all':[book.sum()],
        'hold_on_top':[hold.reindex(book[book>=q[0.99]].index).mean()],
        'hold_on_bottom':[hold.reindex(book[book<=q[0.01]].index).mean()]})
    # by coin: book contribution
    Dd['br']=Dd['book_return']
    out['C_book_by_coin']=Dd.groupby('coin')['br'].agg(['mean','sum','std'])
    # ---------- D: in-position 30d after entry by allocation level / time held
    T=[]
    for c,wins in data['trades'].items():
        for w,t in wins.items():
            t=t.copy(); t['coin']=c; T.append(t)
    T=pd.concat(T,ignore_index=True)
    T['dd']=T['duration_minutes']/1440
    T['db']=pd.cut(T['dd'],[-1,7,29,31,60,200])
    out['D_trades_by_duration']=T.groupby('db',observed=True)['net_profit_loss_percent'].agg(['mean','median','count'])
    return out
