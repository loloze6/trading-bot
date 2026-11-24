import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; coins = list(bars.keys())
    cost = 0.0019/2
    rows = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values.astype(float)
            al = b["postRebalance_current_allocation"].fillna(0).values.astype(float)
            fc = b["forecast"].fillna(0).values.astype(float)
            ts = pd.to_datetime(b["timestamp"])
            nxt = np.r_[cl[1:]/cl[:-1]-1, np.nan]
            prev = np.r_[0, al[:-1]]
            r60 = pd.Series(cl).pct_change(60).values
            rows.append(pd.DataFrame({"coin":c,"wn":int(w[1:]),"t":np.arange(len(b)),"day":ts.dt.floor("D"),
                                      "wd":ts.dt.weekday,"al":al,"prev":prev,"fc":fc,"nxt":nxt,"r60":r60,"cl":cl}))
    X = pd.concat(rows, ignore_index=True)
    # sign of the active position: carry the sign of the last nonzero alloc
    X["sgn"] = np.sign(X["al"])
    def book(mask_keep):
        a = np.where(mask_keep, X["al"].values, 0.0)
        Y = X[["coin","wn","day","nxt"]].copy(); Y["a"]=a
        Y["pa"] = Y.groupby(["coin","wn"])["a"].shift(1).fillna(0)
        Y["g"] = Y["a"]*Y["nxt"].fillna(0) - (Y["a"]-Y["pa"]).abs()*cost
        d = Y.groupby(["wn","day","coin"])["g"].sum().groupby(["wn","day"]).mean().sort_index()
        val=(1+d).cumprod().values; dd=(val/np.maximum.accumulate(val)-1).min()
        yrs=len(d)/365; yr=val[-1]**(1/yrs)-1
        return pd.Series({"sharpe":d.mean()/d.std()*np.sqrt(365),"yearly":yr,"maxdd":dd,"calmar":yr/-dd,
                          "share_pos":(a!=0).mean()})
    allm = np.ones(len(X),bool)
    longm = X["al"].values>0
    shortm = X["al"].values<0
    up60 = (X["r60"].values>0)
    out["books"] = pd.DataFrame({"all":book(allm),"long_only":book(longm),"short_only":book(shortm),
                                 "short_only_up60_long_all":book(longm | (shortm & up60))}).T
    # weekday drift: 2-bar returns from each weekday close, non-overlapping by week (one per weekday per week)
    X["f2"] = X.groupby(["coin","wn"])["cl"].shift(-2)/X["cl"]-1
    wdtab = X.dropna(subset=["f2"]).groupby("wd")["f2"].agg(["mean","count",lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    wdtab.columns=["mean2","n","t"]
    out["weekday_2bar_drift(wd of bar start; Thu=3)"]=wdtab
    # Thursday bars: condition alone vs with signal
    T = X[(X["wd"]==3)].dropna(subset=["f2"]).copy()
    T["r14"] = np.nan
    T["fcq"] = pd.qcut(T["fc"],5,labels=False,duplicates="drop")
    out["thu_by_fcq_up60"] = T.groupby([T["r60"]>0,"fcq"]).agg(n=("f2","size"),f2=("f2","mean"),fc=("fc","mean"))
    # other weekdays: does a 14-day rise (sign of 14-day return) grade 2-bar moves anyway?
    X["r14"]=X.groupby(["coin","wn"])["cl"].pct_change(14)
    O = X[(X["wd"]!=3)].dropna(subset=["f2","r14"])
    O["q"]=O.groupby("coin")["r14"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["other_days_by_r14_q"]=O.groupby("q")["f2"].agg(["mean","count"])
    T2 = X[(X["wd"]==3)].dropna(subset=["f2","r14"]).copy()
    T2["q"]=T2.groupby("coin")["r14"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["thu_by_r14_q"]=T2.groupby("q")["f2"].agg(["mean","count"])
    # long-only falls by year
    a = np.where(longm, X["al"].values, 0.0)
    X["gl"]=a*X["nxt"].fillna(0)
    X["year"]=X["day"].dt.year
    out["long_pnl_by_year"]=X.groupby("year")["gl"].sum()/len(coins)
    X["gs"]=np.where(shortm,X["al"].values,0)*X["nxt"].fillna(0)
    out["short_pnl_by_year"]=X.groupby("year")["gs"].sum()/len(coins)
    return out
