def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    ev = []
    hold = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            nxt = np.r_[c[1:] / c[:-1] - 1, np.nan]
            g = alloc * nxt
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            wick = (np.minimum(b["open"], b["close"]) - b["low"]) / rng
            r1 = b["close"].pct_change()
            sd = r1.rolling(20).std()
            z = r1 / sd
            vr = b["volume"] / b["volume"].shift(1).rolling(20).median()
            for i in range(len(b)):
                if b["regime"].iloc[i] == "mean_reversion":
                    f = {}
                    for h in (1, 2, 3, 5, 10):
                        f["r%d" % h] = c[i + h] / c[i] - 1 if i + h < len(b) else np.nan
                    ev.append(dict(coin=coin, w=w, fc=b["forecast"].iloc[i], wick=wick.iloc[i],
                                   z=z.iloc[i], vr=vr.iloc[i], alloc=alloc[i],
                                   year=pd.Timestamp(b["timestamp"].iloc[i]).year, **f))
            # holding run lengths
            run = 0
            for a in alloc:
                if abs(a) > 1e-9: run += 1
                elif run: hold.append(run); run = 0
            if run: hold.append(run)
            rows.append(dict(coin=coin, w=w, gain=np.nansum(g), inbars=(np.abs(alloc) > 1e-9).sum(),
                             meanalloc=np.mean(np.abs(alloc[np.abs(alloc) > 1e-9])) if (np.abs(alloc) > 1e-9).any() else np.nan))
    E = pd.DataFrame(ev)
    R = pd.DataFrame(rows)
    out["per coin gain/inbars"] = R.groupby("coin")[["gain", "inbars", "meanalloc"]].agg(["sum", "mean"])
    out["holding run lengths"] = pd.Series(hold).describe()
    out["n events"] = len(E)
    out["event mean fwd returns"] = E[["r1", "r2", "r3", "r5", "r10"]].agg(["mean", "median", "count"])
    out["t of fwd"] = pd.Series({k: stats.ttest_1samp(E[k].dropna(), 0).statistic for k in ["r1", "r2", "r3", "r5", "r10"]})
    E["wq"] = pd.qcut(E["wick"], 3, labels=["lo", "mid", "hi"])
    out["by wick tercile"] = E.groupby("wq")[["r1", "r3", "r5", "r10", "alloc"]].mean().join(E.groupby("wq").size().rename("n"))
    E["zq"] = pd.qcut(E["z"], 3, labels=["deep", "mid", "shallow"])
    out["by z tercile"] = E.groupby("zq")[["r1", "r3", "r5", "r10"]].mean().join(E.groupby("zq").size().rename("n"))
    out["by year"] = E.groupby("year")[["r1", "r3", "r10"]].mean().join(E.groupby("year").size().rename("n"))
    out["by coin"] = E.groupby("coin")[["r1", "r3", "r10"]].mean().join(E.groupby("coin").size().rename("n"))
    out["fc>0 share, alloc>0 share"] = pd.Series({"fc>0": (E.fc > 0).mean(), "alloc>0": (E.alloc > 0).mean()})
    # fees
    tr = pd.concat([t for ws in data["trades"].values() for t in ws.values()])
    out["trades"] = tr[["profit_loss_percent", "net_profit_loss_percent", "duration_minutes"]].describe()
    return out
