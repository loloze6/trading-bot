import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            c = b["close"]
            b["r1"] = c.shift(-1)/c - 1
            for h in (2,3,5):
                b[f"r{h}"] = c.shift(-h)/c - 1
            b["ret30"] = c/c.shift(30) - 1
            b["ret1"] = c/c.shift(1) - 1
            lr = np.log(c).diff()
            b["vol30"] = lr.rolling(30).std()
            b["z1"] = b["ret1"]/b["vol30"]
            b["hi30"] = c/c.rolling(30).max() - 1
            b["alloc"] = b["postRebalance_current_allocation"]
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["pg"] = b["alloc"]*b["r1"]
            b["coin"] = coin; b["win"] = w
            b["pos"] = np.arange(len(b))
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
            d = data["days"][coin][w].copy(); d["coin"]=coin; d["win"]=w
            daily.append(d)
    B = pd.concat(rows, ignore_index=True)
    D = pd.concat(daily, ignore_index=True)
    bk = D.groupby(["win","day"]).agg(br=("book_return","mean"), cr=("coin_return","mean")).reset_index()
    bk["wn"] = bk["win"].str[1:].astype(int)
    bk = bk.sort_values(["wn","day"]).dropna()
    out["book_overall"] = pd.Series({"mean":bk.br.mean(),"sd":bk.br.std(),"sharpe":bk.br.mean()/bk.br.std()*np.sqrt(365),
        "hold_mean":bk.cr.mean(),"hold_sharpe":bk.cr.mean()/bk.cr.std()*np.sqrt(365),"n":len(bk)})
    eq = (1+bk.br).cumprod(); dd = eq/eq.cummax()-1
    bk["dd"]=dd.values
    out["by_window"] = bk.groupby("wn").agg(book=("br","mean"),hold=("cr","mean"),mindd=("dd","min"),n=("br","size"))
    out["deepest_dd"] = float(dd.min())
    # drawdown episode: from peak to trough
    t = dd.idxmin(); peak = eq.loc[:t].idxmax()
    ep = bk.loc[peak:t]
    out["dd_episode"] = pd.Series({"days":len(ep),"book_sum":ep.br.sum(),"hold_sum":ep.cr.sum(),"window_first":ep.wn.iloc[0],"window_last":ep.wn.iloc[-1]})
    # exposure & fees
    out["exposure"] = pd.Series({"share_bars_long":(B.alloc>0).mean(),"mean_alloc":B.alloc.mean(),"mean_alloc_when_long":B.loc[B.alloc>0,"alloc"].mean(),
        "mean_fee_per_bar":B.fee.mean(),"mean_gross_pg":B.pg.mean(),"share_fee_of_gross":B.fee.mean()/B.pg.mean() if B.pg.mean()!=0 else np.nan,
        "share_active_trending":(B.regime=="trending").mean(),"share_fc_pos":(B.forecast>0).mean()})
    A = B[B.forecast>0]
    out["active_fwd"] = pd.DataFrame({h:{"mean":A[h].mean(),"t":stats.ttest_1samp(A[h].dropna(),0).statistic,"n":A[h].notna().sum()} for h in ["r1","r2","r3","r5"]}).T
    # gain by forecast quintile
    A = A.copy(); A["fq"]=pd.qcut(A.forecast,5,labels=False,duplicates="drop")
    out["by_fc_q"] = A.groupby("fq").agg(fc=("forecast","mean"),r1=("r1","mean"),r3=("r3","mean"),alloc=("alloc","mean"),pg=("pg","mean"),fee=("fee","mean"),n=("r1","size"))
    # by ret30 strength and nearness to high
    A["r30q"]=pd.qcut(A.ret30,4,labels=False,duplicates="drop")
    out["by_ret30_q"] = A.groupby("r30q").agg(r30=("ret30","mean"),r1=("r1","mean"),r3=("r3","mean"),pg=("pg","mean"),n=("r1","size"))
    A["hiq"]=pd.qcut(A.hi30,4,labels=False,duplicates="drop")
    out["by_hi30_q"] = A.groupby("hiq").agg(hi=("hi30","mean"),r1=("r1","mean"),r3=("r3","mean"),pg=("pg","mean"),n=("r1","size"))
    A["vq"]=pd.qcut(A.vol30,4,labels=False,duplicates="drop")
    out["by_vol_q"] = A.groupby("vq").agg(v=("vol30","mean"),r1=("r1","mean"),pg=("pg","mean"),n=("r1","size"))
    # all trending down days vs non-trending down days next return
    B["down"]=B.ret1<0
    out["down_by_regime"] = B[B.down].groupby(B.ret30>0).agg(r1=("r1","mean"),r3=("r3","mean"),n=("r1","size"))
    out["pg_by_coin"] = B.groupby("coin").agg(pg=("pg","mean"),fee=("fee","mean"),r1=("r1","mean"))
    return out
