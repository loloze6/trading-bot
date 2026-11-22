def explore(data):
    import numpy as np, pandas as pd
    col='debug_info.components.fail_depth.last_history_value'
    rows=[]; cases=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            n=len(b); c=b['close'].values; h=b['high'].values; l=b['low'].values
            # recompute raw situation from prices
            hh=pd.Series(h).rolling(20).max().shift(1).values
            brk=c>hh
            sit=np.zeros(n,bool); dep=np.zeros(n)
            for t in range(n):
                for k in range(0,4):
                    j=t-k
                    if j<0: break
                    if brk[j]:
                        if c[t]<l[j]:
                            sit[t]=True; dep[t]=(l[j]-c[t])/l[j]*100
                        break
            raw=b[col].values if col in b else np.full(n,np.nan)
            f=b['forecast'].values
            yr=pd.to_datetime(b['timestamp']).dt.year.values
            grid=np.arange(0,n-5,5)
            fwd=np.array([c[g+5]/c[g]-1 for g in grid])
            for i,g in enumerate(grid):
                cell=slice(g,g+5)
                rows.append(dict(coin=coin,w=w,year=yr[g],grid_fc=f[g]<0,grid_sit=sit[g],
                                 cell_sit=sit[cell].any(),cell_fc=(f[cell]<0).any(),ret=fwd[i]))
            cases.append(dict(coin=coin,w=w,year=yr[0],bars=n,breakouts=int(brk.sum()),
                              sit_price=int(sit.sum()),sit_raw=int(np.nansum(raw>0)),fc_neg=int((f<0).sum()),
                              grid_fc=int(sum(f[g]<0 for g in grid)),grid_sit=int(sum(sit[g] for g in grid))))
    R=pd.DataFrame(rows); C=pd.DataFrame(cases)
    R['ex']=R['ret']-R.groupby('coin')['ret'].transform('mean')
    out={}
    out['per_coin']=C.groupby('coin')[['bars','breakouts','sit_price','sit_raw','fc_neg','grid_fc','grid_sit']].sum()
    out['per_year']=C.groupby('year')[['bars','breakouts','sit_price','fc_neg','grid_fc']].sum()
    out['per_window']=C.groupby('w')[['bars','breakouts','sit_price','fc_neg','grid_fc']].sum()
    def st(m):
        x=R.loc[m,'ex']; return pd.Series(dict(n=len(x),mean=x.mean(),sd=x.std(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>1 else np.nan))
    out['outcome']=pd.DataFrame({'grid_fc':st(R.grid_fc),'grid_sit':st(R.grid_sit),'cell_sit':st(R.cell_sit),'cell_fc':st(R.cell_fc),'all':st(R.ret.notna())}).T
    out['sit_rate_per_coin_year']=float(C.sit_price.sum()/(C.bars.sum()/365)/1)
    out['fc_neg_vs_sit']=f"fc<0 bars {C.fc_neg.sum()}, sit price bars {C.sit_price.sum()}, raw>0 {C.sit_raw.sum()}"
    return out
