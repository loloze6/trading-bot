import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    # ---- book daily returns, combined across coins
    dfs = []
    for c in coins:
        for w, d in days[c].items():
            x = d[["day","book_return","coin_return"]].copy(); x["w"]=w; x["coin"]=c
            dfs.append(x)
    D = pd.concat(dfs)
    wnum = lambda w: int(w[1:])
    comb = D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    comb["wn"]=comb.w.map(wnum); comb=comb.sort_values(["wn","day"]).dropna()
    sh = lambda r: r.mean()/r.std()*np.sqrt(365)
    out["sharpe book/hold"] = pd.Series({"book":sh(comb.book_return),"hold":sh(comb.coin_return),
        "book_mean":comb.book_return.mean(),"hold_mean":comb.coin_return.mean()})
    # drawdown on chained book
    v = (1+comb.book_return).cumprod().values
    peak = np.maximum.accumulate(v); dd = v/peak-1
    comb["dd"]=dd
    # find top 5 distinct falls: segments from peak to trough
    segs=[]; i=0; n=len(v)
    in_dd=False
    for k in range(n):
        if dd[k]<0 and not in_dd: start=k; in_dd=True
        if in_dd and (dd[k]==0 or k==n-1):
            seg=slice(start,k+1); trough=start+np.argmin(dd[seg])
            segs.append((dd[trough],start,trough)); in_dd=False
    segs=sorted(segs)[:6]
    rows=[]
    for depth,s,t in segs:
        sub=comb.iloc[s:t+1]
        rows.append({"depth":depth,"days":t-s+1,"windows":",".join(sorted(set(sub.w),key=wnum)),
                     "book_cum":(1+sub.book_return).prod()-1,"coin_cum":(1+sub.coin_return).prod()-1})
    out["deepest falls"]=pd.DataFrame(rows)
    # ---- bar level: allocation, decomposition, cases
    caseRows=[]; barRows=[]
    for c in coins:
        allr=[]
        for w,b in bars[c].items():
            r=b.close.pct_change().shift(-1); allr.append(r)
        mu=pd.concat(allr).mean()
        g24=[]
        for w,b in bars[c].items():
            cl=b.close.values; idx=np.arange(0,len(cl)-24,24)
            g24.append(cl[idx+24]/cl[idx]-1)
        g24=np.concatenate(g24); drift=g24.mean(); usd=g24.std()
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            a=b.postRebalance_current_allocation.fillna(0)
            r=b.close.pct_change().shift(-1)
            barRows.append(pd.DataFrame({"a":a,"r":r,"mu":mu,"w":w,"coin":c}))
            cl=b.close; lr=np.log(cl).diff()
            ret720=cl/cl.shift(720)-1
            ret168=cl/cl.shift(168)-1
            vol=lr.rolling(720,min_periods=200).std()
            f=b.forecast.fillna(0).values
            # cases: first bet per grid cell
            low=0.0; cells=set()
            for k in range(len(b)):
                if f[k]<=0: low=0.0; continue
                if f[k]-low>=2:
                    cell=k//24
                    if cell not in cells and k+24<len(b):
                        cells.add(cell)
                        fr=cl.iloc[k+24]/cl.iloc[k]-1
                        caseRows.append({"coin":c,"w":w,"f":f[k],"fr":fr,"un":fr-drift,"s":(fr-drift)/usd,
                          "r30":ret720.iloc[k],"r7":ret168.iloc[k],"vol":vol.iloc[k],
                          "hour":b.timestamp.iloc[k].hour,"year":b.timestamp.iloc[k].year,
                          "h1":lr.iloc[k]})
                    low=f[k]
                low=min(low,f[k])
    B=pd.concat(barRows).dropna()
    out["bar decomposition"]=pd.Series({"mean_gain":(B.a*B.r).mean(),"market":(B.a*B.mu).mean(),
        "timing":(B.a*(B.r-B.mu)).mean(),"mean_alloc":B.a.mean(),"share_bars_in":(B.a.abs()>1e-6).mean()})
    C=pd.DataFrame(caseRows)
    def grp(col,q=5):
        x=C.dropna(subset=[col]).copy(); x["g"]=pd.qcut(x[col],q,duplicates="drop")
        G=x.groupby("g").agg(n=("un","size"),mean_un=("un","mean"),mean_tot=("fr","mean"),
            strength=("s","mean"),sd=("s","std"))
        G["t"]=G.strength/(G.sd/np.sqrt(G.n)); return G.drop(columns="sd").reset_index().astype({"g":str})
    out["cases by 30d return"]=grp("r30")
    out["cases by 7d return"]=grp("r7")
    out["cases by 30d vol"]=grp("vol")
    out["cases by forecast"]=grp("f")
    out["cases by year"]=C.groupby("year").agg(n=("un","size"),mean_un=("un","mean"),mean_tot=("fr","mean")).reset_index()
    return out
