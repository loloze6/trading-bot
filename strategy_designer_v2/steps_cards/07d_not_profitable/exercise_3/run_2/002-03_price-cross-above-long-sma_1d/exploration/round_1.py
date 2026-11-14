import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    # book daily: mean across coins per day within window
    wins = sorted({w for c in data["days"] for w in data["days"][c]}, key=lambda s:int(s[1:]))
    chain = []
    for w in wins:
        frames = []
        for c in data["days"]:
            if w in data["days"][c]:
                d = data["days"][c][w][["day","book_return","coin_return"]].copy()
                d["coin"] = c
                frames.append(d)
        f = pd.concat(frames)
        g = f.groupby("day").agg(book=("book_return","mean"), hold=("coin_return","mean")).dropna()
        g["w"] = w
        chain.append(g)
    ch = pd.concat(chain).reset_index(drop=True)
    eq = (1+ch["book"]).cumprod(); dd = eq/eq.cummax()-1
    ch["dd"] = dd
    # per-window book stats
    pw = ch.groupby("w", sort=False).agg(book_sum=("book","sum"), hold_sum=("hold","sum"), min_dd=("dd","min"), n=("book","size"))
    out["per_window"] = pw.round(4)
    # deepest episodes: peaks to trough
    eps = []
    peak_i = 0
    i_trough = None
    vals = eq.values
    runmax = np.maximum.accumulate(vals)
    in_dd = dd.values < 0
    start = None
    for i in range(len(vals)):
        if in_dd[i] and start is None: start = i
        if (not in_dd[i] or i == len(vals)-1) and start is not None:
            seg = dd.values[start:i+1]
            t = start + int(np.argmin(seg))
            eps.append((start, t, i, seg.min(), ch["w"].iloc[start], ch["w"].iloc[t]))
            start = None
    E = pd.DataFrame(eps, columns=["s","t","e","depth","w_start","w_trough"]).sort_values("depth").head(6)
    E["len_to_trough"] = E["t"]-E["s"]
    E["hold_cum_during"] = [ (1+ch["hold"].iloc[a:b+1]).prod()-1 for a,b in zip(E.s,E.t)]
    out["deepest_dd"] = E[["depth","w_start","w_trough","len_to_trough","hold_cum_during"]].round(4)
    # bar-level per coin analysis
    rows = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.copy()
            r1 = b["close"].shift(-1)/b["close"]-1
            a = b["postRebalance_current_allocation"]
            dist = b.get("debug_info.components.above_ma.last_history_value")
            df = pd.DataFrame({"gain": a*r1, "alloc": a, "fc": b["forecast"], "r1": r1,
                               "dist": dist,
                               "mom20": b["close"]/b["close"].shift(20)-1,
                               "dd60": b["close"]/b["close"].rolling(60,min_periods=20).max()-1,
                               "vol20": np.log(b["close"]).diff().rolling(20).std(),
                               "coin": c, "w": w})
            # fees approx via book value change vs gain
            rows.append(df)
    B = pd.concat(rows).dropna(subset=["gain"])
    act = B[B.alloc > 0]
    out["active_share"] = float((B.alloc>0).mean())
    def grp(col, q=5):
        x = act.dropna(subset=[col]).copy()
        x["b"] = pd.qcut(x[col], q, labels=False, duplicates="drop")
        g = x.groupby("b").agg(lo=(col,"min"), hi=(col,"max"), n=("gain","size"), mean_gain=("gain","mean"),
                               sd=("gain","std"), mean_r1=("r1","mean"), worst5pct=("gain", lambda s: s.quantile(0.05)),
                               alloc=("alloc","mean"))
        g["t"] = g.mean_gain/(g.sd/np.sqrt(g.n))
        return g.round(5)
    out["by_forecast"] = grp("fc")
    out["by_dist"] = grp("dist")
    out["by_mom20"] = grp("mom20")
    out["by_dd60"] = grp("dd60")
    out["by_vol20"] = grp("vol20")
    out["coin_mean_r1_all"] = float(B.r1.mean())
    return out
