import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    # chained book, drawdown by window
    rows=[]
    for c in days:
        for w,d in days[c].items():
            dd=d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w; rows.append(dd)
    D=pd.concat(rows)
    D["wn"]=D.w.str[1:].astype(int)
    byday=D.groupby(["wn","day"])[["book_return","coin_return"]].mean().dropna().sort_index()
    eq=(1+byday.book_return).cumprod(); dd=eq/eq.cummax()-1
    trough=dd.idxmin(); peak=eq.loc[:trough].idxmax()
    out["dd"]=pd.Series({"maxdd":dd.min(),"peak_w":peak[0],"trough_w":trough[0],
        "yearly":(eq.iloc[-1])**(365/len(eq))-1})
    out["dd_by_window"]=byday.groupby(level=0).agg(book=("book_return","sum"),hold=("coin_return","sum")).T
    # per-bar gains by forecast bucket, and cells
    cells=[]; gains=[]
    for c in bars:
        r5all=[]
        for w,b in bars[c].items():
            cl=b.close.values
            for i in range(0,len(cl)-5,5): r5all.append(cl[i+5]/cl[i]-1)
        mu5=np.mean(r5all)
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            nxt=b.close.shift(-1)/b.close-1
            a=b.postRebalance_current_allocation.fillna(0)
            # forecast at entry of current holding: use forecast bucket of bar
            gains.append(pd.DataFrame({"g":a*nxt,"f":b.forecast,"a":a}))
            hi=b.high.rolling(30).max(); lo=b.low.rolling(30).min()
            nm=(b.close-b.close.shift(30)).abs()/(hi-lo)
            pos=(b.close-(hi+lo)/2)/(hi-lo)
            f10=b.close/b.close.shift(10)-1
            vol10=b.close.pct_change().rolling(60).std()*np.sqrt(10)
            f1=b.close/b.close.shift(1)-1
            f3=b.close/b.close.shift(3)-1
            cl=b.close.values
            for i in range(0,len(cl)-5,5):
                if b.forecast.iloc[i]>0:
                    cells.append(dict(f=b.forecast.iloc[i],ex=cl[i+5]/cl[i]-1-mu5,r5=cl[i+5]/cl[i]-1,
                        nm=nm.iloc[i],pos=pos.iloc[i],z=f10.iloc[i]/vol10.iloc[i],f3=f3.iloc[i]))
    G=pd.concat(gains)
    G["fb"]=pd.cut(G.f,[-1,0.001,5,10,15,21],labels=["0","0-5","5-10","10-15","15-20"])
    out["bar_gain_by_forecast"]=G.groupby("fb").agg(n=("g","size"),g_mean=("g","mean"),a=("a","mean"),g_sum=("g","sum"))
    A=pd.DataFrame(cells).dropna()
    A["deep"]=(A.f>=10).astype(int)
    A["nmhi"]=(A.nm>=A.nm.median()).astype(int)
    out["deep_x_nm"]=A.groupby(["deep","nmhi"]).agg(n=("ex","size"),ex=("ex","mean"),r5=("r5","mean"))
    A["f3q"]=pd.qcut(A.f3,3,labels=False)
    out["by_last3d"]=A.groupby("f3q").agg(n=("ex","size"),f3=("f3","mean"),ex=("ex","mean"))
    A["zq"]=pd.qcut(A.z,4,labels=False)
    out["by_fall_over_vol"]=A.groupby("zq").agg(n=("ex","size"),z=("z","mean"),ex=("ex","mean"))
    sl=stats.linregress(A.f,A.ex); out["slope_all"]=pd.Series({"slope":sl.slope,"t":sl.slope/sl.stderr,"n":len(A)})
    H=A[A.f>=10]; out["deep_mean_t"]=pd.Series({"n":len(H),"ex":H.ex.mean(),"t":H.ex.mean()/(H.ex.std()/np.sqrt(len(H))),"r5":H.r5.mean()})
    return out
