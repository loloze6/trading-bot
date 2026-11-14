import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]; samp=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            sp=b["debug_info.components.sma_cross.last_history_value"].astype(float)
            f=b["forecast"].astype(float)
            a=b["postRebalance_current_allocation"].astype(float)
            r1=c.shift(-1)/c-1
            v=b["postRebalance_total_value"].astype(float)
            br=v.shift(-1)/v-1
            dsp=sp-sp.shift(10)
            mom20=c/c.shift(20)-1
            vol=np.log(c).diff().rolling(20).std()
            hi=c/c.rolling(30,min_periods=10).max()-1
            df=pd.DataFrame(dict(coin=coin,w=w,f=f,a=a,r1=r1,gain=a*r1,br=br,sp=sp,dsp=dsp,mom20=mom20,vol=vol,hi=hi))
            rows.append(df)
            idx=np.arange(0,len(b)-10,10)
            fr=(c.shift(-10)/c-1).iloc[idx]
            s=df.iloc[idx].copy(); s["fr"]=fr.values
            samp.append(s)
    D=pd.concat(rows); S=pd.concat(samp)
    S["ex"]=S["fr"]-S.groupby("coin")["fr"].transform("mean")
    out={}
    D["fb"]=pd.cut(D["f"],[-0.1,0,5,10,15,20.1],labels=["0","0-5","5-10","10-15","15-20"])
    out["daily by forecast bucket"]=D.groupby("fb").agg(n=("br","count"),book=("br","mean"),coin=("r1","mean"),alloc=("a","mean"))
    on=S[S.f>0]
    def q(df,col,lab):
        g=df.dropna(subset=[col,"ex"]).copy()
        g["qq"]=pd.qcut(g[col],4,labels=False,duplicates="drop")
        t=g.groupby("qq").agg(n=("ex","count"),mid=(col,"median"),ex=("ex","mean"),sd=("ex","std"))
        t["t"]=t.ex/(t.sd/np.sqrt(t.n)); return t.drop(columns="sd")
    for col in ["sp","dsp","mom20","vol","hi"]:
        out["active 10bar excess by q "+col]=q(on,col,col)
    out["all samples excess by q dsp"]=q(S,"dsp","dsp")
    # book drawdown: daily book returns by window and coin
    D["yr"]=0
    out["book per coin"]=D.groupby("coin").agg(book=("br","mean"),coin=("r1","mean"),alloc=("a","mean"),
        bsh=("br",lambda x:x.mean()/x.std()*np.sqrt(365)),hsh=("r1",lambda x:x.mean()/x.std()*np.sqrt(365)))
    # worst 5% of book days: conditions
    act=D[D.a>0].dropna(subset=["br"])
    thr=act.br.quantile(0.05)
    worst=act[act.br<=thr]
    out["worst book days vs active"]=pd.DataFrame({"worst":worst[["sp","dsp","mom20","vol","hi","a"]].median(),"active":act[["sp","dsp","mom20","vol","hi","a"]].median()})
    # book gain by dsp sign while active
    act=act.copy(); act["dsign"]=np.sign(act.dsp)
    out["active daily by spread change sign"]=act.groupby("dsign").agg(n=("br","count"),book=("br","mean"),coin=("r1","mean"))
    act["volq"]=pd.qcut(act.vol,4,labels=False)
    out["active daily by vol q"]=act.groupby("volq").agg(n=("br","count"),book=("br","mean"),coin=("r1","mean"),alloc=("a","mean"),bsd=("br","std"))
    tr=pd.concat([t for wins in data["trades"].values() for t in wins.values()])
    out["trades"]=pd.Series(dict(n=len(tr),gross=tr.profit_loss_percent.mean(),net=tr.net_profit_loss_percent.mean()))
    return out
