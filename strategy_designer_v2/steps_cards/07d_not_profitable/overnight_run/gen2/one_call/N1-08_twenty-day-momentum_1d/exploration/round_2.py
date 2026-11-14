def explore(data):
    import numpy as np, pandas as pd
    out = {}
    nb = []; dr = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = pd.Series(b["close"].values)
            f = b["forecast"].values
            a = b["postRebalance_current_allocation"].values
            r1 = cl.pct_change()
            p20 = cl.pct_change(20); p60 = cl.pct_change(60)
            ma100 = cl.rolling(100, min_periods=60).mean()
            vol = r1.rolling(20).std()
            flips = pd.Series(np.sign(f)).diff().abs().gt(0).rolling(20).sum()
            for i in range(60, len(b) - 20, 20):
                nb.append(dict(coin=c, win=w, f=f[i], fwd=cl[i+20]/cl[i]-1, p20=p20[i], p60=p60[i],
                               above=cl[i] > ma100[i] if not np.isnan(ma100[i]) else np.nan, vol=vol[i], flips=flips[i]))
            # daily book pnl attributed by side and by trend state
            nxt = r1.shift(-1)
            for i in range(60, len(b) - 1):
                dr.append(dict(coin=c, side=np.sign(a[i]), pnl=a[i]*nxt[i], above=(cl[i] > ma100[i]) if not np.isnan(ma100[i]) else np.nan,
                               up60=p60[i] > 0, flip=np.sign(f[i]) != np.sign(f[i-1])))
    N = pd.DataFrame(nb).dropna(subset=["f", "p60"])
    N["fwd_ex"] = N["fwd"] - N.groupby("coin")["fwd"].transform("mean")
    t = lambda x: x.mean()/x.std()*np.sqrt(len(x))
    N["s20"] = np.sign(N["f"])*N["fwd"]; N["s60"] = np.sign(N["p60"])*N["fwd"]
    out["sign20_vs_sign60_nonoverlap"] = pd.DataFrame({"n": [len(N)]*2, "mean": [N["s20"].mean(), N["s60"].mean()], "t": [t(N["s20"]), t(N["s60"])]}, index=["sign of 20d", "sign of 60d"])
    N["state"] = np.where(N["p60"] > 0, "up60", "down60")
    out["fwd_by_60state_and_20side"] = N.groupby(["state", np.sign(N["f"])]).agg(n=("f", "size"), fwd=("fwd", "mean"), fwd_ex=("fwd_ex", "mean"), t=("fwd_ex", t))
    N2 = N.dropna(subset=["above"])
    out["fwd_by_ma100_and_20side"] = N2.groupby(["above", np.sign(N2["f"])]).agg(n=("f", "size"), fwd=("fwd", "mean"), fwd_ex=("fwd_ex", "mean"), t=("fwd_ex", t))
    N["fq"] = pd.qcut(N["f"], 5, labels=False)
    out["fwd_by_fq_and_vol"] = N.groupby(["fq", pd.qcut(N["vol"], 2, labels=["calm", "volatile"])]).agg(n=("f", "size"), fwd_ex=("fwd_ex", "mean"))
    D = pd.DataFrame(dr).dropna(subset=["pnl"])
    out["daily_pnl_by_side_up60"] = D.groupby(["up60", "side"]).agg(n=("pnl", "size"), mean_bp=("pnl", lambda x: x.mean()*1e4), t=("pnl", t))
    out["daily_pnl_flip_days"] = D.groupby("flip").agg(n=("pnl", "size"), mean_bp=("pnl", lambda x: x.mean()*1e4))
    out["sign_flips_per_20bars_mean"] = float(N["flips"].mean())
    return out
