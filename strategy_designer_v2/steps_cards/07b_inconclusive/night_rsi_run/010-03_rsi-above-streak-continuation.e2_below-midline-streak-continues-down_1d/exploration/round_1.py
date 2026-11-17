import numpy as np, pandas as pd
from scipy import stats

def wilder_rsi(c, n=14):
    d = c.diff()
    up = d.clip(lower=0); dn = -d.clip(upper=0)
    au = up.ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    ad = dn.ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    return 100 - 100/(1+au/ad)

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            lh = b.get("debug_info.components.rsi_below_age.last_history_value")
            rsi = wilder_rsi(c)
            side = np.sign(rsi - 50)
            run = np.zeros(len(c))
            for i in range(len(c)):
                if np.isnan(rsi.iloc[i]): run[i] = np.nan; continue
                s = side.iloc[i]
                if i > 0 and not np.isnan(run[i-1]) and np.sign(run[i-1]) == s and s != 0:
                    run[i] = run[i-1] + s
                else:
                    run[i] = s
            for h in [1, 3, 7, 14, 28]:
                for i in range(0, len(c) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i,
                        year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                        fc=b["forecast"].iloc[i], lh=(lh.iloc[i] if lh is not None else np.nan),
                        run=run[i], rsi=rsi.iloc[i],
                        ret=c.iloc[i+h]/c.iloc[i]-1))
    df = pd.DataFrame(rows)
    df["ex"] = df["ret"] - df.groupby(["coin", "h"])["ret"].transform("mean")
    d7 = df[df.h == 7]
    neg = d7[d7.fc < 0].copy()
    neg["len"] = -neg["lh"]
    out["lh_vs_myrun_corr"] = float(neg[["len"]].assign(r=-neg["run"]).corr().iloc[0, 1])
    out["lh_describe"] = neg["len"].describe()
    def slope_t(x, y):
        m = ~(np.isnan(x) | np.isnan(y))
        if m.sum() < 5: return (np.nan, np.nan, int(m.sum()))
        r = stats.linregress(x[m], y[m]); return (r.slope, r.slope/r.stderr, int(m.sum()))
    res = []
    for h in [1, 3, 7, 14, 28]:
        dh = df[(df.h == h) & (df.fc < 0)]
        s, t, n = slope_t(-dh["lh"].values, dh["ex"].values)
        dd = df[df.h == h]
        below = dd[dd.run < 0]["ex"]; above = dd[dd.run > 0]["ex"]
        tt = stats.ttest_ind(below, above, equal_var=False)
        res.append(dict(h=h, slope=s, t_slope=t, n=n, mean_ex_below=below.mean(), mean_ex_above=above.mean(),
                        t_below_minus_above=tt.statistic, n_below=len(below), n_above=len(above)))
    out["by_horizon"] = pd.DataFrame(res)
    d7b = d7[d7.run < 0].copy()
    d7b["bucket"] = pd.cut(-d7b["run"], [0, 3, 7, 14, 28, 1000])
    out["h7_below_by_runlen"] = d7b.groupby("bucket")["ex"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    d7a = d7[d7.run > 0].copy()
    d7a["bucket"] = pd.cut(d7a["run"], [0, 3, 7, 14, 28, 1000])
    out["h7_above_by_runlen"] = d7a.groupby("bucket")["ex"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    pc = []
    for coin, g in neg.groupby("coin"):
        s, t, n = slope_t(g["len"].values, g["ex"].values); pc.append(dict(coin=coin, slope=s, t=t, n=n, mean_ex=g.ex.mean()))
    out["h7_neg_by_coin"] = pd.DataFrame(pc)
    py = []
    for y, g in neg.groupby("year"):
        s, t, n = slope_t(g["len"].values, g["ex"].values); py.append(dict(year=y, slope=s, t=t, n=n, mean_ex=g.ex.mean()))
    out["h7_neg_by_year"] = pd.DataFrame(py)
    # RSI level among below-50
    neg2 = d7[d7.rsi < 50].copy()
    neg2["rb"] = pd.cut(neg2["rsi"], [0, 30, 40, 45, 50])
    out["h7_below_by_rsi_level"] = neg2.groupby("rb")["ex"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    return out
