def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    ev=[]
    for c in data["bars"]:
        for w in data["bars"][c]:
            b = data["bars"][c][w].reset_index(drop=True)
            cl = b["close"].values; n=len(b)
            vol = b["volume"]
            vr = (vol/vol.rolling(90,min_periods=22).mean()).values
            isnh = (b["regime"]=="trending").values
            last=-10**9
            for i in range(n):
                if isnh[i] and i-last>=30 and i+30<n:
                    last=i
                    r=lambda a,z: cl[i+z]/cl[i+a]-1
                    ev.append(dict(coin=c,win=w,fc=b["forecast"].iloc[i],vr=vr[i],
                        d0_2=r(0,2),d2_10=r(2,10),d10_30=r(10,30),d0_30=r(0,30),
                        nh_next30=isnh[i+1:i+31].sum(),
                        held_days=(b["postRebalance_current_allocation"].iloc[i:i+31].abs()>1e-6).sum(),
                        mdd30=(cl[i:i+31]/np.maximum.accumulate(cl[i:i+31])-1).min()))
    E=pd.DataFrame(ev)
    med=E["fc"].median()
    E["hi"]=E["fc"]>med
    g=E.groupby("hi")[["d0_2","d2_10","d10_30","d0_30","nh_next30","held_days","mdd30"]].mean()
    g["n"]=E.groupby("hi").size()
    out["breakout events (30-bar spaced) by high forecast"]=g
    for col in ["d0_2","d2_10","d10_30","d0_30"]:
        a=E.loc[E.hi,col];bb=E.loc[~E.hi,col]
        out["t all "+col]=pd.Series({"t_mean_all":stats.ttest_1samp(E[col],0).statistic,"welch_hi_lo":stats.ttest_ind(a,bb,equal_var=False).statistic,"n":len(E)})
    E["vq"]=pd.qcut(E["vr"].rank(method="first"),3,labels=False)
    out["by raw volume ratio tercile"]=E.groupby("vq")[["vr","d0_2","d2_10","d10_30","d0_30","mdd30"]].mean()
    # book drawdown chain
    rows=[]
    for c in data["days"]:
        for w in data["days"][c]:
            d=data["days"][c][w].copy(); d["coin"]=c; d["win"]=w; rows.append(d)
    D=pd.concat(rows)
    D["wn"]=D["win"].str[1:].astype(int)
    P=D.groupby(["wn","day"])["book_return"].mean().dropna().reset_index().sort_values(["wn","day"])
    eq=(1+P["book_return"]).cumprod().values
    dd=eq/np.maximum.accumulate(eq)-1
    i=dd.argmin(); pk=np.argmax(eq[:i+1])
    out["deepest fall"]=pd.Series({"dd":dd[i],"len days":i-pk,"windows":f"w{P['wn'].iloc[pk]}->w{P['wn'].iloc[i]}","share of days book flat":(P["book_return"]==0).mean(),"mean":P["book_return"].mean()})
    seg=P.iloc[pk:i+1]
    out["fall: days with loss, sum loss"]=pd.Series({"loss days":(seg.book_return<0).sum(),"sum":seg.book_return.sum(),"worst":seg.book_return.min()})
    return out
