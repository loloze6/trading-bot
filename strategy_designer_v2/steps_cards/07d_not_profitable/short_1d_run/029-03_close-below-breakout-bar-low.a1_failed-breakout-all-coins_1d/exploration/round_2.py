import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars, trades, days = data["bars"], data["trades"], data["days"]
    out = {}
    rows = []
    allp = []
    for c in bars:
        nb = 0; nact = 0; nsit = 0; ntr = 0; absal = []
        for w, b in bars[c].items():
            nb += len(b)
            a = b["postRebalance_current_allocation"].fillna(0)
            nact += (a.abs() > 1e-9).sum()
            absal += list(a[a.abs() > 1e-9].abs())
            col = "debug_info.components.fail_depth.last_history_value"
            if col in b: nsit += (b[col].fillna(0).abs() > 0).sum()
        for w, t in trades.get(c, {}).items():
            if t is None or len(t) == 0: continue
            ntr += len(t)
            for k in ["net_profit_loss_percent", "profit_loss_percent"]:
                if k in t.columns:
                    allp += list(pd.to_numeric(t[k], errors="coerce").dropna()); break
        rows.append(dict(coin=c, bars=nb, situation_share=nsit/nb, active_share=nact/nb,
                         mean_abs_alloc=np.mean(absal) if absal else np.nan, trades=ntr))
    out["exposure"] = pd.DataFrame(rows).set_index("coin")
    allp = np.array(allp)
    if len(allp) > 1:
        out["trades_pnl"] = pd.Series(dict(n=len(allp), mean=allp.mean(), median=np.median(allp),
                                          win=(allp > 0).mean(), t=allp.mean()/(allp.std(ddof=1)/np.sqrt(len(allp)))))
    H = 5
    def cases(variant, fw):
        res = []
        for c in bars:
            r_all = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl)-H, H)
                r_all += list(cl[idx+H]/cl[idx]-1)
            if not r_all: continue
            drift = np.mean(r_all); sd = np.std(r_all)
            for w, b in bars[c].items():
                cl = b["close"].values; hi = b["high"].values; lo = b["low"].values
                ph = pd.Series(hi).shift(1).rolling(20).max().values
                bo = cl > ph
                ret20 = pd.Series(cl).pct_change(20).values
                yr = pd.to_datetime(b["timestamp"]).dt.year.values
                n = len(cl)
                for g in range(0, n-H, H):
                    for i in range(g, min(g+H, n-H)):
                        if bo[i]: continue
                        js = [j for j in range(max(0, i-fw), i) if bo[j]]
                        if not js: continue
                        j = js[-1]
                        ref = lo[j] if variant == "below_bo_low" else ph[j]
                        if cl[i] >= ref: continue
                        r = cl[i+H]/cl[i]-1
                        res.append(dict(coin=c, win=w, depth=(ref-cl[i])/ref, unusual=-(r-drift), total=-r,
                                        strength=-(r-drift)/sd, ret20=ret20[i], year=yr[i]))
                        break
        return pd.DataFrame(res)
    summ = []; store = {}
    for v in ["below_bo_low", "below_old_high"]:
        for fw in [3, 5, 10]:
            d = cases(v, fw); store[(v, fw)] = d
            m = d["unusual"]
            summ.append(dict(variant=v, fail_window=fw, cases=len(d), unusual=m.mean(),
                             t=m.mean()/(m.std(ddof=1)/np.sqrt(len(d))), total=d["total"].mean(),
                             strength=d["strength"].mean(), rho=stats.spearmanr(d["depth"], m).correlation))
    out["alt_situations"] = pd.DataFrame(summ)
    for key in [("below_bo_low", 3), ("below_old_high", 10)]:
        d = store[key].dropna(subset=["ret20"]).copy()
        d["trend20"] = pd.qcut(d["ret20"], 3, labels=["low", "mid", "high"])
        out["by_ret20_%s_%d" % key] = d.groupby("trend20").agg(n=("unusual", "size"), unusual=("unusual", "mean"),
                                                             total=("total", "mean"), ret20=("ret20", "mean"))
        d["dq"] = pd.qcut(d["depth"].rank(method="first"), 3, labels=["shallow", "mid", "deep"])
        out["by_depth_%s_%d" % key] = d.groupby("dq").agg(n=("unusual", "size"), unusual=("unusual", "mean"),
                                                        total=("total", "mean"))
        out["by_year_%s_%d" % key] = d.groupby("year").agg(n=("unusual", "size"), unusual=("unusual", "mean"),
                                                         total=("total", "mean"))
    # book daily: pooled across coins per day, and drawdown by window
    allb = []
    for c in days:
        for w, dd in days[c].items():
            allb.append(dd[["day", "book_return", "coin_return"]].assign(c=c, w=w))
    br = pd.concat(allb)
    out["book_daily"] = pd.Series(dict(mean=br["book_return"].mean(), coin_mean=br["coin_return"].mean(),
                                       share_nonzero=(br["book_return"].abs() > 1e-12).mean()))
    wsum = br.groupby("w").agg(book=("book_return", "sum"), coin=("coin_return", "mean"))
    out["book_by_window"] = wsum
    return out
