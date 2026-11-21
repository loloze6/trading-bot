def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    days=data["days"]; bars=data["bars"]
    coins=list(days.keys())
    wins=sorted(set(w for c in coins for w in days[c].keys()), key=lambda s:int(s[1:]))
    rows=[]
    for c in coins:
        for w in days[c]:
            d=days[c][w].copy(); b=bars[c][w].copy()
            b['day']=pd.to_datetime(b['timestamp']).dt.floor('D')
            bb=b.groupby('day').last()[['postRebalance_current_allocation','forecast','sizing_realised_vol','close']]
            d['day']=pd.to_datetime(d['day']).dt.floor('D')
            d=d.merge(bb[['postRebalance_current_allocation','forecast','sizing_realised_vol']],left_on='day',right_index=True,how='left')
            d['alloc_prev']=d['postRebalance_current_allocation'].shift(1)
            d['fc_prev']=d['forecast'].shift(1)
            d['vol_prev']=d['sizing_realised_vol'].shift(1)
            d['r28_prev']=(d['close']/d['close'].shift(28)-1).shift(1)
            d['r5_prev']=(d['close']/d['close'].shift(5)-1).shift(1)
            d['r1_prev']=d['coin_return'].shift(1)
            d['coin']=c; d['win']=w; d['wi']=int(w[1:])
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    P=D.groupby(['wi','day'])['book_return'].mean().reset_index().sort_values(['wi','day'])
    P=P.dropna()
    eq=(1+P['book_return']).cumprod(); dd=eq/eq.cummax()-1
    P['dd']=dd.values
    yr=eq.iloc[-1]**(365/len(P))-1
    imin=dd.idxmin(); peak=eq.loc[:imin].idxmax()
    out={}
    out['summary']=pd.Series({'yearly':yr,'maxdd':dd.min(),'calmar':yr/-dd.min(),'ndays':len(P),
        'peak_wi':P.loc[peak,'wi'],'trough_wi':P.loc[imin,'wi'],'days_in_fall':imin-peak})
    # per window
    pw=P.groupby('wi').agg(ret=('book_return',lambda x:(1+x).prod()-1),mindd=('dd','min'),n=('book_return','size'))
    out['per_window']=pw
    # fall period days
    fall=P.loc[peak:imin,['wi','day']]
    Df=D.merge(fall,on=['wi','day'])
    Df['pnl']=Df['alloc_prev']*Df['coin_return']
    Df['side']=np.sign(Df['alloc_prev'])
    out['fall_by_side']=Df.groupby('side').agg(n=('pnl','size'),pnl_sum=('pnl','sum'),coin_ret_mean=('coin_return','mean'),absalloc=('alloc_prev',lambda x:x.abs().mean()))
    out['fall_by_coin']=Df.groupby('coin').agg(pnl_sum=('pnl','sum'),coin_cum=('coin_return',lambda x:(1+x).prod()-1),alloc=('alloc_prev','mean'))
    # all days
    D['pnl']=D['alloc_prev']*D['coin_return']
    D['side']=np.sign(D['alloc_prev'])
    out['all_by_side']=D.groupby('side').agg(n=('pnl','size'),pnl_mean=('pnl','mean'),pnl_std=('pnl','std'),coin_ret=('coin_return','mean'))
    D['fcq']=pd.qcut(D['fc_prev'],8,duplicates='drop')
    out['by_fc']=D.groupby('fcq').agg(n=('pnl','size'),pnl=('pnl','mean'),coin=('coin_return','mean'),alloc=('alloc_prev','mean'))
    D['volq']=D.groupby('coin')['vol_prev'].transform(lambda x:pd.qcut(x,4,labels=False,duplicates='drop'))
    out['by_vol']=D.groupby(['volq','side']).agg(n=('pnl','size'),pnl=('pnl','mean'),pstd=('pnl','std'),coin=('coin_return','mean')).reset_index()
    # 20 worst portfolio days
    w20=P.nsmallest(20,'book_return')[['wi','day']]
    Dw=D.merge(w20,on=['wi','day'])
    out['worst20_days']=pd.Series({'mean_book':P.nsmallest(20,'book_return')['book_return'].mean(),
        'share_long':(Dw['side']>0).mean(),'share_short':(Dw['side']<0).mean(),
        'coin_ret':Dw['coin_return'].mean(),'r28_prev':Dw['r28_prev'].mean(),'r5_prev':Dw['r5_prev'].mean(),
        'fc_prev':Dw['fc_prev'].mean(),'pnl_long':Dw.loc[Dw.side>0,'pnl'].sum(),'pnl_short':Dw.loc[Dw.side<0,'pnl'].sum()})
    return out
