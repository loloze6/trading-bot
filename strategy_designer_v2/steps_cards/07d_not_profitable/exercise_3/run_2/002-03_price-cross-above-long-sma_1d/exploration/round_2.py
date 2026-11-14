import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.copy()
            r1 = b["close"].shift(-1)/b["close"]-1
            a = b["postRebalance_current_allocation"]
            dist = b.get("debug_info.components.above_ma.last_history_value")
            df = pd.DataFrame({"gain": a*r1, "alloc": a, "fc": b["forecast"], "r1": r1, "dist": dist,
                               "mom20": b["close"]/b["close"].shift(20)-1,
                               "mom60": b["close"]/b["close"].shift(60)-1,
                               "dd60": b["close"]/b["close"].rolling(60,min_periods=20).max()-1,
                               "coin": c, "w": w})
            # forward 20 bar return on grid for non-overlap
            df["pos"] = np.arange(len(df))
            df["f20"] = b["close"].shift(-20)/b["close"]-1
            df["g20"] = a*df["f20"]
            rows.append(df)
    B = pd.concat(rows).dropna(subset=["gain"])
    act = B[B.alloc > 0].copy()
    # share of total loss days among active bars by state
    act["mom20_neg"] = act.mom20 < 0
    act["dd_deep"] = act.dd60 < -0.15
    tab = act.groupby(["mom20_neg","dd_deep"]).agg(n=("gain","size"), mean_gain=("gain","mean"),
            sd=("gain","std"), sum_gain=("gain","sum"), sum_neg=("gain", lambda s: s[s<0].sum()),
            alloc=("alloc","mean"))
    tab["t"] = tab.mean_gain/(tab.sd/np.sqrt(tab.n))
    out["state_mom_dd"] = tab.round(5)
    # mom20 graded within forecast>10 (high allocation)
    hi = act[act.fc > 10].dropna(subset=["mom20"]).copy()
    hi["b"] = pd.qcut(hi.mom20, 5, labels=False)
    g = hi.groupby("b").agg(lo=("mom20","min"), hi=("mom20","max"), n=("gain","size"), mean_gain=("gain","mean"),
            sd=("gain","std"), sum_neg=("gain", lambda s: s[s<0].sum()), alloc=("alloc","mean"))
    g["t"] = g.mean_gain/(g.sd/np.sqrt(g.n))
    out["hi_fc_by_mom20"] = g.round(5)
    # non-overlapping 20-bar, active grid
    grid = B[(B.pos % 20 == 0) & (B.alloc > 0)].dropna(subset=["f20","mom20"]).copy()
    grid["b"] = pd.qcut(grid.mom20, 4, labels=False)
    g2 = grid.groupby("b").agg(lo=("mom20","min"), hi=("mom20","max"), n=("f20","size"), mean_f20=("f20","mean"),
            sd=("f20","std"), mean_g20=("g20","mean"), q10=("f20", lambda s: s.quantile(0.1)))
    g2["t"] = g2.mean_f20/(g2.sd/np.sqrt(g2.n))
    out["grid_f20_by_mom20"] = g2.round(4)
    # mom60 graded on active
    m = act.dropna(subset=["mom60"]).copy()
    m["b"] = pd.qcut(m.mom60, 5, labels=False)
    g3 = m.groupby("b").agg(lo=("mom60","min"), hi=("mom60","max"), n=("gain","size"), mean_gain=("gain","mean"),
            sd=("gain","std"), sum_neg=("gain", lambda s: s[s<0].sum()), alloc=("alloc","mean"))
    g3["t"] = g3.mean_gain/(g3.sd/np.sqrt(g3.n))
    out["act_by_mom60"] = g3.round(5)
    # book daily drawdown episodes: state of held coins during deepest falls
    wins = sorted({w for c in data["days"] for w in data["days"][c]}, key=lambda s:int(s[1:]))
    in_falls = act[act.w.isin(["w15","w16","w17","w18","w19","w12","w13","w21","w22"])]
    out["fall_windows_state"] = pd.DataFrame({
        "share_mom20_neg": [ (in_falls.mom20<0).mean(), (act.mom20<0).mean()],
        "sum_gain": [in_falls.gain.sum(), act.gain.sum()],
        "sum_gain_mom20_neg": [in_falls.gain[in_falls.mom20<0].sum(), act.gain[act.mom20<0].sum()],
        "mean_alloc": [in_falls.alloc.mean(), act.alloc.mean()]}, index=["fall_windows","all"]).round(4)
    # by year of bars
    return out
