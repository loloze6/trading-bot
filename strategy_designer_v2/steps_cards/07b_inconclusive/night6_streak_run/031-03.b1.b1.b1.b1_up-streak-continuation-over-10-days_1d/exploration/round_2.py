import numpy as np, pandas as pd
from scipy import stats as sst

def explore(data):
    bars = data["bars"]
    H = [3, 5, 10]
    st = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            rs = np.array(rs)
            st[(coin, h)] = (rs.mean() if len(rs) else np.nan, rs.std(ddof=1) if len(rs) > 1 else np.nan)
    rows, base = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            c = df["close"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            level = 0.0
            bet = np.zeros(n, bool)
            for i in range(n):
                if f[i] <= 0:
                    level = 0.0; continue
                if f[i] - level >= 2:
                    bet[i] = True; level = f[i]
                else:
                    level = min(level, f[i]) if level > 0 else level
            for h in [5, 10]:
                seen = set()
                for i in np.where(bet)[0]:
                    cell = i // h
                    if cell in seen or i + h >= n or i < 30:
                        continue
                    seen.add(cell)
                    m, s = st[(coin, h)]
                    rows.append({"h": h, "coin": coin, "day": ts[i].normalize(), "year": ts[i].year,
                                 "fc": f[i], "ret30": c[i] / c[i - 30] - 1,
                                 "u": c[i + h] / c[i] - 1 - m})
                # baseline: all grid bars with ret30>0, no-signal days included
                for i in range(30, n - h, h):
                    r30 = c[i] / c[i - 30] - 1
                    if r30 > 0:
                        m, s = st[(coin, h)]
                        base.append({"h": h, "coin": coin, "day": ts[i].normalize(), "ret30": r30,
                                     "sig": bool(f[i] > 0), "u": c[i + h] / c[i] - 1 - m})
    cs = pd.DataFrame(rows); bs = pd.DataFrame(base)

    def ct(d):
        d = d.dropna(subset=["u"])
        if len(d) < 5:
            return pd.Series({"n": len(d), "days": np.nan, "mean": np.nan, "t": np.nan})
        m = d["u"].mean()
        g = (d["u"] - m).groupby(d["day"]).sum()
        D = len(g)
        se = np.sqrt((g ** 2).sum() * D / (D - 1)) / len(d)
        return pd.Series({"n": len(d), "days": D, "mean": m, "t": m / se})

    out = {}
    out["cases_by_h"] = cs.groupby("h").apply(ct)
    for h in [5, 10]:
        d = cs[cs.h == h].copy()
        d["fct"] = pd.qcut(d["fc"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
        d["r30t"] = pd.qcut(d["ret30"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
        out[f"h{h}_fc_x_r30"] = d.groupby(["r30t", "fct"]).apply(ct)
        hi, lo = d[d.fct == "hi"]["u"], d[d.fct == "lo"]["u"]
        out[f"h{h}_fc_top_minus_bottom"] = pd.Series({"diff": hi.mean() - lo.mean(), "welch_t": sst.ttest_ind(hi, lo, equal_var=False).statistic})
        hi, lo = d[d.r30t == "hi"]["u"], d[d.r30t == "lo"]["u"]
        out[f"h{h}_r30_top_minus_bottom"] = pd.Series({"diff": hi.mean() - lo.mean(), "welch_t": sst.ttest_ind(hi, lo, equal_var=False).statistic})
        out[f"h{h}_corr_ret30_u"] = float(d[["ret30", "u"]].corr(method="spearman").iloc[0, 1])
        out[f"h{h}_by_year_hi_r30"] = d[d.r30t == "hi"].groupby("year").apply(ct)
    for h in [5, 10]:
        b = bs[bs.h == h].copy()
        b["r30t"] = pd.qcut(b["ret30"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
        out[f"base_h{h}_r30t_by_sig"] = b.groupby(["r30t", "sig"]).apply(ct)
    return out
