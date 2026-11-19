import numpy as np, pandas as pd
from scipy import stats

def ols(x, y):
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if len(x) < 30: return (np.nan, np.nan, len(x))
    r = stats.linregress(x, y)
    return (r.slope, r.slope / r.stderr, len(x))

def explore(data):
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    rows = []
    hr = []
    g24 = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"].values.astype(float); vol = b["volume"].values.astype(float)
            n = len(cl)
            lr = np.diff(np.log(cl), prepend=np.nan)
            for t in range(0, n, 72):
                if t < 72 or t + 72 >= n: continue
                h = lr[t-71:t+1]; v = vol[t-71:t+1]
                r72 = cl[t]/cl[t-72]-1
                net = np.log(cl[t]/cl[t-72])
                eff = abs(net)/np.nansum(np.abs(h)) if np.nansum(np.abs(h))>0 else np.nan
                srt = np.sort(h)
                top3loss = -srt[:3].clip(max=0).sum(); top3gain = srt[-3:].clip(min=0).sum()
                share = (top3loss/abs(net)) if net < 0 else (top3gain/abs(net))
                vs = np.sort(v)[-3:].sum()/v.sum() if v.sum()>0 else np.nan
                r24 = cl[t]/cl[t-24]-1
                rows.append(dict(coin=c, w=w, r72=r72, r24=r24, eff=eff, share=share, vconc=vs,
                                 vol=np.nanstd(h), fwd=cl[t+72]/cl[t]-1, hour=pd.Timestamp(b["timestamp"].iloc[t]).hour))
            ts = pd.to_datetime(b["timestamp"])
            nxt = np.append(lr[1:], np.nan)
            hr.append(pd.DataFrame({"coin": c, "hour": ts.dt.hour.values, "wd": ts.dt.weekday.values, "nxt": nxt}))
            for t in range(0, n, 24):
                if t < 24 or t + 24 >= n: continue
                h = lr[t-23:t+1]
                s = np.nanstd(lr[max(1,t-167):t+1])
                g24.append(dict(coin=c, last1=lr[t]/s if s>0 else np.nan, r24z=np.log(cl[t]/cl[t-24])/(s*np.sqrt(24)) if s>0 else np.nan,
                                vol=s, fwd24=cl[t+24]/cl[t]-1))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    out = {}
    res = {}
    res["ex~r72 all"] = ols(d.r72.values, d.ex.values)
    dn = d[d.r72 < 0]; up = d[d.r72 > 0]
    res["ex~r72 down"] = ols(dn.r72.values, dn.ex.values)
    res["ex~r72 up"] = ols(up.r72.values, up.ex.values)
    res["ex~eff down"] = ols(dn.eff.values, dn.ex.values)
    res["ex~eff up"] = ols(up.eff.values, up.ex.values)
    res["ex~share down"] = ols(dn.share.values, dn.ex.values)
    res["ex~share up"] = ols(up.share.values, up.ex.values)
    res["ex~vconc down"] = ols(dn.vconc.values, dn.ex.values)
    res["ex~vconc up"] = ols(up.vconc.values, up.ex.values)
    res["ex~vol all"] = ols(d.vol.values, d.ex.values)
    res["ex~r24 all"] = ols(d.r24.values, d.ex.values)
    out["regs"] = pd.DataFrame(res, index=["slope", "t", "n"]).T
    d["r72q"] = d.groupby("coin")["r72"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["by r72 quintile"] = d.groupby("r72q")["ex"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    d["volq"] = d.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["by vol quintile"] = d.groupby("volq")["ex"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    dn = d[d.r72 < 0].copy()
    dn["effq"] = pd.qcut(dn.eff, 3, labels=False)
    dn["r72t"] = pd.qcut(dn.r72, 3, labels=False)
    out["down: r72 tercile x eff tercile mean ex"] = dn.pivot_table(index="r72t", columns="effq", values="ex", aggfunc="mean")
    up = d[d.r72 > 0].copy()
    up["effq"] = pd.qcut(up.eff, 3, labels=False); up["r72t"] = pd.qcut(up.r72, 3, labels=False)
    out["up: r72 tercile x eff tercile mean ex"] = up.pivot_table(index="r72t", columns="effq", values="ex", aggfunc="mean")
    out["per coin ex~r72"] = pd.DataFrame({c: ols(g.r72.values, g.ex.values) for c, g in d.groupby("coin")}, index=["slope","t","n"]).T
    H = pd.concat(hr)
    hh = H.groupby("hour")["nxt"].agg(["mean", "count", "std"]); hh["t"] = hh["mean"]/(hh["std"]/np.sqrt(hh["count"]))
    out["next-1h by hour"] = hh[["mean", "t"]]
    ww = H.groupby("wd")["nxt"].agg(["mean", "count", "std"]); ww["t"] = ww["mean"]/(ww["std"]/np.sqrt(ww["count"]))
    out["next-1h by weekday"] = ww[["mean", "t"]]
    G = pd.DataFrame(g24)
    G["ex"] = G.fwd24 - G.groupby("coin")["fwd24"].transform("mean")
    out["24h regs"] = pd.DataFrame({"ex24~last1h z": ols(G.last1.values, G.ex.values),
                                    "ex24~r24 z": ols(G.r24z.values, G.ex.values),
                                    "ex24~vol": ols(G.vol.values, G.ex.values)}, index=["slope","t","n"]).T
    # book
    br = []
    for c in days:
        for w, dd in days[c].items():
            b = bars[c][w]
            pos = b.groupby(pd.to_datetime(b["timestamp"]).dt.floor("D"))["postRebalance_current_allocation"].mean().values
            x = dd[["book_return", "coin_return"]].copy()
            x["pos"] = pos[:len(x)] if len(pos) >= len(x) else np.nan
            x["coin"] = c; x["w"] = w
            br.append(x)
    B = pd.concat(br)
    out["book"] = pd.Series({"mean book": B.book_return.mean(), "mean coin": B.coin_return.mean(),
                             "mean pos": B.pos.mean(), "share days pos>0": (B.pos > 0.01).mean()})
    T = pd.concat([t.assign(coin=c) for c in trades for w, t in trades[c].items()])
    out["trades"] = pd.Series({"n": len(T), "mean gross %": T.profit_loss_percent.mean(), "mean net %": T.net_profit_loss_percent.mean(),
                               "median dur h": T.duration_minutes.median()/60})
    return out
