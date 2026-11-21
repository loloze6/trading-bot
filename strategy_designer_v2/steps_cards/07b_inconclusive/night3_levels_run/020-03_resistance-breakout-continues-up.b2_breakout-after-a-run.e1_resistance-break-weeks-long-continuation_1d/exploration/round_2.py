def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    col='debug_info.components.res_break.last_history_value'
    out={}
    H=[20,40]
    drift={}; usual={}
    for c,ws in data['bars'].items():
        for h in H:
            r=[]
            for w,df in ws.items():
                cl=df['close'].values
                idx=np.arange(0,len(cl)-h,h)
                r+=list(cl[idx+h]/cl[idx]-1)
            drift[(c,h)]=np.mean(r); usual[(c,h)]=np.std(r)
    rows=[]
    allx=[]
    for c,ws in data['bars'].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            cl=df['close'].values; raw=df[col].fillna(0).values
            n=len(df)
            ma50=pd.Series(cl).rolling(50).mean().values
            for i in np.where(raw>0)[0]:
                rec={'coin':c,'win':w,'raw':raw[i],'cell':i//20,'wlen':n}
                rec['p30']=cl[i]/cl[i-30]-1 if i>=30 else np.nan
                rec['p60']=cl[i]/cl[i-60]-1 if i>=60 else np.nan
                rec['ma50']=cl[i]/ma50[i]-1 if i>=49 else np.nan
                for h in H:
                    rec[f'x{h}']=(cl[i+h]/cl[i]-1-drift[(c,h)]) if i+h<n else np.nan
                rows.append(rec)
    d=pd.DataFrame(rows)
    cases=d.groupby(['coin','win','cell']).first().reset_index()
    def tt(s):
        s=s.dropna(); return pd.Series({'n':len(s),'mean':s.mean(),'t':s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out['wlen']=cases['wlen'].describe()
    for v in ['p30','p60','ma50']:
        q=pd.qcut(cases[v],3,labels=False)
        for h in H:
            out[f'{v}_x{h}']=cases.groupby(q)[f'x{h}'].apply(tt).unstack()
    # graded: correlation of p30 with x20 overall
    out['spear_p30_x20']=stats.spearmanr(cases['p30'],cases['x20'],nan_policy='omit')[0]
    out['spear_ma50_x20']=stats.spearmanr(cases['ma50'],cases['x20'],nan_policy='omit')[0]
    # inside uptrend (p30>0) raw split
    up=cases[cases['p30']>0].copy()
    up['rh']=up['raw']>up['raw'].median()
    out['up_rawhalf_x20']=up.groupby('rh')['x20'].apply(tt).unstack()
    out['up_by_coin_x20']=up.groupby('coin')['x20'].apply(tt).unstack()
    out['dn_x20']=tt(cases[cases['p30']<=0]['x20'])
    return out
