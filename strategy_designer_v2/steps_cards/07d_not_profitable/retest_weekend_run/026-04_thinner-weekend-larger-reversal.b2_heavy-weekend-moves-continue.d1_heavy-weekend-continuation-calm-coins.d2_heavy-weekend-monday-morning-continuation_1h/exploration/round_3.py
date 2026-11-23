def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    def q(x, k=4):
        return pd.qcut(pd.Series(x).rank(method="first"), k, labels=False)
    def st(x):
        x = pd.Series(x).dropna(); n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean()/x.std()*np.sqrt(n) if n > 2 and x.std() > 0 else np.nan})
    def safe(name, fn):
        try:
            out[name] = fn()
        except Exception as e:
            out[name] = "err: " + str(e)[:80]
    wins = sorted({w for c in coins for w in days[c]}, key=lambda s: int(s[1:]))
    chain = []
    for w in wins:
        dfs = [days[c][w].set_index("day")["book_return"].rename(c) for c in coins if w in days[c]]
        m = pd.concat(dfs, axis=1).mean(axis=1).dropna()
        chain.append(pd.DataFrame({"w": w, "r": m.values}))
    ch = pd.concat(chain, ignore_index=True)
    v = (1+ch.r).cumprod(); dd = v/v.cummax()-1
    ch["dd"] = dd.values
    safe("dd_by_window", lambda: ch.groupby("w").agg(ret=("r", lambda x: (1+x).prod()-1), mindd=("dd", "min"), worstday=("r", "min")).reindex(wins))
    i_min = int(np.argmin(dd.values)); i_peak = int(np.argmax(v.values[:i_min+1]))
    out["deepest_fall"] = pd.Series({"depth": dd.values[i_min], "days_peak_to_trough": i_min-i_peak,
                                     "w_peak": ch.w.iloc[i_peak], "w_trough": ch.w.iloc[i_min],
                                     "years": len(ch)/365, "chain_total": v.values[-1]-1})
    rows = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b.timestamp, utc=True)
            wd = ts.dt.weekday.values; hr = ts.dt.hour.values
            yrs = ts.dt.year.values
            epoch = (ts.astype("int64").values // 10**9) // (7*86400)
            cl = b.close.values.astype(float); vol = b.volume.values.astype(float)
            r1 = np.r_[np.nan, np.diff(np.log(cl))]
            al = b.postRebalance_current_allocation.values.astype(float)
            fc = b.forecast.values.astype(float)
            idx = np.where((wd == 6) & (hr == 23))[0]
            for i in idx:
                if i < 216 or i+24 >= len(b): continue
                wk = cl[i]/cl[i-48]-1
                if wk == 0: continue
                vr = vol[i-47:i+1].mean()/max(vol[i-167:i-47].mean(), 1e-12)
                pw = cl[i-48]/cl[i-168]-1
                rv = np.nanstd(r1[max(1, i-720):i+1])*np.sqrt(48)
                rvs = np.nanstd(r1[i-47:i+1])*np.sqrt(48)
                s = np.sign(wk)
                path = cl[i+1:i+13]/cl[i]-1
                tr30 = cl[i]/cl[max(0, i-720)]-1
                rows.append(dict(c=c, w=w, yr=yrs[i], wk=wk, vr=vr, pw=pw, rv=rv, rvs=rvs, f=fc[i], s=s,
                                 sfwd=s*(cl[i+12]/cl[i]-1), sfwd24=s*(cl[i+24]/cl[i]-1),
                                 sfwd6=s*(cl[i+6]/cl[i]-1),
                                 mae=(s*path).min(), z=abs(wk)/rv, alloc=al[i],
                                 pnl=al[i]*(cl[i+12]/cl[i]-1), sun=s*(cl[i]/cl[i-24]-1),
                                 tr30=s*tr30, wid=int(epoch[i])))
    d = pd.DataFrame(rows)
    d["heavy"] = d.vr >= 1
    h = d[d.heavy & (d.f != 0)].copy()
    L = d[~d.heavy].copy()
    out["n_cases"] = pd.Series({"heavy_signal": len(h), "light": len(L)})
    safe("heavy_vs_light", lambda: d.groupby("heavy").sfwd.apply(st).unstack())
    h["side"] = np.where(h.s > 0, "long", "short")
    safe("by_side", lambda: pd.concat({"sfwd": h.groupby("side").sfwd.apply(st).unstack(), "pnl": h.groupby("side").pnl.apply(st).unstack()}, axis=1))
    safe("by_coin", lambda: h.groupby("c").sfwd.apply(st).unstack())
    safe("by_year", lambda: h.groupby("yr").agg(sf=("sfwd", "mean"), pnl=("pnl", "mean"), n=("sfwd", "size")))
    safe("horizons", lambda: pd.DataFrame({"h6": st(h.sfwd6), "h12": st(h.sfwd), "h24": st(h.sfwd24)}))
    h["zq"] = q(h.z); safe("by_zq", lambda: h.groupby("zq").agg(z=("z", "mean"), sf=("sfwd", "mean"), sd=("sfwd", "std"), pnl=("pnl", "mean"), n=("sfwd", "size")))
    h["vq"] = q(h.vr); safe("by_vrq", lambda: h.groupby("vq").agg(vr=("vr", "mean"), sf=("sfwd", "mean"), sd=("sfwd", "std"), n=("sfwd", "size")))
    h["rvq"] = q(h.rv); safe("by_rvq", lambda: h.groupby("rvq").agg(rv=("rv", "mean"), sf=("sfwd", "mean"), sfz=("sfwd", lambda x: 0), pnl=("pnl", "mean"), pnlsd=("pnl", "std"), alloc=("alloc", lambda x: x.abs().mean()), n=("sfwd", "size")))
    h["fq"] = q(h.f.abs()); safe("by_absf_q", lambda: h.groupby("fq").agg(sf=("sfwd", "mean"), pnl=("pnl", "mean"), pnlsd=("pnl", "std"), alloc=("alloc", lambda x: x.abs().mean()), n=("sfwd", "size")))
    h["sunagree"] = h.sun > 0; L["sunagree"] = L.sun > 0
    safe("sunday_same_dir_heavy", lambda: h.groupby("sunagree").sfwd.apply(st).unstack())
    safe("sunday_same_dir_light", lambda: L.groupby("sunagree").sfwd.apply(st).unstack())
    h["tragree"] = h.tr30 > 0; L["tragree"] = L.tr30 > 0
    safe("trend30_agree_heavy", lambda: h.groupby("tragree").agg(sf=("sfwd", "mean"), t=("sfwd", lambda x: st(x)["t"]), pnl=("pnl", "mean"), pnlsd=("pnl", "std"), n=("sfwd", "size")))
    safe("trend30_agree_light", lambda: L.groupby("tragree").sfwd.apply(st).unstack())
    h["rsq"] = q(h.rvs/h.rv, 3); safe("weekend_vol_vs_usual", lambda: h.groupby("rsq").agg(sf=("sfwd", "mean"), pnl=("pnl", "mean"), pnlsd=("pnl", "std"), n=("sfwd", "size")))
    safe("mae_q", lambda: h.mae.quantile([.05, .1, .25, .5]))
    def stops():
        r = {}
        for k in [-0.02, -0.03, -0.05]:
            hit = h.mae <= k
            r[str(k)] = {"hits": hit.sum(), "fwd_if_hit": h.sfwd[hit].mean(), "capped_mean": np.where(hit, k, h.sfwd).mean()}
        return pd.DataFrame(r).T
    safe("stops", stops)
    wkp = h.groupby("wid").agg(pnl=("pnl", "mean"), n=("pnl", "size"), samedir=("s", lambda x: abs(x.mean())))
    safe("week_pnl_q", lambda: wkp.pnl.quantile([.01, .05, .1, .5, .9]))
    safe("week_by_samedir", lambda: wkp.assign(sd1=wkp.samedir == 1).groupby("sd1").agg(mean=("pnl", "mean"), sd=("pnl", "std"), cnt=("pnl", "size"), n=("n", "mean")))
    worst = wkp.nsmallest(15, "pnl").index
    cols = {"sfwd": "mean", "z": "mean", "vr": "mean", "rv": "mean", "sun": "mean", "tr30": "mean", "s": "mean"}
    safe("worst15_weeks_vs_all", lambda: pd.DataFrame({"worst": h[h.wid.isin(worst)].agg(cols), "all": h.agg(cols)}))
    safe("worst_weeks_year", lambda: h[h.wid.isin(worst)].groupby("yr").size())
    return out
