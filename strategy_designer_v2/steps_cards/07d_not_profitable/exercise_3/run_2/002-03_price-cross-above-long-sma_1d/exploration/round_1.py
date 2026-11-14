import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    H = 20
    # pooled mean daily return per coin
    pm = {}
    for c, ws in data["bars"].items():
        rs = []
        for w, b in ws.items():
            rs.append(b["close"].pct_change().dropna())
        pm[c] = pd.concat(rs).mean()
    # non-overlapping 20-bar samples with forecast, raw distance
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            f = b["forecast"].values
            raw = b.get("debug_info.components.above_ma.last_history_value")
            raw = raw.values if raw is not None else np.full(len(b), np.nan)
            # past 20-bar return and days since forecast turned positive
            pos = (f > 0).astype(int)
            run = np.zeros(len(b))
            for i in range(len(b)):
                run[i] = run[i-1]+1 if (pos[i] and i>0) else (1 if pos[i] else 0)
            for i in range(0, len(b)-H, H):
                fr = cl[i+H]/cl[i]-1
                past = cl[i]/cl[i-H]-1 if i>=H else np.nan
                rows.append(dict(coin=c, win=w, f=f[i], raw=raw[i], fr=fr,
                                 ex=fr-H*pm[c], past=past, run=run[i]))
    d = pd.DataFrame(rows)
    d["fbin"] = pd.cut(d["f"], [-0.01, 0, 5, 10, 15, 20.01])
    g = d.groupby("fbin", observed=True)["ex"]
    out["fwd20 excess by forecast bin"] = pd.DataFrame({"n": g.size(), "mean": g.mean(),
        "t": g.apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan),
        "share_pos": g.apply(lambda s: (s>0).mean())})
    a = d[d.f > 0].copy()
    a["rawq"] = pd.qcut(a["raw"], 5, duplicates="drop")
    g = a.groupby("rawq", observed=True)["ex"]
    out["active: excess by raw distance quintile"] = pd.DataFrame({"n": g.size(), "mean": g.mean(),
        "t": g.apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))))})
    a["runb"] = pd.cut(a["run"], [0, 20, 60, 150, 10000])
    g = a.groupby("runb", observed=True)["ex"]
    out["active: excess by days since turned on"] = pd.DataFrame({"n": g.size(), "mean": g.mean(),
        "t": g.apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))))})
    a["pastq"] = pd.qcut(a["past"], 5, duplicates="drop")
    g = a.groupby("pastq", observed=True)["ex"]
    out["active: excess by past20 return quintile"] = pd.DataFrame({"n": g.size(), "mean": g.mean(),
        "t": g.apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))))})
    # book per coin
    rr = []
    for c, ws in data["days"].items():
        allb = []; allc = []
        for w, dd in ws.items():
            allb.append(dd["book_return"].dropna()); allc.append(dd["coin_return"].dropna())
        bb = pd.concat(allb); cc = pd.concat(allc)
        eq = (1+bb).cumprod(); dd_ = (eq/eq.cummax()-1).min()
        eqc = (1+cc).cumprod(); ddc = (eqc/eqc.cummax()-1).min()
        rr.append(dict(coin=c, sh=bb.mean()/bb.std()*np.sqrt(365), sh_hold=cc.mean()/cc.std()*np.sqrt(365),
                       maxdd=dd_, maxdd_hold=ddc, mean=bb.mean()))
    out["book per coin"] = pd.DataFrame(rr)
    # book returns by window (average of coins)
    wr = []
    for c, ws in data["days"].items():
        for w, dd in ws.items():
            wr.append(dict(win=w, br=(1+dd["book_return"].dropna()).prod()-1,
                           cr=(1+dd["coin_return"].dropna()).prod()-1))
    wr = pd.DataFrame(wr).groupby("win")[["br","cr"]].mean()
    wr = wr.loc[sorted(wr.index, key=lambda x: int(x[1:]))]
    out["window book vs coin return (mean of coins)"] = wr
    # daily: book return on held days by forecast bin and recent drawdown from 20-day high
    dl = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            al = b["postRebalance_current_allocation"].values
            r1 = b["close"].shift(-1)/b["close"]-1
            ddh = b["close"]/b["close"].rolling(20, min_periods=1).max()-1
            vol = b["close"].pct_change().rolling(20).std()
            dl.append(pd.DataFrame(dict(al=al, g=al*r1, f=b["forecast"], ddh=ddh, vol=vol, r1=r1)))
    dl = pd.concat(dl).dropna()
    h = dl[dl.al > 0].copy()
    h["ddb"] = pd.cut(h["ddh"], [-1, -0.2, -0.1, -0.05, -0.0001, 0.01])
    g = h.groupby("ddb", observed=True)
    out["held days: gain by fall from 20d high"] = pd.DataFrame({"n": g.size(), "mean_gain": g["g"].mean(),
        "mean_r1": g["r1"].mean(), "mean_alloc": g["al"].mean()})
    h["volq"] = pd.qcut(h["vol"], 5)
    g = h.groupby("volq", observed=True)
    out["held days: by vol quintile"] = pd.DataFrame({"n": g.size(), "mean_gain": g["g"].mean(),
        "mean_r1": g["r1"].mean(), "sum_gain": g["g"].sum(), "mean_alloc": g["al"].mean()})
    out["mean alloc when held"] = float(h["al"].mean())
    t = pd.concat([t for ws in data["trades"].values() for t in ws.values()])
    out["trades"] = pd.DataFrame({"n":[len(t)], "mean_gross":[t["profit_loss_percent"].mean()],
        "mean_net":[t["net_profit_loss_percent"].mean()], "mean_dur_days":[t["duration_minutes"].mean()/1440]})
    return out
