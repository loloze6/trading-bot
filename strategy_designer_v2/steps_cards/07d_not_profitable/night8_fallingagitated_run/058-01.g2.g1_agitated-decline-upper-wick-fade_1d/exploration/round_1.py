def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; dayrows=[]
    allret=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; r=c.pct_change()
            allret.append(r.dropna())
            sd30=r.rolling(30,min_periods=20).std()
            b["ret1"]=r; b["sd30"]=sd30
            b["gb"]=(b["high"]-c)/c/sd30
            b["r1s"]=r/sd30
            b["r3s"]=(c/c.shift(3)-1)/(sd30*np.sqrt(3))
            b["dd20"]=(c/c.rolling(20,min_periods=10).max()-1)/sd30
            for h in (1,2,3,5):
                b[f"f{h}"]=c.shift(-h)/c-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["gain"]=b["pos"]*b["f1"]
            b["coin"]=coin; b["w"]=w; b["i"]=np.arange(len(b))
            b["dow"]=pd.to_datetime(b["timestamp"]).dt.dayofweek
            b["yr"]=pd.to_datetime(b["timestamp"]).dt.year
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
        for w,d in data["days"][coin].items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; dayrows.append(d)
    B=pd.concat(rows,ignore_index=True)
    drift=pd.concat(allret).mean()
    inprof=B[B["regime"].isin(["trending","unknown"])].copy()
    cases=B[(B["regime"]=="trending")&(B["forecast"]<0)].copy()
    for h in (1,2,3,5): cases[f"u{h}"]=-(cases[f"f{h}"]-drift*h)
    out={}
    def grp(df,col,q=4,val="u1"):
        df=df.dropna(subset=[col,val]).copy()
        df["q"]=pd.qcut(df[col].rank(method="first"),q,labels=False)
        g=df.groupby("q")[val]
        return pd.DataFrame({"lo":df.groupby("q")[col].min(),"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    out["cases_horizon"]=pd.DataFrame({h:{"mean":cases[f"u{h}"].mean(),"t":cases[f"u{h}"].mean()/(cases[f"u{h}"].std()/np.sqrt(cases[f"u{h}"].notna().sum())),"n":cases[f"u{h}"].notna().sum()} for h in (1,2,3,5)}).T
    out["by_gb"]=grp(cases,"gb")
    out["by_r1s"]=grp(cases,"r1s")
    out["by_r3s"]=grp(cases,"r3s")
    out["by_dd20"]=grp(cases,"dd20")
    out["by_absfc"]=grp(cases.assign(af=cases["forecast"].abs()),"af")
    # condition alone: in-profile down days, long-side check
    dn=inprof[inprof["regime"]=="unknown"].copy(); dn["u1"]=-(dn["f1"]-drift)
    out["inprof_downdays_shortmove"]=pd.Series({"mean":dn["u1"].mean(),"n":dn["u1"].notna().sum()})
    # position gain by group (book-like)
    held=B[B["pos"].abs()>0]
    out["held_gain_by_coin"]=held.groupby("coin")["gain"].agg(["size","mean","sum"])
    out["held_gain_by_window"]=held.groupby("w")["gain"].agg(["size","mean","sum"])
    out["held_gain_by_year"]=held.groupby("yr")["gain"].agg(["size","mean","sum"])
    out["held_gain_by_dow"]=held.groupby("dow")["gain"].agg(["size","mean","sum"])
    out["held_by_r3s"]=grp(held.assign(g=held["gain"]),"r3s",val="g")
    # book daily
    D=pd.concat(dayrows,ignore_index=True)
    bk=D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    bk["wn"]=bk["w"].str[1:].astype(int); bk=bk.sort_values(["wn","day"])
    eq=(1+bk["book_return"].fillna(0)).cumprod(); dd=eq/eq.cummax()-1
    bk["dd"]=dd.values
    out["book_by_window"]=bk.groupby("w").agg(ret=("book_return",lambda x:(1+x.fillna(0)).prod()-1),coin=("coin_return",lambda x:(1+x.fillna(0)).prod()-1),mindd=("dd","min"))
    # deepest fall episode
    trough=bk["dd"].idxmin(); pos_t=list(bk.index).index(trough)
    peak_pos=int(np.argmax(eq.values[:pos_t+1]))
    seg=bk.iloc[peak_pos:pos_t+1]
    out["deepest_fall"]=pd.Series({"depth":bk["dd"].min(),"days":len(seg),"window":seg["w"].iloc[-1],"coin_ret_during":(1+seg["coin_return"].fillna(0)).prod()-1})
    # losing held bars: features
    held2=held.dropna(subset=["gain"])
    out["held_lose_vs_win_feats"]=held2.assign(win=held2["gain"]>0).groupby("win")[["r1s","r3s","gb","dd20","ret1"]].mean()
    return out
