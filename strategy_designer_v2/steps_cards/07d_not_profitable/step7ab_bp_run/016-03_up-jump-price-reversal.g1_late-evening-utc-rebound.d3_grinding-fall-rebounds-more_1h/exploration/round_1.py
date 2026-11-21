import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = list(days[coins[0]].keys())
    # book daily: mean across coins per (window, day)
    rows = []
    for c in coins:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    D = D.dropna(subset=["book_return"])
    B = D.groupby(["w","day"]).agg(book=("book_return","mean"), coin=("coin_return","mean")).reset_index()
    B["wn"] = B["w"].str[1:].astype(int)
    B = B.sort_values(["wn","day"]).reset_index(drop=True)
    B["eq"] = (1+B["book"]).cumprod(); B["peak"]=B["eq"].cummax(); B["dd"]=B["eq"]/B["peak"]-1
    B["heq"] = (1+B["coin"]).cumprod(); B["hdd"]=B["heq"]/B["heq"].cummax()-1
    yrs = len(B)/365
    out["summary"] = pd.Series({"days":len(B),"book_yearly":B["eq"].iloc[-1]**(1/yrs)-1,"book_maxdd":B["dd"].min(),
        "hold_yearly":B["heq"].iloc[-1]**(1/yrs)-1,"hold_maxdd":B["hdd"].min(),
        "book_sharpe":B.book.mean()/B.book.std()*np.sqrt(365),"hold_sharpe":B.coin.mean()/B.coin.std()*np.sqrt(365),
        "corr_book_hold":B.book.corr(B.coin)})
    # drawdown episodes
    B["year"]=pd.to_datetime(B["day"]).dt.year
    ep=[]; inDD=False
    for i,r in B.iterrows():
        if r.dd<0 and not inDD: inDD=True; s=i
        if r.dd==0 and inDD:
            inDD=False; seg=B.loc[s:i]; ep.append((seg.dd.min(),seg.w.iloc[0],seg.w.iloc[-1],seg.year.iloc[0],len(seg),
              (1+seg.coin).prod()-1, seg.book.sum(), seg.coin.sum()))
    if inDD:
        seg=B.loc[s:]; ep.append((seg.dd.min(),seg.w.iloc[0],seg.w.iloc[-1],seg.year.iloc[0],len(seg),(1+seg.coin).prod()-1,seg.book.sum(),seg.coin.sum()))
    E=pd.DataFrame(ep,columns=["depth","w_start","w_end","year","days","hold_ret","book_sum","coin_sum"]).sort_values("depth").head(8)
    out["deepest_falls"]=E
    # per window
    out["per_window"]=B.groupby("wn").agg(year=("year","first"),book_sum=("book","sum"),coin_sum=("coin","sum"),
        book_minDD=("dd","min"),n=("book","size"))
    # bar-level: position gain grouped by market state
    st=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.copy()
            cl=b["close"]
            r1=cl.pct_change()
            b["gain"]=b["postRebalance_current_allocation"]*(cl.shift(-1)/cl-1)
            b["ret7d"]=cl/cl.shift(168)-1
            b["ret24"]=cl/cl.shift(24)-1
            b["vol7d"]=r1.rolling(168).std()
            b["vol30d"]=r1.rolling(720).std()
            b["volratio"]=b["vol7d"]/b["vol30d"]
            b["ret30d"]=cl/cl.shift(720)-1
            b["coin"]=c; b["w"]=w
            st.append(b[["gain","ret7d","ret24","volratio","ret30d","postRebalance_current_allocation","forecast","coin","w"]])
    S=pd.concat(st).dropna()
    S["inpos"]=S.postRebalance_current_allocation.abs()>1e-6
    out["share_in_position"]=S.inpos.mean()
    P=S[S.inpos]
    for col in ["ret30d","ret7d","volratio","ret24"]:
        q=pd.qcut(P[col],5,labels=False,duplicates="drop")
        g=P.groupby(q).agg(lo=(col,"min"),hi=(col,"max"),mean_gain_bps=("gain",lambda x:x.mean()*1e4),
            n=("gain","size"),alloc=("postRebalance_current_allocation","mean"),total_share=("gain","sum"))
        g["total_share"]=g["total_share"]/P.gain.sum()
        out["gain_by_"+col]=g
    return out
