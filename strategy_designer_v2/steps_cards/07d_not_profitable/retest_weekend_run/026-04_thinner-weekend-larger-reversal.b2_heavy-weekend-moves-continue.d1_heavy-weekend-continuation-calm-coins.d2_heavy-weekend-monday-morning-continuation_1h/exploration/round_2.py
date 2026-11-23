def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    def q(x, k=4):
        return pd.qcut(x.rank(method="first"), k, labels=False)
    def st(x):
        x = pd.Series(x).dropna(); n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean()/x.std()*np.sqrt(n) if n > 2 and x.std() > 0 else np.nan})
    wins = sorted({w for c in coins for w in days[c]}, key=lambda s: int(s[1:]))
    chain = []
    for w in wins:
        dfs = [days[c][w].set_index("day")["book_return"].rename(c) for c in coins if w in days[c]]
        m = pd.concat(dfs, axis=1).mean(axis=1).dropna()
        chain.append(pd.DataFrame({"w": w, "day": m.index, "r": m.values}))
    ch = pd.concat(chain, ignore_index=True)
    v = (1+ch.r).cumprod(); dd = v/v.cummax()-1
    ch["dd"] = dd.values
    out["dd_by_window"] = ch.groupby("w").agg(ret=("r", lambda x: (1+x).prod()-1), mindd=("dd", "min"), worstday=("r", "min")).reindex(wins)
    i_min = int(np.argmin(dd.values)); i_peak = int(np.argmax(v.values[:i_min+1]))
    out["deepest_fall"] = pd.Series({"depth": dd.values[i_min], "days_peak_to_trough": i_min-i_peak,
                                     "w_peak": ch.w.iloc[i_peak], "w_trough": ch.w.iloc[i_min],
                                     "years": len(ch)/365, "chain_total": v.values[-1]-1})
    rows = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b.timestamp)
            cl = b.close.values.astype(float); vol = b.volume.values.astype(float)
            r1 = np.r_[np.nan, np.diff(np.log(cl))]
            idx = np.where((ts.dt.weekday.values == 6) & (ts.dt.hour.values == 23))[0]
            al = b.postRebalance_current_allocation.values
            for i in idx:
                if i < 216 or i+24 >= len(b): continue
                wk = cl[i]/cl[i-48]-1
                vr = vol[i-47:i+1].mean()/max(vol[i-167:i-47].mean(), 1e-12)
                pw = cl[i-48]/cl[i-168]-1
                rv = np.nanstd(r1[max(1, i-720):i+1])*np.sqrt(48)
                rvs = np.nanstd(r1[i-47:i+1])*np.sqrt(48)
                f = b.forecast.iloc[i]
                s = np.sign(wk)
                path = cl[i+1:i+13]/cl[i]-1
                lastday = cl[i]/cl[i-24]-1
                rows.append(dict(c=c, w=w, yr=ts.iloc[i].year, wk=wk, vr=vr, pw=pw, rv=rv, rvs=rvs, f=f, s=s,
                                 sfwd=s*(cl[i+12]/cl[i]-1), sfwd24=s*(cl[i+24]/cl[i]-1),
                                 mae=(s*path).min(), z=abs(wk)/rv, alloc=al[i],
                                 pnl=al[i]*(cl[i+12]/cl[i]-1), sun=s*lastday, sat=s*(cl[i-24]/cl[i-48]-1),
                                 wid=(ts.iloc[i]-pd.Timestamp("2000-01-02")).days//7))
    d = pd.DataFrame(rows)
    d["heavy"] = d.vr >= 1
    h = d[d.heavy & (d.f != 0)].copy()
    out["heavy_vs_light_signed"] = d.groupby("heavy").sfwd.apply(st).unstack()
    h["side"] = np.where(h.s > 0, "long", "short")
    out["by_side"] = h.groupby("side").sfwd.apply(st).unstack()
    out["by_side_pnl"] = h.groupby("side").pnl.apply(st).unstack()
    out["by_coin"] = h.groupby("c").sfwd.apply(st).unstack()
    out["by_year"] = h.groupby("yr").sfwd.apply(st).unstack()
    h["agree"] = np.sign(h.pw) == h.s
    out["heavy_by_prevweek_agree"] = h.groupby("agree").sfwd.apply(st).unstack()
    d["agree"] = np.sign(d.pw) == d.s
    out["light_by_agree"] = d[~d.heavy].groupby("agree").sfwd.apply(st).unstack()
    h["sunagree"] = h.sun > 0
    out["heavy_by_sunday_same_dir"] = h.groupby("sunagree").sfwd.apply(st).unstack()
    out["light_by_sunday_same_dir"] = d[~d.heavy].assign(sa=lambda x: x.sun > 0).groupby("sa").sfwd.apply(st).unstack()
    h["zq"] = q(h.z); out["by_zq"] = h.groupby("zq").sfwd.apply(st).unstack()
    h["vq"] = q(h.vr); out["by_vrq"] = h.groupby("vq").sfwd.apply(st).unstack()
    h["rvq"] = q(h.rv); out["by_rvq"] = h.groupby("rvq").agg(sf=("sfwd", "mean"), pnl=("pnl", "mean"), pnlsd=("pnl", "std"), alloc=("alloc", lambda x: x.abs().mean()), n=("sfwd", "size"))
    h["fq"] = q(h.f.abs()); out["by_absf_q"] = h.groupby("fq").agg(sf=("sfwd", "mean"), pnl=("pnl", "mean"), pnlsd=("pnl", "std"), alloc=("alloc", lambda x: x.abs().mean()), n=("sfwd", "size"))
    out["h24_vs_h12"] = pd.DataFrame({"h12": st(h.sfwd), "h24": st(h.sfwd24)})
    out["mae_quantiles"] = h.mae.quantile([.05, .1, .25, .5])
    for k in [-0.02, -0.03, -0.05]:
        hit = h.mae <= k
        out[f"stop{k}"] = pd.Series({"hits": hit.sum(), "fwd_if_hit": h.sfwd[hit].mean(), "capped_mean": np.where(hit, k, h.sfwd).mean()})
    wkp = h.groupby("wid").agg(pnl=("pnl", "mean"), n=("pnl", "size"), samedir=("s", lambda x: abs(x.mean())))
    out["week_pnl_q"] = wkp.pnl.quantile([.01, .05, .1, .5, .9])
    wkp["nq"] = pd.cut(wkp.n, [0, 1, 2, 4, 6])
    out["week_by_ncoins"] = wkp.groupby("nq").agg(mean=("pnl", "mean"), sd=("pnl", "std"), cnt=("pnl", "size"))
    worst = wkp.nsmallest(10, "pnl").index
    out["worst10_weeks_cases"] = h[h.wid.isin(worst)].agg({"sfwd": "mean", "z": "mean", "vr": "mean", "rvs": "mean", "sun": "mean"}).to_frame().T
    out["all_cases_mean"] = h.agg({"sfwd": "mean", "z": "mean", "vr": "mean", "rvs": "mean", "sun": "mean"}).to_frame().T
    h["rvsq"] = q(h.rvs / h.rv)
    out["by_weekend_vol_vs_usual"] = h.groupby("rvsq").agg(sf=("sfwd", "mean"), pnl=("pnl", "mean"), pnlsd=("pnl", "std"), n=("sfwd", "size"))
    tr = pd.concat([t.assign(c=c) for c in coins for w, t in data["trades"][c].items() if len(t)], ignore_index=True)
    out["trades"] = tr.groupby("side").net_profit_loss_percent.agg(["count", "mean", "std", "min"])
    out["dur_q"] = tr.duration_minutes.quantile([.1, .5, .9])
    return out
