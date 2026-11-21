import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    coinstats = {}
    for coin, wins in data["bars"].items():
        st = {}
        for H in (5, 10, 26, 52):
            g = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c) - H, H):
                    g.append(c[i + H] / c[i] - 1)
            st[H] = (np.mean(g) if g else np.nan, np.std(g) if g else np.nan)
        coinstats[coin] = st
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            ten = (hi.rolling(9).max() + lo.rolling(9).min()) / 2
            kij = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            sa = ((ten + kij) / 2).shift(26)
            sb = ((hi.rolling(52).max() + lo.rolling(52).min()) / 2).shift(26)
            top = np.maximum(sa, sb); bot = np.minimum(sa, sb)
            mid = (sa + sb) / 2
            slope = mid / mid.shift(26) - 1
            thick = (top - bot) / c
            dist = c / top - 1
            ma = c.rolling(50).mean()
            f = b["forecast"].fillna(0).values
            cv = c.values; n = len(cv)
            for i in range(0, n - 26, 26):
                r = {"coin": coin, "fc": f[i], "on": f[i] > 0,
                     "above_rise": (dist.iloc[i] > 0) and (slope.iloc[i] > 0),
                     "slope": slope.iloc[i], "thick": thick.iloc[i], "dist": dist.iloc[i],
                     "above_ma": cv[i] > ma.iloc[i] if not np.isnan(ma.iloc[i]) else np.nan}
                for H in (5, 10, 26, 52):
                    r["ex%d" % H] = (cv[i + H] / cv[i] - 1 - coinstats[coin][H][0]) / coinstats[coin][H][1] if i + H < n else np.nan
                r["raw26"] = cv[i + 26] / cv[i] - 1 - coinstats[coin][26][0]
                rows.append(r)
    d = pd.DataFrame(rows)
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    hz = []
    for H in (5, 10, 26, 52):
        for lab, sub in (("on", d[d.on]), ("off", d[~d.on]), ("above_rise_recomp", d[d.above_rise.astype(bool)])):
            s = tt(sub["ex%d" % H]); s["H"] = H; s["set"] = lab; hz.append(s)
    out["strength_by_horizon_and_set"] = pd.DataFrame(hz)
    out["on_minus_off_26_welch"] = stats.ttest_ind(d[d.on]["ex26"].dropna(), d[~d.on]["ex26"].dropna(), equal_var=False).statistic
    on = d[d.on].copy()
    on["thq"] = pd.qcut(on["thick"].rank(method="first"), 4, labels=False)
    out["on_by_thickness_q"] = on.groupby("thq").apply(lambda g: pd.concat([tt(g["ex26"]), pd.Series({"thick": g["thick"].mean(), "raw26": g["raw26"].mean(), "med_raw": g["raw26"].median()})]))
    on["dq"] = pd.qcut(on["dist"].rank(method="first"), 4, labels=False)
    out["on_by_distance_q"] = on.groupby("dq").apply(lambda g: pd.concat([tt(g["ex26"]), pd.Series({"dist": g["dist"].mean(), "raw26": g["raw26"].mean()})]))
    on["sq"] = pd.qcut(on["slope"].rank(method="first"), 4, labels=False)
    out["on_by_slope_q"] = on.groupby("sq").apply(lambda g: pd.concat([tt(g["ex26"]), pd.Series({"slope": g["slope"].mean()})]))
    out["spearman_on"] = pd.Series({k: stats.spearmanr(on[k], on["ex26"], nan_policy="omit").correlation for k in ["slope", "thick", "dist", "fc"]})
    out["above_ma_all_bars"] = d.dropna(subset=["above_ma"]).groupby("above_ma").apply(lambda g: tt(g["ex26"]))
    return out
