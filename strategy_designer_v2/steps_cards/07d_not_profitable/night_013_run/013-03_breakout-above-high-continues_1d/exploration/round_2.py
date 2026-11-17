import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    ev = []; grid = []; tr = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; hi = b["high"].values
            raw = b["debug_info.components.break_dist.last_history_value"].values
            brk = raw > 0
            last = -10**9; since = np.full(len(b), np.nan)
            for i in range(len(b)):
                if brk[i]: last = i
                if last > -10**9: since[i] = i - last
            # break events: first break after >=10 bars without
            prev = -10**9
            for i in range(len(b)):
                if brk[i]:
                    if i - prev > 10:
                        r = {}
                        for h in (1, 5, 10, 30):
                            r[h] = cl[i+h]/cl[i]-1 if i+h < len(b) else np.nan
                        # does close fall back below the old high within 5 bars
                        oldhigh = cl[i]/(1+raw[i]/100)
                        fb = np.nan
                        if i+5 < len(b): fb = float((cl[i+1:i+6] < oldhigh).any())
                        ev.append(dict(coin=c, win=w, dist=raw[i], r1=r[1], r5=r[5], r10=r[10], r30=r[30], fellback=fb,
                                       vol_ratio=b["volume"].iloc[i]/b["volume"].iloc[max(0,i-30):i].mean() if i>0 else np.nan))
                    prev = i
            for i in range(0, len(b)-30, 30):
                g = dict(coin=c, win=w, ret=cl[i+30]/cl[i]-1, since=since[i], dist=raw[i])
                if i >= 60:
                    g["d60"] = cl[i]/hi[i-60:i].max()-1
                grid.append(g)
            # in-position days vs after exit within 30 bars
            al = b["postRebalance_current_allocation"].fillna(0).values
            pos = b["close"].pct_change().shift(-1).values
            for i in range(len(b)-1):
                tr.append(dict(coin=c, in_=al[i] > 0.01, since=since[i], nxt=pos[i]))
    E = pd.DataFrame(ev)
    G = pd.DataFrame(grid)
    G["ex"] = G["ret"] - G.groupby("coin")["ret"].transform("mean")
    out["break_events"] = f"n {len(E)}"
    out["event_means"] = E[["r1", "r5", "r10", "r30", "fellback"]].agg(["mean", "count"])
    for k in ("r10", "r30"):
        e = E.dropna(subset=[k])
        if len(e) > 3:
            s = stats.linregress(e["dist"], e[k]); out[f"event_{k}_on_dist"] = f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(e)}"
    e = E.dropna(subset=["r30", "fellback"])
    out["r30_by_fellback"] = e.groupby("fellback")["r30"].agg(["size", "mean"])
    e = E.dropna(subset=["r30", "vol_ratio"])
    out["r30_by_volratio"] = e.groupby(e["vol_ratio"] > e["vol_ratio"].median())["r30"].agg(["size", "mean"])
    G["sb"] = pd.cut(G["since"], [-1, 0, 10, 30, 60, 120, 1000])
    out["grid30_by_days_since_break"] = G.groupby("sb", observed=True)["ex"].agg(["size", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    out["grid30_never_broke_in_window"] = G[G.since.isna()]["ex"].agg(["size", "mean"])
    g = G.dropna(subset=["d60"])
    s = stats.linregress(g["d60"], g["ex"]); out["grid30_on_60bar_high_dist"] = f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(g)}"
    g["q"] = pd.qcut(g["d60"], 4)
    out["grid30_by_60bar_dist_q"] = g.groupby("q", observed=True)["ex"].agg(["size", "mean"])
    T = pd.DataFrame(tr).dropna(subset=["nxt"])
    T["sb"] = pd.cut(T["since"], [-1, 0, 5, 10, 30, 1000])
    out["next_bar_ret_by_since_and_in"] = T.groupby(["sb", "in_"], observed=True)["nxt"].agg(["size", "mean"])
    return out
