def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    col='debug_info.components.res_break.last_history_value'
    out={}
    H=[5,10,20,40]
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
    for c,ws in data['bars'].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            cl=df['close'].values; raw=df[col].fillna(0).values if col in df else np.zeros(len(df))
            fc=df['forecast'].values
            yr=pd.to_datetime(df['timestamp']).dt.year.values
            n=len(df)
            for i in np.where(raw>0)[0]:
                rec={'coin':c,'win':w,'year':yr[i],'raw':raw[i],'fc':fc[i],'cell':i//20}
                rec['prior20']=cl[i]/cl[i-20]-1 if i>=20 else np.nan
                rec['prior90']=cl[i]/cl[i-90]-1 if i>=90 else np.nan
                for h in H:
                    rec[f'x{h}']=(cl[i+h]/cl[i]-1-drift[(c,h)]) if i+h<n else np.nan
                    rec[f's{h}']=rec[f'x{h}']/usual[(c,h)] if i+h<n else np.nan
                rows.append(rec)
    d=pd.DataFrame(rows)
    cases=d.groupby(['coin','win','cell']).first().reset_index()
    def tt(s):
        s=s.dropna(); return pd.Series({'n':len(s),'mean':s.mean(),'t':s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out['n_raw_bars']=len(d)
    out['fc_dist']=cases['fc'].describe()
    out['by_h']=pd.DataFrame({h:tt(cases[f'x{h}']) for h in H}).T
    out['strength_by_h']=pd.DataFrame({h:tt(cases[f's{h}']) for h in H}).T
    cases['rawq']=pd.qcut(cases['raw'].rank(method='first'),4,labels=False)
    out['by_rawq_20']=cases.groupby('rawq')['x20'].apply(tt).unstack().join(cases.groupby('rawq')['raw'].median())
    out['by_rawq_10']=cases.groupby('rawq')['x10'].apply(tt).unstack()
    out['by_coin_20']=cases.groupby('coin')['x20'].apply(tt).unstack()
    out['by_year_20']=cases.groupby('year')['x20'].apply(tt).unstack()
    cases['p20q']=pd.qcut(cases['prior20'],3,labels=False)
    out['by_prior20_20']=cases.groupby('p20q')['x20'].apply(tt).unstack()
    cases['p90q']=pd.qcut(cases['prior90'],3,labels=False)
    out['by_prior90_20']=cases.groupby('p90q')['x20'].apply(tt).unstack()
    out['corr_raw_x20']=stats.spearmanr(cases['raw'],cases['x20'],nan_policy='omit')[0]
    return out
