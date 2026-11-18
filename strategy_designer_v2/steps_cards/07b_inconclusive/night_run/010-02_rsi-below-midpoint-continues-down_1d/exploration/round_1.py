def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    fc='forecast'
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df['close'].values; f=df[fc].values
            raw=df['debug_info.components.rsi_below_share.last_history_value'].values
            n=len(df)
            # past 28-day return for regime
            for h in [1,3,7,14,21]:
                for i in range(0,n-h,h):
                    r28=c[i]/c[i-28]-1 if i>=28 else np.nan
                    rows.append(dict(coin=coin,w=w,wn=int(w[1:]),h=h,f=f[i],raw=raw[i],r=c[i+h]/c[i]-1,r28=r28,ts=df['timestamp'].iloc[i]))
    d=pd.DataFrame(rows)
    d['ex']=d['r']-d.groupby(['coin','h'])['r'].transform('mean')
    d['year']=pd.to_datetime(d['ts']).dt.year
    def slope_t(x):
        x=x.dropna(subset=['f','ex'])
        if len(x)<10 or x['f'].std()==0: return pd.Series({'n':len(x),'t':np.nan,'slope':np.nan})
        res=stats.linregress(x['f'],x['ex'])
        return pd.Series({'n':len(x),'t':res.slope/res.stderr,'slope':res.slope})
    out={}
    out['by_h']=d.groupby('h').apply(slope_t)
    d7=d[d.h==7].copy()
    out['h7_by_coin']=d7.groupby('coin').apply(slope_t)
    out['h7_by_year']=d7.groupby('year').apply(slope_t)
    d7['side']=np.sign(d7['f'])
    out['h7_by_side']=d7.groupby('side').apply(slope_t)
    out['h7_side_mean_ex']=d7.groupby('side')['ex'].agg(['count','mean','std'])
    d7['q']=pd.qcut(d7['f'].rank(method='first'),5,labels=False)
    out['h7_fquint_ex']=d7.groupby('q')['ex'].agg(['count','mean','std'])
    d7['rawq']=d7['raw'].round(3)
    out['h7_by_raw']=d7.groupby(pd.cut(d7['raw'],[-0.51,-0.3,-0.1,0.1,0.3,0.51]))['ex'].agg(['count','mean'])
    d7['trend']=np.where(d7['r28']>0,'up28','down28')
    out['h7_by_trend']=d7.groupby('trend').apply(slope_t)
    d14=d[d.h==14].copy(); d14['side']=np.sign(d14['f'])
    out['h14_by_side']=d14.groupby('side').apply(slope_t)
    out['h14_by_coin']=d14.groupby('coin').apply(slope_t)
    return out
