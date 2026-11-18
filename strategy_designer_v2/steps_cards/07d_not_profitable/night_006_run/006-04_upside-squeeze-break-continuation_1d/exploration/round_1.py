def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily
    rows=[]
    for c in data["days"]:
        for w,d in data["days"][c].items():
            rows.append(d.assign(coin=c,window=w))
    D=pd.concat(rows)
    book=D.groupby(['window','day'])['book_return'].mean().dropna()
    hold=D.groupby(['window','day'])['coin_return'].mean().dropna()
    out['book_vs_hold']=pd.DataFrame({'mean':[book.mean(),hold.mean()],'std':[book.std(),hold.std()],
        'sharpe':[book.mean()/book.std()*np.sqrt(365),hold.mean()/hold.std()*np.sqrt(365)]},index=['book','hold'])
    # bar level
    B=[];
    for c in data["bars"]:
        cm=[]
        for w,b in data["bars"][c].items():
            b=b.copy(); b['coin']=c; b['window']=w
            b['r1']=b['close'].shift(-1)/b['close']-1
            for h in [1,3,5,10,20]:
                b[f'f{h}']=b['close'].shift(-h)/b['close']-1
            b['prevhi']=b['high'].rolling(20).max().shift(1)
            b['brk']=b['close']/b['prevhi']-1
            b['ret20']=b['close']/b['close'].shift(20)-1
            b['vol20']=np.log(b['close']).diff().rolling(20).std()
            b['volu']=b['volume'].rolling(5).mean()/b['volume'].rolling(50).mean()
            b['pos_i']=np.arange(len(b))
            B.append(b)
    B=pd.concat(B,ignore_index=True)
    B['alloc']=B['postRebalance_current_allocation']
    B['gain']=B['alloc']*B['r1']
    B['fee']=(B['total_portfolio_value']-B['postRebalance_total_value'])/B['total_portfolio_value']
    cmean=B.groupby('coin')['r1'].mean()
    B['mkt']=B['alloc']*B['coin'].map(cmean)
    out['bar_gain']=pd.Series({'mean_gain':B['gain'].mean(),'mkt_part':B['mkt'].mean(),'timing':B['gain'].mean()-B['mkt'].mean(),
        'fee_mean':B['fee'].mean(),'share_bars_inpos':(B['alloc'].abs()>1e-6).mean(),'mean_alloc_when_in':B.loc[B['alloc']>1e-6,'alloc'].mean()})
    # gain by regime / forecast on
    B['on']=B['forecast']>0
    B['held']=B['alloc']>1e-6
    out['gain_by_on_held']=B.groupby(['on','held']).agg(n=('gain','size'),gain=('gain','mean'),r1=('r1','mean'),alloc=('alloc','mean'),fee=('fee','mean'))
    # consecutive break bars: run length
    out['per_coin']=B.groupby('coin').agg(gain=('gain','mean'),fee=('fee','mean'),onshare=('on','mean'),r1_on=('r1',lambda s: s[B.loc[s.index,'on']].mean()),r1_all=('r1','mean'))
    # forward returns after break bars, all bars (overlapping ok descriptive) by compression quintile
    on=B[B['on']].copy()
    on['cq']=pd.qcut(on['debug_info.components.compression.last_history_value'],4,labels=False,duplicates='drop')
    g={}
    for h in [1,3,5,10,20]:
        on[f'x{h}']=on[f'f{h}']-on['coin'].map(B.groupby('coin')[f'f{h}'].mean())
    out['fwd_excess_by_cq']=on.groupby('cq')[['x1','x3','x5','x10','x20']].mean().assign(n=on.groupby('cq').size())
    on['fq']=pd.qcut(on['forecast'],4,labels=False,duplicates='drop')
    out['fwd_excess_by_forecastq']=on.groupby('fq')[['x1','x3','x5','x10','x20']].mean().assign(n=on.groupby('fq').size(),gain=on.groupby('fq')['gain'].mean())
    on['bq']=pd.qcut(on['brk'],4,labels=False)
    out['fwd_excess_by_breaksize']=on.groupby('bq')[['x1','x3','x5','x10','x20']].mean().assign(brk=on.groupby('bq')['brk'].mean())
    on['rq']=pd.qcut(on['ret20'],4,labels=False)
    out['fwd_excess_by_ret20']=on.groupby('rq')[['x1','x3','x5','x10','x20']].mean().assign(r20=on.groupby('rq')['ret20'].mean())
    out['fwd_excess_overall']=on[['x1','x3','x5','x10','x20']].agg(['mean','count'])
    # first break vs continuation
    B['prev_on']=B.groupby(['coin','window'])['on'].shift(1).fillna(False)
    on['first']=~B.loc[on.index,'prev_on'].astype(bool)
    out['fwd_by_first']=on.groupby('first')[['x1','x3','x5','x10','x20']].mean().assign(n=on.groupby('first').size())
    T=[]
    for c in data["trades"]:
        for w,t in data["trades"][c].items(): T.append(t)
    T=pd.concat(T)
    out['trades']=pd.Series({'n':len(T),'gross':T['profit_loss_percent'].mean(),'net':T['net_profit_loss_percent'].mean(),'dur_days':T['duration_minutes'].mean()/1440,'win':(T['net_profit_loss_percent']>0).mean()})
    return out
