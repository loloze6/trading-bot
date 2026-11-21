def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    for H in [5, 10, 26, 40]:
        for coin, ws in bars.items():
            allr = []
            cases = []
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                c = df["close"].values
                f = df["forecast"].fillna(0).values
                reg = df["regime"].astype(str).values
                slope = df.get("debug_info.components.slope.last_history_value")
                slope = slope.values if slope is not None else np.full(len(df), np.nan)
                yr = pd.to_datetime(df["timestamp"]).dt.year.values
                n = len(df)
                for i in range(0, n - H, H):
                    r = c[i + H] / c[i] - 1
                    allr.append(r)
                    # past 26-day coin return
                    past = c[i] / c[i - 26] - 1 if i >= 26 else np.nan
                    cases.append((w, i, r, f[i], reg[i] == "trending", slope[i], yr[i], past))
            drift = np.mean(allr)
            for (w, i, r, fc, tr, sl, y, past) in cases:
                rows.append(dict(H=H, coin=coin, w=w, ex=r - drift, ret=r, fc=fc, tr=tr, sl=sl, yr=y, past=past))
    d = pd.DataFrame(rows)
    def summ(g):
        return pd.Series(dict(n=len(g), mean=g.ex.mean(), t=g.ex.mean() / (g.ex.std(ddof=1) / np.sqrt(len(g))) if len(g) > 2 else np.nan))
    act = d[d.fc > 0]
    out["by_H_active"] = act.groupby("H").apply(summ)
    out["by_H_inactive"] = d[d.fc <= 0].groupby("H").apply(summ)
    a26 = act[act.H == 26].copy()
    out["26_by_coin"] = a26.groupby("coin").apply(summ)
    out["26_by_year"] = a26.groupby("yr").apply(summ)
    a26["fq"] = pd.qcut(a26.fc.rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["26_by_fc_tercile"] = a26.groupby("fq").apply(summ)
    a26["pq"] = pd.qcut(a26.past.rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["26_by_past26_tercile"] = a26.dropna(subset=["past"]).groupby("pq").apply(summ)
    # trending bars incl. forecast 0
    tr26 = d[(d.H == 26) & d.tr]
    out["26_trending_all"] = summ(tr26)
    s = tr26.dropna(subset=["sl"])
    if len(s) > 5:
        lr = stats.linregress(s.sl, s.ex)
        out["26_trending_rawslope_reg"] = pd.Series(dict(n=len(s), slope=lr.slope, t=lr.slope / lr.stderr))
    out["26_median_ex_active"] = a26.ex.median()
    out["26_share_pos_active"] = (a26.ex > 0).mean()
    return out
