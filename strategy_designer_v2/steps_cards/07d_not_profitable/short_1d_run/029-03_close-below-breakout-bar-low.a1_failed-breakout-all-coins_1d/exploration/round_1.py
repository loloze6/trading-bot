import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars, trades, days = data["bars"], data["trades"], data["days"]
    out = {}
    # exposure and trades
    rows = []
    for c in bars:
        nb = 0; nact = 0; nsit = 0; ntr = 0; pnl = []
        for w, b in bars[c].items():
            nb += len(b)
            a = b["postRebalance_current_allocation"].fillna(0)
            nact += (a.abs() > 1e-9).sum()
            nsit += (b["debug_info.components.fail_depth.last_history_value"].fillna(0).abs() > 0).sum()
        for w, t in trades[c].items():
            ntr += len(t); pnl += list(t["net_profit_loss_percent"].dropna())
        rows.append(dict(coin=c, bars=nb, situation_share=nsit/nb, active_share=nact/nb, trades=ntr,
                         mean_net_pnl=np.mean(pnl) if pnl else np.nan))
    out["exposure"] = pd.DataFrame(rows).set_index("coin")
    allp = np.concatenate([trades[c][w]["net_profit_loss_percent"].dropna().values for c in trades for w in trades[c]])
    out["trades_net_pnl"] = pd.Series(dict(n=len(allp), mean=allp.mean(), median=np.median(allp), win=(allp>0).mean(),
                                          t=allp.mean()/(allp.std(ddof=1)/np.sqrt(len(allp)))))
    # alternative situations, recomputed from prices
    H = 5
    def cases(variant, fw):
        res = []
        for c in bars:
            # drift
            r_all = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl)-H, H)
                r_all += list(cl[idx+H]/cl[idx]-1)
            drift = np.mean(r_all) if r_all else 0
            sd = np.std(r_all) if r_all else np.nan
            for w, b in bars[c].items():
                cl = b["close"].values; hi = b["high"].values; lo = b["low"].values
                ph = pd.Series(hi).shift(1).rolling(20).max().values
                bo = cl > ph
                ret20 = pd.Series(cl).pct_change(20).values
                n = len(cl)
                for g in range(0, n-H, H):
                    for i in range(g, min(g+H, n-H)):
                        # most recent breakout in previous fw days
                        js = [j for j in range(max(0, i-fw), i) if bo[j]]
                        if not js or bo[i]: continue
                        j = js[-1]
                        if variant == "below_bo_low":
                            ref = lo[j]
                        else:
                            ref = ph[j]
                        if cl[i] >= ref: continue
                        depth = (ref-cl[i])/ref
                        r = cl[i+H]/cl[i]-1
                        res.append(dict(coin=c, win=w, depth=depth, unusual=-(r-drift), total=-r,
                                        strength=-(r-drift)/sd, ret20=ret20[i], year=b["timestamp"].iloc[i].year if hasattr(b["timestamp"].iloc[i],'year') else pd.Timestamp(b["timestamp"].iloc[i]).year))
                        break
        return pd.DataFrame(res)
    summ = []
    store = {}
    for v in ["below_bo_low", "below_old_high"]:
        for fw in [3, 5, 10]:
            d = cases(v, fw); store[(v,fw)] = d
            m = d["unusual"]
            summ.append(dict(variant=v, fail_window=fw, cases=len(d), unusual=m.mean(),
                             t=m.mean()/(m.std(ddof=1)/np.sqrt(len(d))), total=d["total"].mean(),
                             strength=d["strength"].mean(), rho=stats.spearmanr(d["depth"], m).correlation))
    out["alt_situations"] = pd.DataFrame(summ)
    # regime split for broad variant
    d = store[("below_old_high", 10)].copy()
    d["trend20"] = pd.qcut(d["ret20"], 3, labels=["low", "mid", "high"])
    out["broad_by_ret20"] = d.groupby("trend20").agg(n=("unusual","size"), unusual=("unusual","mean"), total=("total","mean"))
    d["dq"] = pd.qcut(d["depth"], 3, labels=["shallow","mid","deep"])
    out["broad_by_depth"] = d.groupby("dq").agg(n=("unusual","size"), unusual=("unusual","mean"))
    out["broad_by_year"] = d.groupby("year").agg(n=("unusual","size"), unusual=("unusual","mean"))
    # book daily
    br = pd.concat([days[c][w][["book_return"]].assign(c=c) for c in days for w in days[c]])
    out["book_daily"] = pd.Series(dict(mean=br["book_return"].mean(), share_nonzero=(br["book_return"].abs()>1e-12).mean()))
    return out
