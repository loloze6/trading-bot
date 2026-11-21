def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    days=data["days"]; bars=data["bars"]
    rows=[]
    for c in days:
        for w in days[c]:
            d=days[c][w].copy(); b=bars[c][w].copy()
            b['day']=pd.to_datetime(b['timestamp']).dt.floor('D')
            bb=b.groupby('day').last()[['postRebalance_current_allocation','forecast']]
            d['day']=pd.to_datetime(d['day']).dt.floor('D')
            d=d.merge(bb,left_on='day',right_index=True,how='left')
            d['a']=d['postRebalance_current_allocation'].shift(1)
            d['fc']=d['forecast'].shift(1)
            cl=d['close']
            d['r28']=(cl/cl.shift(28)-1).shift(1)
            d['r90']=(cl/cl.shift(90)-1).shift(1)
            d['r7']=(cl/cl.shift(7)-1).shift(1)
            lr=np.log(cl).diff()
            d['vol10']=lr.rolling(10).std().shift(1)
            d['vol60']=lr.rolling(60).std().shift(1)
            d['coin']=c; d['wi']=int(w[1:])
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D['pnl']=D['a']*D['coin_return']
    D['pl']=D['a'].clip(lower=0)*D['coin_return']
    D['ps']=D['a'].clip(upper=0)*D['coin_return']
    out={}
    def book(col):
        P=D.dropna(subset=['coin_return']).groupby(['wi','day'])[col].mean().sort_index()
        eq=(1+P).cumprod(); dd=(eq/eq.cummax()-1).min()
        yr=eq.iloc[-1]**(365/len(P))-1
        return pd.Series({'yearly':yr,'maxdd':dd,'calmar':yr/-dd,'sharpe':P.mean()/P.std()*np.sqrt(365),'mean':P.mean()})
    out['books']=pd.DataFrame({'all_gross':book('pnl'),'long_only':book('pl'),'short_only':book('ps')})
    S=D[D['a']<0].dropna(subset=['r90','pnl'])
    S['r90s']=np.sign(S['r90'])
    out['short_by_r90sign']=S.groupby('r90s').agg(n=('pnl','size'),pnl=('pnl','mean'),coin=('coin_return','mean'))
    L=D[D['a']>0].dropna(subset=['r90','pnl'])
    L['r90s']=np.sign(L['r90'])
    out['long_by_r90sign']=L.groupby('r90s').agg(n=('pnl','size'),pnl=('pnl','mean'),coin=('coin_return','mean'))
    S2=D[D['a']<0].dropna(subset=['vol10','vol60','pnl']).copy()
    S2['vr']=pd.qcut(S2['vol10']/S2['vol60'],4,labels=False)
    out['short_by_volratio']=S2.groupby('vr').agg(n=('pnl','size'),pnl=('pnl','mean'),coin=('coin_return','mean'))
    L2=D[D['a']>0].dropna(subset=['vol10','vol60','pnl']).copy()
    L2['vr']=pd.qcut(L2['vol10']/L2['vol60'],4,labels=False)
    out['long_by_volratio']=L2.groupby('vr').agg(n=('pnl','size'),pnl=('pnl','mean'),coin=('coin_return','mean'))
    # non-overlapping 5-day grid: coin 5d return by r28 quintile, per coin pooled
    g=[]
    for (c,wi),x in D.groupby(['coin','wi']):
        x=x.reset_index(drop=True)
        cl=x['close'].values
        for i in range(0,len(x)-5,5):
            r28=cl[i]/cl[i-28]-1 if i>=28 else np.nan
            g.append((c,r28,cl[i+5]/cl[i]-1))
    G=pd.DataFrame(g,columns=['coin','r28','f5']).dropna()
    G['f5d']=G['f5']-G.groupby('coin')['f5'].transform('mean')
    G['q']=G.groupby('coin')['r28'].transform(lambda x:pd.qcut(x,5,labels=False))
    out['grid_by_r28q']=G.groupby('q').agg(n=('f5d','size'),f5d=('f5d','mean'),t=('f5d',lambda x:x.mean()/x.std()*np.sqrt(len(x))),r28=('r28','mean'))
    out['short_side_t_by_coin']=D[D['a']<0].groupby('coin')['pnl'].agg(['size','mean',lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    return out
