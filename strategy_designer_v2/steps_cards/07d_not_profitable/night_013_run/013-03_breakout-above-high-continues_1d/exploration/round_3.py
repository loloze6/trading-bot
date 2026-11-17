import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []; grid = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            raw = b["debug_info.components.break_dist.last_history_value"].values
            n = len(b)
            lvl = np.nan; lastbrk = -10**9
            dist = np.full(n, np.nan); age = np.full(n, np.nan)
            for i in range(n):
                if raw[i] > 0:
                    L = cl[i]/(1+raw[i]/100)
                    if i - lastbrk > 30 or np.isnan(lvl): lvl = L
                    else: lvl = max(lvl, L) if False else lvl
                    lastbrk = i
                if i - lastbrk <= 30 and not np.isnan(lvl):
                    dist[i] = cl[i]/lvl - 1; age[i] = i - lastbrk
                elif i - lastbrk > 30:
                    lvl = np.nan
            nxt = np.append(cl[1:]/cl[:-1]-1, np.nan)
            for i in range(n):
                rows.append(dict(coin=c, win=w, dist=dist[i], age=age[i], nxt=nxt[i]))
            for i in range(0, n-10, 10):
                grid.append(dict(coin=c, win=w, dist=dist[i], age=age[i], r10=cl[i+10]/cl[i]-1))
    R = pd.DataFrame(rows).dropna(subset=["nxt"])
    R["mu"] = R.groupby("coin")["nxt"].transform("mean")
    R["ex"] = R["nxt"] - R["mu"]
    S = R.dropna(subset=["dist"])
    S["state"] = np.where(S["dist"] > 0, "above_old_high", "back_below")
    out["post_break_daily_by_state"] = S.groupby("state")["ex"].agg(["size", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    a = S[S.dist > 0]
    s = stats.linregress(a["dist"], a["ex"]); out["daily_ex_on_dist_above"] = f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(a)}"
    S["ageb"] = pd.cut(S["age"], [-1, 0, 3, 10, 20, 30])
    out["daily_ex_above_by_age"] = S[S.dist > 0].groupby("ageb", observed=True)["ex"].agg(["size", "mean"])
    G = pd.DataFrame(grid)
    G["ex"] = G["r10"] - G.groupby("coin")["r10"].transform("mean")
    g = G.dropna(subset=["dist"]); g = g[g.dist > 0]
    s = stats.linregress(g["dist"], g["ex"]); out["grid10_ex_on_dist_above"] = f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(g)} mean_ex {g['ex'].mean():.4f}"
    # simple long-while-above daily return stats
    lw = R["nxt"].where(R["dist"] > 0, 0.0)
    out["long_while_above"] = f"share_in {(R['dist']>0).mean():.4f} mean {lw.mean():.6f} sharpe {lw.mean()/lw.std()*np.sqrt(365):.3f} hold_sharpe {R['nxt'].mean()/R['nxt'].std()*np.sqrt(365):.3f}"
    return out
