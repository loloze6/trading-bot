import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; out = {}
    # basic: regime, forecast, positions, trades
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            rows.append(pd.DataFrame({"coin": c, "win": w, "regime": b["regime"].values,
                "fc": b["forecast"].values, "pos": b["postRebalance_current_allocation"].values}))
    allb = pd.concat(rows)
    out["regime_share"] = allb.groupby("regime").agg(n=("fc","size"), fc_nonzero=("fc", lambda s: (s!=0).mean()),
        fc_mean=("fc","mean"), pos_nonzero=("pos", lambda s: (s.abs()>1e-9).mean()), pos_mean=("pos","mean"))
    tr = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            if len(t): tt = t.copy(); tt["coin"] = c; tr.append(tt)
    if tr:
        T = pd.concat(tr)
        out["trades"] = T.groupby("side").agg(n=("net_profit_loss_percent","size"),
            mean_net=("net_profit_loss_percent","mean"), med_net=("net_profit_loss_percent","median"),
            win=("net_profit_loss_percent", lambda s: (s>0).mean()),
            dur_days=("duration_minutes", lambda s: s.mean()/1440), fc_entry=("entry_forecast","mean"))
    # coin drift and usual move per horizon
    def grid(h, L):
        recs = []
        for c in bars:
            # drift
            fr = []
            for w, b in bars[c].items():
                cl = b["close"].values
                for i in range(0, len(cl)-h, h):
                    fr.append(cl[i+h]/cl[i]-1)
            fr = np.array(fr); drift = fr.mean() if len(fr) else 0; sd = fr.std() if len(fr)>1 else np.nan
            for w, b in bars[c].items():
                cl = b["close"].values; reg = b["regime"].values; fc = b["forecast"].values
                lr = np.log(cl[1:]/cl[:-1])
                for i in range(0, len(cl)-h, h):
                    if i < L: continue
                    past = cl[i]/cl[i-L]-1
                    vol = np.std(lr[max(0,i-14):i])*np.sqrt(365) if i>=5 else np.nan
                    recs.append((c, w, i, past, cl[i+h]/cl[i]-1-drift, (cl[i+h]/cl[i]-1-drift)/sd, sd, reg[i], fc[i], vol))
        return pd.DataFrame(recs, columns=["coin","win","i","past","ex","z","sd","regime","fc","vol"])
    # tested situation on 30-day grid
    g = grid(30, 0)
    mr = g[g.regime=="mean_reversion"]
    if len(mr) > 3:
        med = mr.fc.median(); up = mr[mr.fc>med].ex; lo = mr[mr.fc<=med].ex
        out["mr_30d"] = pd.Series({"n": len(mr), "mean_ex": mr.ex.mean(), "t_mean": stats.ttest_1samp(mr.ex,0).statistic,
            "n_up": len(up), "n_lo": len(lo), "up_minus_lo": up.mean()-lo.mean(),
            "welch_t": stats.ttest_ind(up, lo, equal_var=False).statistic, "fc_pos_mean_ex": mr[mr.fc>0].ex.mean(), "n_fc_pos": (mr.fc>0).sum()})
    out["by_regime_30d"] = g.groupby("regime").ex.agg(["size","mean", lambda s: stats.ttest_1samp(s,0).statistic])
    # past-L vs next-h, all bars, quintiles of scaled past
    for h, L in [(30,30),(14,14),(7,7),(7,30),(3,3),(1,1)]:
        gg = grid(h, L).dropna(subset=["past"])
        gg["ps"] = gg.groupby("coin").past.transform(lambda s: (s - s.mean())/s.std())
        gg["q"] = pd.qcut(gg.ps, 5, labels=False)
        tab = gg.groupby("q").agg(n=("ex","size"), past=("past","mean"), ex=("ex","mean"), z=("z","mean"))
        r, p = stats.spearmanr(gg.ps, gg.z)
        tab.loc["rho"] = [len(gg), r, p, np.nan]
        out[f"past{L}_next{h}"] = tab
    # vol level vs next 7d
    gv = grid(7, 14).dropna(subset=["vol"])
    gv["vr"] = gv.groupby("coin").vol.rank(pct=True)
    gv["q"] = pd.cut(gv.vr, [0,.2,.4,.6,.8,1], labels=False)
    out["vol_next7"] = gv.groupby("q").agg(n=("ex","size"), ex=("ex","mean"), z=("z","mean"),
        t=("z", lambda s: stats.ttest_1samp(s,0).statistic))
    # weekday daily returns
    dd = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            x = d.copy(); x["coin"] = c; dd.append(x)
    D = pd.concat(dd).dropna(subset=["coin_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["ex"] = D.coin_return - D.groupby("coin").coin_return.transform("mean")
    out["weekday"] = D.groupby("wd").ex.agg(["size","mean", lambda s: stats.ttest_1samp(s,0).statistic])
    return out
