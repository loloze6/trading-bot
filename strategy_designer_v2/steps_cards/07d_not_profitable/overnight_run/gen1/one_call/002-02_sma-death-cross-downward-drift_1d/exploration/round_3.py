import pandas as pd, numpy as np

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").copy()
            c=b["close"].astype(float)
            fc=pd.to_numeric(b["forecast"],errors="coerce").fillna(0)
            raw=pd.to_numeric(b["debug_info.components.sma_cross_down.last_history_value"],errors="coerce")
            sma50=c.rolling(50,min_periods=30).mean()
            short=(fc<0).astype(int)
            age=short.groupby((short!=short.shift()).cumsum()).cumcount()
            vol=c.pct_change().rolling(20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"year":pd.to_datetime(b["timestamp"]).dt.year.values,
                "fc":fc.values,"fwd10":(c.shift(-10)/c-1).values,"age":age.values,"vol":vol.values,
                "dspread":(raw-raw.shift(10)).values,"px_vs_50":(c/sma50-1).values,"pos":np.arange(len(b))})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True).dropna(subset=["fwd10"])
    hold=D.groupby("coin").fwd10.mean()
    D["short_gain"]=-(D.fwd10-D.coin.map(hold))
    A=D[(D.fc<0)].dropna(subset=["dspread","px_vs_50","vol"]).copy()
    A["combo"]=np.where(A.px_vs_50<0,"below50","above50")+"|"+np.where(A.dspread>0,"narrowing","widening")
    N=A[A.pos%10==0].copy()
    def tab(df,cols):
        g=df.groupby(cols,observed=True).short_gain
        return pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    out={}
    out["nonoverlap_combo"]=tab(N,"combo")
    tgt=A[A.combo=="below50|narrowing"]
    out["below50_narrowing_by_coin"]=tab(tgt,"coin")
    out["below50_narrowing_by_year"]=tab(tgt,"year")
    A["volq"]=pd.qcut(A.vol,3,labels=["calm","mid","volatile"])
    out["combo_by_vol"]=tab(A,["combo","volq"])
    A["old"]=np.where(A.age>60,"old>60","young<=60")
    out["nonoverlap_age"]=tab(A[A.pos%10==0],"old")
    return out
