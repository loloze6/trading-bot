import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    col = "debug_info.components.rsi_above_age.last_history_value"
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            d = np.diff(c, prepend=np.nan)
            up = pd.Series(np.where(d > 0, d, 0.0)); dn = pd.Series(np.where(d < 0, -d, 0.0))
            rs = up.ewm(alpha=1/14, adjust=False).mean() / dn.ewm(alpha=1/14, adjust=False).mean()
            rsi = 100 - 100/(1+rs)
            # own run length
            age = np.zeros(len(df)); a = 0
            for i in range(len(df)):
                if i < 15: age[i] = np.nan; continue
                if rsi[i] > 50: a = a + 1 if a > 0 else 1
                else: a = a - 1 if a < 0 else -1
                age[i] = a
            lhv = df[col].values if col in df else np.full(len(df), np.nan)
            n = len(df)
            for h in (7, 14, 28, 56):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year, h=h,
                                     lhv=lhv[i], age=age[i], fc=df["forecast"].iloc[i],
                                     r=c[i+h]/c[i]-1))
    g = pd.DataFrame(rows)
    g["ex"] = g["r"] - g.groupby(["coin","h"])["r"].transform("mean")
    out["lhv_describe"] = g[g.h==14]["lhv"].describe()
    out["corr_lhv_age"] = float(g[g.h==14][["lhv","age"]].corr().iloc[0,1])
    def slope(s, x="lhv"):
        s = s.dropna(subset=[x,"ex"])
        if len(s) < 8: return (np.nan, np.nan, len(s))
        r = stats.linregress(s[x], s["ex"])
        return (r.slope, r.slope/r.stderr, len(s))
    res = []
    for h in (7,14,28,56):
        s = g[g.h==h]
        res.append(dict(h=h, part="fc<0 lhv", **dict(zip(["slope","t","n"], slope(s[s.fc<0])))))
        res.append(dict(h=h, part="age>0", **dict(zip(["slope","t","n"], slope(s[s.age>0],"age")))))
        res.append(dict(h=h, part="age<0", **dict(zip(["slope","t","n"], slope(s[s.age<0],"age")))))
        res.append(dict(h=h, part="all age", **dict(zip(["slope","t","n"], slope(s,"age")))))
        a = s[s.age>0].ex.dropna(); b = s[s.age<0].ex.dropna()
        tt = stats.ttest_ind(a, b, equal_var=False)
        res.append(dict(h=h, part="above minus below mean", slope=a.mean()-b.mean(), t=tt.statistic, n=len(a)+len(b)))
    out["slopes"] = pd.DataFrame(res)
    s = g[(g.h==14)&(g.fc<0)]
    out["by_coin"] = pd.DataFrame({c: slope(x) for c, x in s.groupby("coin")}, index=["slope","t","n"]).T
    out["by_year"] = pd.DataFrame({y: slope(x) for y, x in s.groupby("year")}, index=["slope","t","n"]).T
    s2 = g[(g.h==14)].dropna(subset=["age"])
    s2["bin"] = pd.cut(s2.age, [-100,-30,-10,-1,0,5,15,30,100])
    out["ex_by_agebin_h14"] = s2.groupby("bin")["ex"].agg(["mean","count",lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    return out
