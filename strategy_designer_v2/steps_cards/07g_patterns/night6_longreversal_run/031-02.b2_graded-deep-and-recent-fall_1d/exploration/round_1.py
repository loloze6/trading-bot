import numpy as np, pandas as pd
from scipy import stats

def _ct(df, col):
    # mean and day-clustered t of col; df has 'ts'
    d = df.dropna(subset=[col])
    if len(d) < 3: return (np.nan, np.nan, len(d), 0)
    m = d[col].mean()
    s = (d[col]-m).groupby(d['ts']).sum()
    D = len(s)
    if D < 2: return (m, np.nan, len(d), D)
    se = np.sqrt((s**2).sum()*D/(D-1))/len(d)
    return (m, m/se if se>0 else np.nan, len(d), D)

def explore(data):
    bars = data["bars"]; out = {}
    # ---- grid samples at several horizons with past returns
    rows = []
    for H, P in [(30,30),(30,60),(7,7),(7,30),(14,14)]:
        for c, wins in bars.items():
            samp = []
            for w, b in wins.items():
                cl = b['close'].values; ts = pd.to_datetime(b['timestamp']).values
                hi = b['high'].values; lo = b['low'].values
                r1 = np.r_[np.nan, cl[1:]/cl[:-1]-1]
                for i in range(0, len(cl), H):
                    if i+H >= len(cl) or i-P < 0: continue
                    vol = np.nanstd(r1[max(1,i-29):i+1]) if i>=10 else np.nan
                    samp.append(dict(coin=c, w=w, ts=ts[i], H=H, P=P,
                                     fwd=cl[i+H]/cl[i]-1, past=cl[i]/cl[i-P]-1, vol=vol,
                                     wd=pd.Timestamp(ts[i]).weekday()))
            s = pd.DataFrame(samp)
            if len(s)==0: continue
            # normal drift: coin mean of fwd over its grid (all windows)
            s['ex'] = s['fwd'] - s['fwd'].mean()
            s['zpast'] = s['past']/s['past'].std()
            s['zvol'] = (s['vol']-s['vol'].mean())/s['vol'].std()
            rows.append(s)
    g = pd.concat(rows, ignore_index=True)
    res = []
    for (H,P), s in g.groupby(['H','P']):
        s = s.copy()
        s['q'] = pd.qcut(s['zpast'], 5, labels=False, duplicates='drop')
        for q, sq in s.groupby('q'):
            m, t, n, D = _ct(sq, 'ex')
            res.append(dict(H=H, P=P, q=q, zpast=sq['zpast'].mean(), mean_ex=m, t=t, n=n, days=D))
        sl = stats.linregress(s['zpast'], s['ex'])
        res.append(dict(H=H, P=P, q='slope', zpast=np.nan, mean_ex=sl.slope, t=sl.slope/sl.stderr, n=len(s), days=s['ts'].nunique()))
    out['past_vs_fwd_quintiles'] = pd.DataFrame(res)
    # volatility level vs forward
    res = []
    for (H,P), s in g.groupby(['H','P']):
        if P != H: continue
        s = s.dropna(subset=['zvol']).copy()
        s['q'] = pd.qcut(s['zvol'], 3, labels=False, duplicates='drop')
        for q, sq in s.groupby('q'):
            m,t,n,D = _ct(sq,'ex'); res.append(dict(H=H,volq=q,mean_ex=m,t=t,n=n,days=D))
    out['vol_vs_fwd'] = pd.DataFrame(res)
    # daily returns by weekday, all coins
    dl = []
    for c, wins in data['days'].items():
        for w, d in wins.items():
            d = d.copy(); d['coin']=c; d['w']=w; dl.append(d)
    D = pd.concat(dl, ignore_index=True)
    D['day'] = pd.to_datetime(D['day'])
    D['wd'] = D['day'].dt.weekday
    D['ts'] = D['day']
    D['cr_ex'] = D['coin_return'] - D.groupby('coin')['coin_return'].transform('mean')
    res=[]
    for wd, s in D.groupby('wd'):
        m,t,n,Dd = _ct(s,'cr_ex'); res.append(dict(wd=wd,mean_ex=m,t=t,n=n))
    out['weekday_coin'] = pd.DataFrame(res)
    # lag-1 daily: return after large daily moves
    D = D.sort_values(['coin','w','day'])
    D['next'] = D.groupby(['coin','w'])['coin_return'].shift(-1)
    D['nx_ex'] = D['next'] - D.groupby('coin')['coin_return'].transform('mean')
    D['z'] = D['coin_return']/D.groupby('coin')['coin_return'].transform('std')
    D['zb'] = pd.cut(D['z'], [-99,-2,-1,0,1,2,99])
    res=[]
    for b, s in D.groupby('zb', observed=True):
        m,t,n,Dd = _ct(s,'nx_ex'); res.append(dict(zbin=str(b),mean_ex=m,t=t,n=n))
    out['next_day_after_move'] = pd.DataFrame(res)
    # book: active share, book daily by year
    book = D.groupby('day')['book_return'].mean()
    out['book_by_year'] = book.groupby(book.index.year).agg(['mean','std','count'])
    # forecast on active grid: by window
    fr=[]
    for c, wins in bars.items():
        for w, b in wins.items():
            cl=b['close'].values; f=b['forecast'].values
            for i in range(0,len(cl),30):
                if i+30>=len(cl): continue
                fr.append(dict(coin=c,w=w,ts=b['timestamp'].iloc[i],f=f[i],fwd=cl[i+30]/cl[i]-1,
                               reg=b['regime'].iloc[i]))
    F=pd.DataFrame(fr); F['ex']=F['fwd']-F.groupby('coin')['fwd'].transform('mean')
    F['act']=F['f']>0
    out['active_vs_not'] = F.groupby('act')['ex'].agg(['mean','count'])
    out['active_by_coin'] = F[F.act].groupby('coin')['ex'].agg(['mean','count'])
    # trades
    T=[]
    for c, wins in data['trades'].items():
        for w,t in wins.items():
            t=t.copy(); t['coin']=c; T.append(t)
    T=pd.concat(T,ignore_index=True)
    out['trades_summary'] = T.groupby('coin')['net_profit_loss_percent'].agg(['mean','median','count'])
    out['trades_duration_days'] = (T['duration_minutes']/1440).describe()
    return out
