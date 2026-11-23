import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    COST = 0.0011  # one side, of value traded
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            r1 = b.close.shift(-1)/b.close-1
            a = b.postRebalance_current_allocation.fillna(0)
            ret30 = b.close/b.close.shift(30)-1
            hi90 = b.close.rolling(90, min_periods=30).max()
            near = b.close/hi90-1
            fwd5 = b.close.shift(-5)/b.close-1
            df = pd.DataFrame({"r1":r1,"a":a,"fc":b.forecast,"ret30":ret30,"near":near,"fwd5":fwd5,
                               "day":pd.to_datetime(b.timestamp).dt.floor("D")})
            df["coin"]=c; df["win"]=w; df["pos"]=np.arange(len(b))
            recs.append(df)
    D = pd.concat(recs, ignore_index=True)
    D["wn"] = D.win.str[1:].astype(int)
    D["up30"] = D.ret30 > 0
    # coin mean 5-bar return on grid
    G = D[D.pos % 5 == 0].dropna(subset=["fwd5"]).copy()
    G["cm"] = G.groupby("coin").fwd5.transform("mean")
    G["ex"] = G.fwd5 - G.cm
    # condition alone: up30 without short signal vs with short signal
    def tt(x):
        return pd.Series({"mean":x.mean(),"n":len(x),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    G["grp"] = np.select([G.up30 & (G.fc<0), G.up30 & (G.fc>0), ~G.up30 & (G.fc<0), ~G.up30 & (G.fc>0)],
                         ["up30_short","up30_long","down30_short","down30_long"], "other")
    out["excess5_by_group"] = G.groupby("grp").ex.apply(tt).unstack()
    out["excess5_up30_all"] = tt(G.loc[G.up30,"ex"])
    out["excess5_down30_all"] = tt(G.loc[~G.up30 & G.ret30.notna(),"ex"])
    # graded: in up30, signal strength quartile vs signed excess
    U = G[G.up30 & (G.fc!=0)].copy()
    U["q"] = pd.qcut(U.fc.abs(),4,labels=False,duplicates="drop")
    U["sg"] = np.sign(U.fc)*U.ex
    out["up30_signed_by_absfc_q"] = U.groupby(["q", np.sign(U.fc)]).sg.apply(tt).unstack()

    def book(alloc):
        d = D.copy(); d["al"] = alloc
        d["prev"] = d.groupby(["coin","win"]).al.shift(1).fillna(0)
        d["g"] = d.al*d.r1.fillna(0) - COST*(d.al-d.prev).abs()
        cd = d.groupby(["coin","win","day"]).g.sum().reset_index()
        bk = cd.groupby(["wn","day"]).g.mean().reset_index().sort_values(["wn","day"])
        r = bk.g
        eq = (1+r).cumprod(); dd = (eq/eq.cummax()-1).min()
        yr = eq.iloc[-1]**(365/len(r))-1
        # worst window-left-out sharpe
        sh = r.mean()/r.std()*np.sqrt(365)
        lo = min(bk[bk.wn!=w].g.mean()/bk[bk.wn!=w].g.std()*np.sqrt(365) for w in bk.wn.unique())
        dd1417 = None
        s = bk[(bk.wn>=14)&(bk.wn<=17)].g
        return pd.Series({"sharpe":sh,"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),"min_loo_sharpe":lo,
                          "ret_w14_17":(1+s).prod()-1,"mean":r.mean()})
    base = D.a
    v = {}
    v["base"] = book(base)
    v["no_short_up30"] = book(np.where((base<0)&D.up30, 0, base))
    v["long_only"] = book(base.clip(lower=0))
    v["no_short_near_top"] = book(np.where((base<0)&(D.near>-0.1), 0, base))
    v["no_short_up30_or_neartop"] = book(np.where((base<0)&(D.up30|(D.near>-0.1)), 0, base))
    out["variants"] = pd.DataFrame(v).T
    # deepest fall composition w14-w17
    F = D[(D.wn>=14)&(D.wn<=17)].dropna(subset=["r1"])
    F["g"] = F.a*F.r1; F["side"]=np.sign(F.a)
    out["w14_17_by_side_trend"] = F.groupby(["side","up30"]).g.agg(["sum","mean","count"])
    out["w14_17_by_coin"] = F.groupby("coin").g.sum()
    return out
