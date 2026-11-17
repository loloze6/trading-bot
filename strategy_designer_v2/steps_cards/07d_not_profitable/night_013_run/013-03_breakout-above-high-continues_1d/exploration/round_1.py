import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []; trows = []; grid = []; drows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            al = b["postRebalance_current_allocation"].fillna(0)
            raw = b.get("debug_info.components.break_dist.last_history_value")
            cl = b["close"].values
            rows.append(dict(coin=c, win=w, n=len(b), in_share=(al > 0.01).mean(),
                             fc_pos=(b["forecast"] > 0).mean(),
                             coin_ret=cl[-1]/cl[0]-1))
            # grid returns 30 and 10 bars with raw distance
            for h in (10, 30):
                for i in range(0, len(b)-h, h):
                    r = cl[i+h]/cl[i]-1
                    d = raw.iloc[i] if raw is not None else np.nan
                    # 30-bar past return
                    p = cl[i]/cl[i-30]-1 if i >= 30 else np.nan
                    grid.append(dict(coin=c, win=w, h=h, ret=r, dist=d, past30=p))
            t = data["trades"][c][w]
            if len(t):
                t = t.copy(); t["coin"] = c; t["win"] = w; trows.append(t)
            d = data["days"][c][w].copy(); d["coin"] = c; d["win"] = w
            al_day = b.assign(day=pd.to_datetime(b["timestamp"]).dt.floor("D")).groupby("day")["postRebalance_current_allocation"].last()
            d["alloc"] = d["day"].map(al_day) if "day" in d else np.nan
            drows.append(d)
    R = pd.DataFrame(rows)
    out["per_coin"] = R.groupby("coin")[["n", "in_share", "fc_pos", "coin_ret"]].mean()
    out["in_share_by_window"] = R.groupby("win")[["in_share", "coin_ret"]].mean()
    T = pd.concat(trows)
    T["days"] = T["duration_minutes"]/1440
    out["trades_by_coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"),
        mean_net=("net_profit_loss_percent", "mean"), med_days=("days", "median"),
        win_rate=("net_profit_loss_percent", lambda x: (x > 0).mean()))
    out["trades_by_window"] = T.groupby("win").agg(n=("net_profit_loss_percent", "size"),
        sum_net=("net_profit_loss_percent", "sum"))
    out["trade_days_buckets"] = T.groupby(pd.cut(T["days"], [0, 2, 5, 10, 20, 60, 400]))["net_profit_loss_percent"].agg(["size", "mean"])
    G = pd.DataFrame(grid)
    res = {}
    for h in (10, 30):
        g = G[(G.h == h)].dropna(subset=["dist"]).copy()
        mu = g.groupby("coin")["ret"].transform("mean")
        g["ex"] = g["ret"] - mu
        g["q"] = pd.cut(g["dist"], [-1e9, -60, -40, -25, -15, -8, -3, 0, 1e9])
        res[h] = g.groupby("q").agg(n=("ex", "size"), mean_ex=("ex", "mean"),
                                   t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan))
        below = g[g.dist <= 0]
        sl = stats.linregress(below["dist"], below["ex"])
        out[f"slope_below_high_h{h}"] = f"slope {sl.slope:.5f} t {sl.slope/sl.stderr:.2f} n {len(below)}"
    out["dist_bucket_h30"] = res[30]
    out["dist_bucket_h10"] = res[10]
    out["dist_describe"] = G[G.h == 30]["dist"].describe()
    D = pd.concat(drows)
    D["in"] = D["alloc"].fillna(0) > 0.01
    out["days_in_vs_out"] = D.groupby("in").agg(n=("book_return", "size"), book=("book_return", "mean"),
                                                 coin=("coin_return", "mean"))
    return out
