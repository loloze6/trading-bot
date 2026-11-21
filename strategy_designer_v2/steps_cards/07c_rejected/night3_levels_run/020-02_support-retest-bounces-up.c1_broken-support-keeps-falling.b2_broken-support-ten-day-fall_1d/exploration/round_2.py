import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df["forecast"].values
            n = len(df)
            r60 = np.full(n, np.nan); r60[60:] = c[60:] / c[:-60] - 1
            r10b = np.full(n, np.nan); r10b[10:] = c[10:] / c[:-10] - 1
            ma = pd.Series(c).rolling(50, min_periods=50).mean().values
            pos = df["postRebalance_current_allocation"].values
            for i in range(0, n - 10, 10):
                rows.append(dict(coin=coin, w=w, f=f[i], ret=c[i+10]/c[i]-1, r60=r60[i],
                                 r10b=r10b[i], abovema=(c[i] > ma[i]) if not np.isnan(ma[i]) else np.nan,
                                 pos=pos[i]))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby("coin")["ret"].transform("mean")
    R["ex"] = R["ret"] - R["drift"]
    out = {}
    A = R[R.f < 0].copy()
    m = -(A.f / 10) * A.ex
    out["plan_measure_recomputed"] = pd.Series({"mean": m.mean(), "t": m.mean()/(m.std()/np.sqrt(len(m))), "n": len(m)})
    s = (A.f / 10) * A.ex  # short's gain beyond drift, sized
    out["short_gain_sized"] = pd.Series({"mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))), "n": len(s)})
    out["mean_position_active"] = pd.Series({"mean_pos": A.pos.mean(), "share_pos_neg": (A.pos < 0).mean()})
    I = R[R.f >= 0]
    out["active_minus_inactive_ex"] = pd.Series({"diff_pct": 100*(A.ex.mean()-I.ex.mean()),
        "welch_t": stats.ttest_ind(A.ex, I.ex, equal_var=False).statistic, "nA": len(A), "nI": len(I)})

    def summ(g):
        return pd.Series({"n": len(g), "mean_ex_pct": 100*g.ex.mean(),
                          "t": g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "mean_ret_pct": 100*g.ret.mean()})
    A2 = A.dropna(subset=["r60"]).copy()
    A2["trend60"] = np.where(A2.r60 < 0, "60d_down", "60d_up")
    A2["fq"] = pd.qcut(A2.f.abs().rank(method="first"), 2, labels=["small", "large"])
    out["active_by_trend60_fsize"] = A2.groupby(["trend60", "fq"]).apply(summ)
    A3 = A.dropna(subset=["abovema"]).copy()
    A3["ma"] = np.where(A3.abovema == True, "above50ma", "below50ma")
    A3["fq"] = pd.qcut(A3.f.abs().rank(method="first"), 2, labels=["small", "large"])
    out["active_by_ma50_fsize"] = A3.groupby(["ma", "fq"]).apply(summ)
    I2 = I.dropna(subset=["r60"]).copy()
    I2["trend60"] = np.where(I2.r60 < 0, "60d_down", "60d_up")
    out["inactive_by_trend60"] = I2.groupby("trend60").apply(summ)
    # short-side regression of ex on |f| within downtrend
    d = A2[A2.trend60 == "60d_down"]
    sl = stats.linregress(d.f.abs(), d.ex)
    out["downtrend_slope_ex_on_absf"] = pd.Series({"slope_pct_per_unit": 100*sl.slope, "t": sl.slope/sl.stderr, "n": len(d)})
    u = A2[A2.trend60 == "60d_up"]
    sl = stats.linregress(u.f.abs(), u.ex)
    out["uptrend_slope_ex_on_absf"] = pd.Series({"slope_pct_per_unit": 100*sl.slope, "t": sl.slope/sl.stderr, "n": len(u)})
    return out
