import numpy as np, pandas as pd

def explore(data):
    rows=[]
    H=[5,10]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].values; n=len(df)
            r=pd.Series(c).pct_change()
            sd30=r.rolling(30).std()
            hi20=pd.Series(c).shift(1).rolling(20).max()
            sd20=r.rolling(20).std()
            dist=(pd.Series(c)-hi20)/hi20/sd20
            for h in H:
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                        day=str(pd.Timestamp(df["timestamp"].iloc[i]).date()),
                        ret=c[i+h]/c[i]-1,reg=df["regime"].iloc[i],fc=df["forecast"].iloc[i],
                        raw=df["debug_info.components.near_high.last_history_value"].iloc[i],
                        mydist=dist.iloc[i],sd30=sd30.iloc[i]))
    R=pd.DataFrame(rows)
    R["drift"]=R.groupby(["coin","h"])["ret"].transform("mean")
    R["ex"]=R["ret"]-R["drift"]
    P=R[(R.reg=="unknown")&R.fc.notna()].copy()
    def slope(d,col):
        d=d.dropna(subset=[col,"ex"])
        if len(d)<20 or d[col].std()==0: return pd.Series(dict(n=len(d),slope=np.nan,t=np.nan))
        x=d[col]-d[col].mean(); b=(x*d.ex).sum()/(x*x).sum()
        e=d.ex-d.ex.mean()-b*x
        g=(x*e).groupby(d.day).sum(); se=np.sqrt((g**2).sum())/(x*x).sum()
        return pd.Series(dict(n=len(d),slope=b,t=b/se))
    def mt(s):
        return pd.Series(dict(n=len(s),mean=s.mean(),t=s.mean()/s.std()*np.sqrt(len(s))))
    out={}
    for h in H:
        Ph=P[P.h==h].copy()
        Ph["bin"]=pd.cut(Ph.raw,[-99,-3,-2,-1,-0.5,0,0.5,99])
        out[f"rawbins_h{h}"]=Ph.groupby("bin")["ex"].apply(mt).unstack()
        out[f"slope_raw_above0_h{h}"]=slope(Ph[Ph.raw>0],"raw")
        out[f"slope_raw_above-1_h{h}"]=slope(Ph[Ph.raw>-1],"raw")
        out[f"above0_minus_rest_h{h}"]=Ph[Ph.raw>0].ex.mean()-Ph[Ph.raw<=0].ex.mean()
        Ph["yr"]=Ph.year
        out[f"above0_by_year_h{h}"]=Ph[Ph.raw>0].groupby("yr")["ex"].apply(mt).unstack()
        out[f"below_by_year_h{h}"]=Ph[Ph.raw<=0].groupby("yr")["ex"].apply(mt).unstack()
    P10=P[P.h==10]
    out["slope_fc_h10_by_year"]=P10.groupby("year").apply(lambda d: slope(d,"fc"))
    out["slope_fc_h10_by_coin"]=P10.groupby("coin").apply(lambda d: slope(d,"fc"))
    return out
