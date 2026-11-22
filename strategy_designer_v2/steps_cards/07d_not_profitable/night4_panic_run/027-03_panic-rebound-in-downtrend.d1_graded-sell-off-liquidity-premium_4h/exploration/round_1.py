import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    # portfolio daily returns
    rows = []
    for c, ws in days.items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    P = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().reset_index().sort_values(["wn","day"])
    P = P.dropna()
    eq = (1+P["book_return"]).cumprod(); peak = eq.cummax(); dd_ = eq/peak-1
    P["dd"] = dd_.values
    out["deepest_fall_total"] = float(dd_.min())
    yrs = len(P)/365; out["yearly_return"] = float(eq.iloc[-1]**(1/yrs)-1)
    # per window
    pw = P.groupby("wn").agg(book_mean=("book_return","mean"), coin_mean=("coin_return","mean"),
                              book_sum=("book_return","sum"), coin_sum=("coin_return","sum"), min_dd=("dd","min"))
    out["per_window"] = pw.round(4)
    # exposure & conditions per bar
    trs = []
    barrows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            ret180 = cl/cl.shift(180)-1
            ret42 = cl/cl.shift(42)-1
            fwd84 = cl.shift(-84)/cl-1
            fwd1 = cl.shift(-1)/cl-1
            al = b["postRebalance_current_allocation"]
            barrows.append(pd.DataFrame({"al":al,"fwd1":fwd1,"pos_gain":al*fwd1,"ret180":ret180,"ret42":ret42}))
            t = data["trades"][c][w]
            if len(t)==0: continue
            ts = pd.to_datetime(b["timestamp"])
            idx = pd.Series(range(len(b)), index=ts)
            for _, r in t.iterrows():
                et = pd.to_datetime(r["entry_time"])
                i = idx.index.searchsorted(et)
                if i>=len(b): continue
                trs.append({"coin":c,"wn":int(w[1:]),"net":r["net_profit_loss_percent"],"gross":r["profit_loss_percent"],
                            "dur_d":r["duration_minutes"]/1440,"ef":r["entry_forecast"],
                            "r180":ret180.iloc[i],"r42":ret42.iloc[i],"f84":fwd84.iloc[i]})
    T = pd.DataFrame(trs)
    out["trades_summary"] = T[["net","gross","dur_d","ef"]].describe().round(3)
    for col in ["r180","r42","ef"]:
        q = pd.qcut(T[col], 5, duplicates="drop")
        out[f"trades_by_{col}"] = T.groupby(q, observed=True).agg(n=("net","size"), net_mean=("net","mean"),
                    net_med=("net","median"), loss_share=("net", lambda x:(x<0).mean()), f84=("f84","mean")).round(3)
    B = pd.concat(barrows).dropna()
    B["inpos"] = B["al"].abs()>1e-6
    q = pd.qcut(B["ret180"],5)
    out["bars_by_prior30d"] = B.groupby(q, observed=True).agg(share_in=("inpos","mean"), mean_al=("al","mean"),
              pos_gain=("pos_gain","mean"), coin_fwd1=("fwd1","mean")).round(5)
    out["worst_trades_r180"] = T.nsmallest(40,"net")[["r180"]].describe().round(3)
    out["all_trades_r180"] = T[["r180"]].describe().round(3)
    out["by_coin"] = T.groupby("coin").agg(n=("net","size"), net=("net","mean")).round(3)
    return out
