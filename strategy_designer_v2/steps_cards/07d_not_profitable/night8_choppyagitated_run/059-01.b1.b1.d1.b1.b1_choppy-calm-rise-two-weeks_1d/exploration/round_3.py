def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; trades = data["trades"]
    out = {}
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = pd.Series(b["close"].values)
            r7 = cl.pct_change(7); sc = r7 / r7.abs().rolling(30).mean()
            r1 = cl.pct_change(1)
            vol30 = r1.rolling(30).std()
            vol7 = r1.rolling(7).std()
            prof = (b["regime"] == "unknown").values
            fc = b["forecast"].fillna(0).values
            n = len(b)
            for i in range(0, n - 14, 14):
                rows.append(dict(coin=c, w=w, sc=sc.iloc[i], prof=prof[i], sig=(fc[i] > 0) and prof[i],
                                 r07=cl.iloc[i + 7] / cl.iloc[i] - 1, r714=cl.iloc[i + 14] / cl.iloc[i + 7] - 1,
                                 r14=cl.iloc[i + 14] / cl.iloc[i] - 1,
                                 r28=(cl.iloc[i + 28] / cl.iloc[i] - 1) if i + 28 < n else np.nan,
                                 vr=vol7.iloc[i] / vol30.iloc[i],
                                 day=pd.to_datetime(b["timestamp"].iloc[i]).floor("D")))
    g = pd.DataFrame(rows)
    g["um14"] = g.r14 - g.groupby("coin").r14.transform("mean")
    g["um28"] = g.r28 - g.groupby("coin").r28.transform("mean")
    g["um714"] = g.r714 - g.groupby("coin").r714.transform("mean")
    def tday(x, col):
        d = x.dropna(subset=[col]).groupby("day")[col].sum()
        return d.mean() / (d.std(ddof=1) / np.sqrt(len(d))) if len(d) > 2 else np.nan
    def S(x):
        return pd.Series(dict(n=len(x), um14=x.um14.mean(), t14=tday(x, "um14"), tot14=x.r14.mean(),
                              um28=x.um28.mean(), t28=tday(x, "um28")))
    sig = g[g.sig]
    out["sig_strong_vs_weak"] = pd.concat({
        "sig_sc_le0.5": S(sig[sig.sc <= 0.5]), "sig_sc_gt0.5": S(sig[sig.sc > 0.5]),
        "prof_nosig_all": S(g[g.prof & ~g.sig]), "noprof_sc_gt0.5": S(g[~g.prof & (g.sc > 0.5)])}, axis=1).T
    # first week path: signal vs non-signal in-profile
    g["p7b"] = pd.cut(g.r07, [-5, -0.05, 0.0, 0.05, 5])
    out["second_week_by_first_week"] = g.groupby(["sig", "p7b"]).apply(
        lambda x: pd.Series(dict(n=len(x), um714=x.um714.mean(), t=tday(x, "um714"))))
    # vol ratio (short-term swing vs month) at signal
    sig = g[g.sig].copy()
    sig["vrb"] = pd.qcut(sig.vr.rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["sig_by_vr"] = sig.groupby("vrb").apply(S)
    out["sig_by_window_strong"] = g[g.sig & (g.sc > 0.5)].groupby("w").agg(n=("um14", "size"), um14=("um14", "mean"))
    out["sig_by_window_weak"] = g[g.sig & (g.sc <= 0.5)].groupby("w").agg(n=("um14", "size"), um14=("um14", "mean"))
    return out
