def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    F='forecast'; RAW='debug_info.components.above_ma.last_history_value'
    bars=data['bars']; days=data['days']
    # pooled mean daily return per coin
    mu={}
    for c in bars:
        rs=[]
        for w,df in bars[c].items():
            rs.append(df['close'].pct_change().dropna())
        mu[c]=pd.concat(rs).mean()
    rows=[]
    for c in bars:
        for w,df in bars[c].items():
            cl=df['close'].values; fc=df[F].values; raw=df[RAW].values if RAW in df else np.full(len(df),np.nan)
            n=len(df)
            for h in (5,20,60):
                for i in range(0,n-h,h):
                    r=cl[i+h]/cl[i]-1
                    rows.append(dict(coin=c,win=w,h=h,fc=fc[i],raw=raw[i],ex=r-h*mu[c],r=r,year=pd.Timestamp(df['timestamp'].iloc[i]).year))
    d=pd.DataFrame(rows)
    def summ(g):
        return pd.Series(dict(n=len(g),mean_ex=g.ex.mean(),med_ex=g.ex.median(),t=g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,share_beat=(g.ex>0).mean()))
    d['on']=d.fc>0
    out={}
    out['by_h_on']=d.groupby(['h','on']).apply(summ)
    d20=d[d.h==20].copy()
    pos=d20[d20.on].copy()
    pos['fq']=pd.qcut(pos.fc.rank(method='first'),4,labels=['q1','q2','q3','q4'])
    out['h20_fc_quart']=pos.groupby('fq').apply(summ)
    for h in (5,60):
        p=d[(d.h==h)&d.on].copy()
        p['fq']=pd.qcut(p.fc.rank(method='first'),4,labels=['q1','q2','q3','q4'])
        out[f'h{h}_fc_quart']=p.groupby('fq').apply(summ)
    out['h20_coin_on']=d20.groupby(['coin','on']).apply(summ)
    out['h20_year_on']=d20.groupby(['year','on']).apply(summ)
    # raw distance quartiles (unstandardised) among on bars
    pos['rq']=pd.qcut(pos.raw.rank(method='first'),4,labels=['r1','r2','r3','r4'])
    out['h20_raw_quart']=pos.groupby('rq').apply(summ)
    # book: market vs timing
    br=[];mk=[];
    for c in bars:
        for w,df in bars[c].items():
            dd=days[c][w].copy()
            b=df.copy(); b['day']=pd.to_datetime(b['timestamp']).dt.floor('D')
            al=b.groupby('day')['postRebalance_current_allocation'].last()
            dd['day']=pd.to_datetime(dd['day'])
            dd=dd.merge(al.rename('al').reset_index(),on='day',how='left')
            dd['al_prev']=dd['al'].shift(1)
            dd['mkt']=dd['al_prev']*mu[c]
            dd['coin']=c
            br.append(dd)
    B=pd.concat(br).dropna(subset=['book_return','al_prev'])
    out['book']=pd.Series(dict(book_mean=B.book_return.mean(),mkt_part=B.mkt.mean(),timing=B.book_return.mean()-B.mkt.mean(),mean_alloc=B.al_prev.mean(),share_inv=(B.al_prev>0).mean()))
    return out
