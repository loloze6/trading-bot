def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    out = {}
    # book's daily gain by the coin's 60-day trend, on bars in a position
    rows = []; cases = []; allg = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            r1 = b.close.pct_change()
            r60 = b.close / b.close.shift(60) - 1
            r5 = b.close / b.close.shift(5) - 1
            cl = (b.close - b.low) / (b.high - b.low)
            vol30 = r1.rolling(30).std(); volmed = vol30.rolling(365, min_periods=60).median()
            agi = np.where(vol30.isna() | volmed.isna(), "na", np.where(vol30 > volmed, "agit", "calm"))
            tr = np.where(r60.isna(), "na", np.where(r60 > 0.10, "rising", np.where(r60 < -0.10, "falling", "choppy")))
            pos = b.postRebalance_current_allocation.fillna(0)
            g = pos * (b.close.shift(-1) / b.close - 1)
            rows.append(pd.DataFrame({"tr": tr, "agi": agi, "pos": pos, "g": g, "w": w}))
            sig = (cl >= 0.8) & (r5 < 0)
            f2 = b.close.shift(-2) / b.close - 1; f5 = b.close.shift(-5) / b.close - 1
            n = len(b)
            for s in range(0, n - 5, 5):
                allg.append(dict(coin=c, tr=tr[s], agi=agi[s], sig=bool(sig[s]), f2=f2[s], f5=f5[s], r5=r5[s]))
                idx = [j for j in range(s, s + 5) if sig[j]]
                if idx:
                    j = idx[0]
                    cases.append(dict(coin=c, w=w, tr=tr[j], agi=agi[j], r5=r5[j], f2=f2[j], f5=f5[j]))
    R = pd.concat(rows); R = R[R.pos != 0]
    out["book_gain_by_trend"] = R.groupby("tr").agg(n=("g", "size"), mean_gain=("g", "mean"), total=("g", "sum"))
    out["book_gain_by_trend_agit"] = R.groupby(["tr", "agi"]).agg(n=("g", "size"), mean_gain=("g", "mean"), total=("g", "sum"))
    C = pd.DataFrame(cases); G = pd.DataFrame(allg)
    def t(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    C["s5"] = -C.f5; C["s2"] = -C.f2; G["s5"] = -G.f5
    notr = C[C.tr != "rising"]
    out["not_rising_s5"] = t(notr.s5); out["not_rising_s2"] = t(notr.s2)
    out["rising_s5"] = t(C[C.tr == "rising"].s5)
    notr = notr.copy(); notr["dq"] = pd.qcut(notr.r5, 3, labels=False)
    out["not_rising_by_depth"] = notr.groupby("dq").agg(r5=("r5", "mean"), n=("s5", "size"), s5=("s5", "mean"), s2=("s2", "mean"))
    out["sig_by_trend_agit"] = C.groupby(["tr", "agi"]).agg(n=("s5", "size"), s5=("s5", "mean"), s2=("s2", "mean"))
    out["nosig_by_trend_agit"] = G[~G.sig].groupby(["tr", "agi"]).agg(n=("s5", "size"), s5=("s5", "mean"))
    out["sig_not_rising_by_window"] = notr.groupby("w").agg(n=("s5", "size"), s5=("s5", "mean"))
    return out
