import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]; trades=[]; book=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            b=b.copy().reset_index(drop=True)
            c=b["close"]
            r1=c.pct_change()
            vol=r1.rolling(20).std()
            z=r1/vol
            r90=c/c.shift(90)-1
            r30=c/c.shift(30)-1
            f1=c.shift(-1)/c-1
            f3=c.shift(-3)/c-1
            f5=c.shift(-5)/c-1
            alloc=b["postRebalance_current_allocation"]
            pnl=alloc*f1
            d=pd.DataFrame({"coin":coin,"w":w,"z":z,"r1":r1,"r90":r90,"r30":r30,"f1":f1,"f3":f3,"f5":f5,
                            "alloc":alloc,"pnl":pnl,"fc":b["forecast"],"regime":b["regime"],"vol":vol,
                            "pos":np.arange(len(b))})
            rows.append(d)
            t=data["trades"][coin][w]
            if len(t): trades.append(t.assign(coin=coin))
            dd=data["days"][coin][w]
            book.append(dd.assign(coin=coin,w=w))
    D=pd.concat(rows)
    mu1=D.groupby("coin")["f1"].mean()
    D["ex1"]=-(D["f1"]-D["coin"].map(mu1))
    out={}
    act=D[(D.alloc<0)]
    out["active short bars"]=pd.Series({"n":len(act),"mean alloc":act.alloc.mean(),
        "mean pnl":act.pnl.mean(),"mean -f1":-act.f1.mean(),"share bars":len(act)/len(D)})
    # situation: r90<0, z>0
    S=D[(D.r90<0)&(D.z>0)].copy()
    S["zb"]=pd.cut(S.z,[0,0.5,1,1.5,2,3,20])
    g=S.groupby("zb",observed=True)
    out["by z bucket (r90<0, up day)"]=pd.DataFrame({"n":g.size(),"ex1":g.ex1.mean(),
        "t":g.ex1.apply(lambda x:x.mean()/x.std()*np.sqrt(len(x))),
        "-f3":g.f3.apply(lambda x:-x.mean()),"-f5":g.f5.apply(lambda x:-x.mean()),
        "mean alloc":g.alloc.mean(),"mean pnl":g.pnl.mean()})
    # rising markets comparison
    R=D[(D.r90>0)&(D.z>0)].copy(); R["zb"]=pd.cut(R.z,[0,0.5,1,1.5,2,3,20])
    g=R.groupby("zb",observed=True)
    out["by z bucket (r90>0, up day)"]=pd.DataFrame({"n":g.size(),"ex1":g.ex1.mean(),
        "-f3":g.f3.apply(lambda x:-x.mean())})
    # depth of fall
    S["db"]=pd.qcut(S.r90,4)
    S2=S[S.z>1]
    g=S2.groupby("db",observed=True)
    out["z>1 by r90 quartile"]=pd.DataFrame({"n":g.size(),"ex1":g.ex1.mean(),
        "t":g.ex1.apply(lambda x:x.mean()/x.std()*np.sqrt(len(x))),"-f3":g.f3.apply(lambda x:-x.mean())})
    S2=S2.copy(); S2["vb"]=pd.qcut(S2.vol,4)
    g=S2.groupby("vb",observed=True)
    out["z>1 by vol20 quartile"]=pd.DataFrame({"n":g.size(),"ex1":g.ex1.mean(),
        "t":g.ex1.apply(lambda x:x.mean()/x.std()*np.sqrt(len(x))),"-f1 raw":-g.f1.mean()})
    T=pd.concat(trades)
    out["trades"]=pd.DataFrame({"n":T.groupby("side").size(),"gross":T.groupby("side").profit_loss_percent.mean(),
        "net":T.groupby("side").net_profit_loss_percent.mean(),"dur_days":T.groupby("side").duration_minutes.mean()/1440})
    B=pd.concat(book)
    bd=B.groupby(["w","day"]).book_return.mean()
    out["book by window mean daily"]=B.groupby("w").book_return.mean()
    out["by coin: book mean, active pnl"]=pd.DataFrame({"book":B.groupby("coin").book_return.mean(),
        "pnl active":act.groupby("coin").pnl.mean(),"n active":act.groupby("coin").size()})
    return out
