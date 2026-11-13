import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").copy()
            c=b["close"].astype(float)
            fc=pd.to_numeric(b["forecast"],errors="coerce").fillna(0)
            raw=pd.to_numeric(b["debug_info.components.sma_cross_down.last_history_value"],errors="coerce")
            alloc=pd.to_numeric(b["postRebalance_current_allocation"],errors="coerce").fillna(0)
            short=(fc<0).astype(int)
            grp=(short!=short.shift()).cumsum()
            age=short.groupby(grp).cumcount()
            sma50=c.rolling(50,min_periods=30).mean()
            d=pd.DataFrame({"coin":coin,"w":w,"fc":fc.values,"raw":raw.values,
                "fwd10":(c.shift(-10)/c-1).values,"nxt":(c.shift(-1)/c-1).values,
                "alloc":alloc.values,"age":age.values,
                "r20":(c/c.shift(20)-1).values,"r5":(c/c.shift(5)-1).values,
                "dspread":(raw-raw.shift(10)).values,
                "px_vs_50":(c/sma50-1).values})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D=D.dropna(subset=["fwd10"])
    hold=D.groupby("coin").fwd10.mean()
    D["ex"]=D.fwd10-D.coin.map(hold)
    A=D[D.fc<0].copy(); P=D[D.fc==0].copy()
    def tab(df,col):
        g=df.groupby(col,observed=True).ex
        return pd.DataFrame({"n":g.size(),"mean_ex10":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))*np.sqrt(1/10),"up_share":df.groupby(col,observed=True).fwd10.apply(lambda x:(x>0).mean())})
    out={}
    A["ageq"]=pd.cut(A.age,[-1,10,30,60,120,1e4])
    out["short_by_age"]=tab(A,"ageq")
    A["r20q"]=pd.qcut(A.r20,5)
    out["short_by_r20"]=tab(A.dropna(subset=["r20"]),"r20q")
    A["dsp"]=np.where(A.dspread>0,"spread_narrowing","spread_widening")
    out["short_by_spread_dir"]=tab(A.dropna(subset=["dspread"]),"dsp")
    A["p50"]=np.where(A.px_vs_50>0,"px_above_sma50","px_below_sma50")
    out["short_by_px_vs_50"]=tab(A.dropna(subset=["px_vs_50"]),"p50")
    B=A.dropna(subset=["px_vs_50","dspread"])
    B["combo"]=B.p50+"|"+B.dsp
    out["short_combo"]=tab(B,"combo")
    D["r20q"]=pd.qcut(D.r20,5)
    out["all_by_r20"]=tab(D.dropna(subset=["r20"]),"r20q")
    P["rawq"]=pd.qcut(P.raw,3)
    out["flat_by_spread"]=tab(P.dropna(subset=["raw"]),"rawq")
    return out
