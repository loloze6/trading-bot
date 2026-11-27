import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        allret=[]
        for w,b in wins.items():
            r=b["close"].pct_change().dropna(); allret.append(r)
        drift=pd.concat(allret).mean()
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            nxt=b["close"].shift(-1)/b["close"]-1
            ret=b["close"].pct_change()
            sd=ret.rolling(30,min_periods=20).std()
            rng=(b["high"]-b["low"])
            cl=(b["high"]-b["close"])/rng.replace(0,np.nan)
            width=rng/b["close"]/sd
            raw=b.get("debug_info.components.wide_high_close.last_history_value")
            d=pd.DataFrame({"coin":coin,"win":w,"year":pd.to_datetime(b["timestamp"]).dt.year,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "fc":b["forecast"],"inprof":b["regime"]!="chop","cl":cl,"width":width,
                "raw":raw,"u":-(nxt-drift),"tot":-nxt,"prev":ret})
            rows.append(d.iloc[:-1])
    df=pd.concat(rows)
    df["absfc"]=-df["fc"]
    cases=df[df["fc"]<0].dropna(subset=["u"])
    prof=df[df["inprof"]].dropna(subset=["u","cl","width"])
    def summ(g):
        dd=g.groupby("day")["u"].sum()
        n=len(g); m=g["u"].mean()
        t=m*n/ (dd.std()*np.sqrt(len(dd))) if len(dd)>1 else np.nan
        return pd.Series({"n":n,"days":len(dd),"mean_u":m,"t":t})
    out={}
    out["cases_all"]=summ(cases)
    q=lambda s,k: pd.qcut(s.rank(method="first"),k,labels=False)
    c=cases.copy()
    c["fc_q"]=q(c["absfc"],4); c["cl_q"]=q(c["cl"],3); c["w_q"]=q(c["width"],3)
    out["by_fc_quartile"]=c.groupby("fc_q").apply(summ)
    out["by_cl_tercile"]=c.groupby("cl_q").apply(summ)
    out["by_width_tercile"]=c.groupby("w_q").apply(summ)
    out["by_coin"]=c.groupby("coin").apply(summ)
    out["by_year"]=c.groupby("year").apply(summ)
    out["corr_absfc_u"]=float(stats.spearmanr(c["absfc"],c["u"]).correlation)
    out["corr_width_u"]=float(stats.spearmanr(c["width"],c["u"]).correlation)
    out["corr_cl_u"]=float(stats.spearmanr(c["cl"],c["u"]).correlation)
    out["corr_raw_u"]=float(stats.spearmanr(c["raw"].dropna(),c.loc[c["raw"].notna(),"u"]).correlation)
    # whole profile: close location buckets, short-direction unusual move
    p=prof.copy()
    p["clb"]=pd.cut(p["cl"],[-0.01,0.1,0.25,0.5,0.75,0.9,1.01])
    out["profile_by_closeloc"]=p.groupby("clb").apply(summ)
    top=p[p["cl"]<=0.25].copy()
    top["w_q"]=q(top["width"],3)
    out["profile_top_by_width"]=top.groupby("w_q").apply(summ)
    top["pr_q"]=q(top["prev"],3)
    out["profile_top_by_dayret"]=top.groupby("pr_q").apply(summ)
    out["top_not_case"]=summ(top[top["fc"]>=0])
    return out
