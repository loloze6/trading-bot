def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 18
    bars = []
    for coin, ws in data["bars"].items():
        rets = []
        for w, b in ws.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            rets += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(rets)
        for w, b in ws.items():
            c = b["close"].values
            f = b["forecast"].values
            al = b["postRebalance_current_allocation"].values
            nr = np.append(c[1:] / c[:-1] - 1, np.nan)
            # bars since last f<0
            last = -10**9; since = np.zeros(len(c))
            for i in range(len(c)):
                if f[i] < 0: last = i
                since[i] = i - last
            up = np.diff(np.append(c[0], c)) > 0
            streak = np.zeros(len(c)); s = 0
            for i in range(len(c)):
                s = s + 1 if up[i] else 0; streak[i] = s
            ma = pd.Series(c).rolling(180, min_periods=1).mean().values
            ret30 = pd.Series(c).pct_change(180).values
            bars.append(pd.DataFrame({"coin": coin, "w": w, "f": f, "al": al, "nr": nr, "g": al * nr,
                                      "since": since, "streak": streak, "above": c > ma, "ret30": ret30}))
    B = pd.concat(bars).dropna(subset=["nr"])
    B["state"] = np.where(B["al"] >= -1e-9, "flat", np.where(B["f"] < 0, "short,f<0", "short,f=0"))
    out["gain by state"] = B.groupby("state").agg(bars=("g", "size"), mean_gain_bp=("g", lambda x: x.mean() * 1e4),
                                                  sum_gain=("g", "sum"), coin_nr_bp=("nr", lambda x: x.mean() * 1e4),
                                                  share_above_ma=("above", "mean"))
    S = B[B["al"] < -1e-9].copy()
    S["sinceb"] = pd.cut(S["since"], [-1, 0, 18, 36, 72, 144, 10**9], labels=["0", "1-18", "19-36", "37-72", "73-144", ">144"])
    out["short bars by bars since last f<0"] = S.groupby("sinceb").agg(bars=("g", "size"), gain_bp=("g", lambda x: x.mean() * 1e4),
                                                                      coin_bp=("nr", lambda x: x.mean() * 1e4), above=("above", "mean"))
    # signal bars: forward return over 6,18,36,72 bars, by 30d return tercile
    sig = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            c = b["close"].values; f = b["forecast"].values
            r30 = pd.Series(c).pct_change(180).values
            for s0 in range(0, len(c) - H, H):
                nz = np.where(f[s0:s0 + H] < 0)[0]
                if len(nz) == 0: continue
                t = s0 + nz[0]
                d = {"coin": coin, "r30": r30[t]}
                for h in (6, 18, 36, 72):
                    d[f"short_{h}"] = -(c[t + h] / c[t] - 1) if t + h < len(c) else np.nan
                sig.append(d)
    G = pd.DataFrame(sig)
    out["case short return by horizon"] = G[["short_6", "short_18", "short_36", "short_72"]].agg(["mean", "count"])
    G["r30q"] = pd.qcut(G["r30"].rank(method="first"), 4, labels=False)
    out["case by 30d return quartile (0=most fallen)"] = G.groupby("r30q").agg(n=("short_18", "size"), r30=("r30", "mean"),
                                                                             s18=("short_18", "mean"), s72=("short_72", "mean"))
    # book daily by window short share
    return out
