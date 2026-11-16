def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily (equal-weight across coins per day within window)
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna().reset_index()
    B["wn"]=B.w.str[1:].astype(int)
    out["book_by_window"] = B.groupby("wn").agg(book_mean=("book_return","mean"), hold_mean=("coin_return","mean"), n=("book_return","size"), book_sum=("book_return","sum"), hold_sum=("coin_return","sum")).round(5)
    # bar-level position gain with states
    br=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.copy()
            r=b.close.pct_change()
            nxt=b.close.shift(-1)/b.close-1
            a=b.postRebalance_current_allocation
            g=a*nxt
            fee=(b.total_portfolio_value-b.postRebalance_total_value)/b.total_portfolio_value
            vol=r.rolling(20).std()
            z=r/vol
            ret20=b.close/b.close.shift(20)-1
            ret5=b.close/b.close.shift(5)-1
            sma50=b.close.rolling(50).mean()
            br.append(pd.DataFrame({"coin":c,"w":w,"a":a,"g":g,"nxt":nxt,"fee":fee,"z":z,"ret20":ret20/(vol*np.sqrt(20)),"ret5":ret5/(vol*np.sqrt(5)),"abv50":(b.close>sma50).where(sma50.notna()),"fc":b.forecast,"reg":b.regime}))
    X=pd.concat(br)
    act=X[X.a.abs()>0.01].dropna(subset=["g"])
    out["active_summary"]=pd.Series({"active_bars":len(act),"mean_gain":act.g.mean(),"t":act.g.mean()/act.g.std()*np.sqrt(len(act)),"mean_fee_all_bars":X.fee.mean(),"mean_alloc_active":act.a.mean(),"share_bars_active":len(act)/len(X)})
    act=act.copy()
    act["ret20q"]=pd.qcut(act.ret20,5,labels=False,duplicates="drop")
    out["by_ret20_quintile"]=act.groupby("ret20q").agg(n=("g","size"),gain=("g","mean"),nxt=("nxt","mean"),t=("nxt",lambda s:s.mean()/s.std()*np.sqrt(len(s)))).round(5)
    act["ret5q"]=pd.qcut(act.ret5,5,labels=False,duplicates="drop")
    out["by_ret5_quintile"]=act.groupby("ret5q").agg(n=("g","size"),gain=("g","mean"),nxt=("nxt","mean")).round(5)
    out["by_above_sma50"]=act.groupby("abv50").agg(n=("g","size"),gain=("g","mean"),nxt=("nxt","mean"),t=("nxt",lambda s:s.mean()/s.std()*np.sqrt(len(s)))).round(5)
    act["fcq"]=pd.qcut(act.fc,4,labels=False,duplicates="drop")
    out["by_forecast_q"]=act.groupby("fcq").agg(n=("g","size"),gain=("g","mean"),nxt=("nxt","mean"),fc=("fc","mean")).round(5)
    # worst losses: coin bars' active gain ranks
    act["zq"]=pd.qcut(act.z,4,labels=False,duplicates="drop")
    out["by_z_q"]=act.groupby("zq").agg(n=("g","size"),gain=("g","mean"),nxt=("nxt","mean"),z=("z","mean")).round(5)
    # book deepest falls: chain per window, worst 3-day stretches
    B=B.sort_values(["wn","day"])
    B["r3"]=B.groupby("wn").book_return.transform(lambda s:(1+s).rolling(3).apply(np.prod,raw=True)-1)
    worst=B.nsmallest(15,"r3")
    out["worst3d_book_vs_hold"]=pd.Series({"book_r3_mean":worst.r3.mean(),"hold_r3_mean":B.loc[worst.index,"coin_return"].mean()})
    out["mean_hold_daily"]=B.coin_return.mean()
    return out
