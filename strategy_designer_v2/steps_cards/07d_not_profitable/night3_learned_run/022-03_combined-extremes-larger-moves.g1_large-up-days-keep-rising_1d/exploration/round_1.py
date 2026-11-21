def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = list(days[coins[0]].keys())
    def wkey(w): return int(w[1:])
    wins = sorted(wins, key=wkey)
    out = {}
    # book daily returns: mean across coins per day per window
    chain = []; hchain=[]; winlab=[]
    for w in wins:
        br = pd.concat([days[c][w].set_index("day")["book_return"] for c in coins if w in days[c]], axis=1).mean(axis=1)
        hr = pd.concat([days[c][w].set_index("day")["coin_return"] for c in coins if w in days[c]], axis=1).mean(axis=1)
        br = br.dropna(); hr = hr.reindex(br.index)
        chain.append(br.values); hchain.append(hr.values); winlab += [w]*len(br)
    b = np.concatenate(chain); h = np.concatenate(hchain); winlab=np.array(winlab)
    v = np.cumprod(1+b); peak = np.maximum.accumulate(v); dd = v/peak-1
    hv = np.cumprod(1+h); hdd = hv/np.maximum.accumulate(hv)-1
    out["summary"] = pd.Series({"book_maxdd":dd.min(),"hold_maxdd":hdd.min(),
        "book_yearly":v[-1]**(365/len(b))-1,"hold_yearly":hv[-1]**(365/len(h))-1,"n_days":len(b)})
    # drawdown episodes
    eps=[]; i=0; n=len(dd)
    trough_idx = []
    # find top 5 episodes by depth
    inn=False
    for k in range(n):
        if dd[k]<0 and not inn: inn=True; s=k
        if dd[k]==0 and inn:
            inn=False; seg=dd[s:k]; j=s+np.argmin(seg); eps.append((seg.min(),s,j,k))
    if inn: seg=dd[s:]; j=s+np.argmin(seg); eps.append((seg.min(),s,j,n))
    eps=sorted(eps)[:6]
    rows=[]
    for d,s,j,e in eps:
        rows.append({"depth":d,"start_win":winlab[s],"trough_win":winlab[j],"days_to_trough":j-s+1,
                     "book_ret_fall":np.prod(1+b[s:j+1])-1,"hold_ret_fall":np.prod(1+h[s:j+1])-1})
    out["episodes"]=pd.DataFrame(rows)
    # per coin-day states
    recs=[]
    for c in coins:
        for w in bars[c]:
            df=bars[c][w].copy()
            cl=df["close"]; r=cl.pct_change()
            df["r30"]=cl/cl.shift(30)-1
            df["vol30"]=r.rolling(30).std()
            df["hi60"]=cl/cl.rolling(60,min_periods=20).max()-1
            df["r1"]=r
            df["pos"]=df["postRebalance_current_allocation"]
            df["gain"]=df["pos"]*(cl.shift(-1)/cl-1)
            df["fwd5"]=cl.shift(-5)/cl-1
            df["coin"]=c; df["win"]=w; df["i"]=np.arange(len(df))
            recs.append(df[["coin","win","i","r30","vol30","hi60","r1","pos","gain","fwd5","forecast"]])
    A=pd.concat(recs,ignore_index=True)
    drift5 = A[A.i%5==0].groupby("coin")["fwd5"].mean()
    A["ex5"]=A["fwd5"]-A["coin"].map(drift5)
    A["r30q"]=A.groupby("coin")["r30"].transform(lambda x: pd.qcut(x,5,labels=False,duplicates="drop"))
    A["volq"]=A.groupby("coin")["vol30"].transform(lambda x: pd.qcut(x,3,labels=False,duplicates="drop"))
    A["hiq"]=A.groupby("coin")["hi60"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    held=A[A.pos.abs()>0]
    for k in ["r30q","volq","hiq"]:
        g=held.groupby(k)["gain"]
        out["gain_by_"+k]=pd.DataFrame({"mean_gain":g.mean(),"n":g.size(),"t":g.mean()/(g.std()/np.sqrt(g.size())),
            "mean_pos":held.groupby(k)["pos"].mean(),"share_neg_days":g.apply(lambda x:(x<0).mean())})
    G=A[(A.i%5==0)&(A.forecast>0)].dropna(subset=["ex5"])
    for k in ["r30q","volq","hiq"]:
        g=G.groupby(k)
        out["case_ex5_by_"+k]=pd.DataFrame({"mean_ex5":g["ex5"].mean(),"mean_tot5":g["fwd5"].mean(),"n":g.size(),
            "t":g["ex5"].mean()/(g["ex5"].std()/np.sqrt(g.size())),
            "slope_t":g.apply(lambda x: stats.linregress(x.forecast,x.ex5).slope/stats.linregress(x.forecast,x.ex5).stderr if len(x)>10 else np.nan)})
    out["time_in_market"]=float((A.pos.abs()>0).mean())
    return out
