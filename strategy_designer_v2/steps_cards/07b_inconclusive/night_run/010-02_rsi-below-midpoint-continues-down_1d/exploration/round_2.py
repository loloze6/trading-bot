def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df['close'].values; f=df['forecast'].values
            raw=df['debug_info.components.rsi_below_share.last_history_value'].values
            n=len(df)
            for h in [1,3,7]:
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,f=f[i],raw=raw[i],r=c[i+h]/c[i]-1,ts=df['timestamp'].iloc[i]))
    d=pd.DataFrame(rows)
    d['ex']=d['r']-d.groupby(['coin','h'])['r'].transform('mean')
    d['year']=pd.to_datetime(d['ts']).dt.year
    def st(x,col='f'):
        x=x.dropna(subset=[col,'ex'])
        if len(x)<10 or x[col].std()==0: return pd.Series({'n':len(x),'t':np.nan})
        res=stats.linregress(x[col],x['ex'])
        return pd.Series({'n':len(x),'t':res.slope/res.stderr,'slope':res.slope})
    out={}
    out['by_h_ex2025']=d[d.year!=2025].groupby('h').apply(st)
    out['by_h_year_t']=d.groupby(['h','year']).apply(st)['t'].unstack(0)
    # raw-share slope (negated raw => same sign as f)
    d['nr']=-d['raw']
    out['by_h_rawslope']=d.groupby('h').apply(lambda x: st(x,'nr'))
    d7=d[d.h==7].copy()
    d7['ext']=np.where(d7['raw'].abs()>=0.3,'extreme','middle')
    out['h7_ext']=d7.groupby('ext').apply(lambda x: st(x,'nr'))
    out['h7_ext_side']=d7.groupby(['ext',np.sign(d7['raw'])])['ex'].agg(['count','mean','std'])
    d7['wn']=d7['w'].str[1:].astype(int)
    out['h7_window_t_pos_share']=float((d7.groupby('wn').apply(st)['t']>0).mean())
    return out
