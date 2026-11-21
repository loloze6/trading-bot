import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    H = 5
    # coin mean daily return over all windows
    md = {}
    for coin, ws in data["bars"].items():
        r = np.concatenate([b["close"].pct_change().values[1:] for b in ws.values()])
        md[coin] = np.nanmean(r)
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; a = b["postRebalance_current_allocation"]
            nr = c.shift(-1)/c - 1
            r1 = c.pct_change()
            df = pd.DataFrame({"coin":coin,"w":w,"a":a,"nr":nr,"g":a*nr,"mkt":a*md[coin],
                               "timing":a*(nr-md[coin]),
                               "mom90":c/c.shift(90)-1,"mom28":c/c.shift(28)-1,
                               "vol30":r1.rolling(30).std(),
                               "year":pd.to_datetime(b["timestamp"]).dt.year,
                               "comb":b.get("debug_info.components.combined.last_history_value")})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True).dropna(subset=["nr"])
    out["market_vs_timing_per_bar"] = pd.Series({"gain":A.g.mean(),"market":A.mkt.mean(),"timing":A.timing.mean(),
        "mean_alloc":A.a.mean(),"mean_abs_alloc":A.a.abs().mean()})
    # by trend state: sign of 90d return
    A["trend90"] = np.sign(A["mom90"])
    A["side"] = np.sign(A["a"])
    t = A.dropna(subset=["mom90"]).groupby(["trend90","side"]).agg(n=("g","size"),gain=("g","mean"),
        nr=("nr","mean"),timing=("timing","mean"))
    out["by_trend90_side"] = t
    # graded: coin-relative quintile of 90d return, next 5-day unusual move non-overlapping
    rows2=[]
    for coin, ws in data["bars"].items():
        rr=np.concatenate([(b["close"].values[np.arange(0,len(b)-H,H)+H]/b["close"].values[np.arange(0,len(b)-H,H)]-1) for b in ws.values()])
        dr=rr.mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True); c=b["close"]
            f=(c.shift(-H)/c-1)-dr
            d=pd.DataFrame({"coin":coin,"un":f,"mom90":c/c.shift(90)-1,"mom28":c/c.shift(28)-1,
                            "pos":np.arange(len(b)),"comb":b.get("debug_info.components.combined.last_history_value"),
                            "year":pd.to_datetime(b["timestamp"]).dt.year})
            rows2.append(d[(d.pos%H==0)&d.un.notna()])
    G=pd.concat(rows2)
    for f in ["mom90","mom28"]:
        g=G.dropna(subset=[f]).copy()
        g["q"]=pd.cut(g.groupby("coin")[f].rank(pct=True),[0,.2,.4,.6,.8,1],labels=False)
        out[f"{f}_quintile_un"]=g.groupby("q").agg(n=("un","size"),un=("un","mean"),
            t=("un",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    # combined signed move by year, and share of short readings
    g=G.dropna(subset=["comb"]).copy(); g["s"]=np.sign(g.comb)*g.un
    out["comb_by_year"]=g.groupby("year").agg(n=("s","size"),signed=("s","mean"),
        t=("s",lambda x:x.mean()/x.std()*np.sqrt(len(x))),share_short=("comb",lambda x:(x<0).mean()))
    # combined in rising vs falling 90d trend
    g=g.dropna(subset=["mom90"]); g["tr"]=np.sign(g.mom90)
    out["comb_by_trend90"]=g.groupby(["tr",np.sign(g.comb)]).agg(n=("s","size"),signed=("s","mean"),
        t=("s",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    return out
