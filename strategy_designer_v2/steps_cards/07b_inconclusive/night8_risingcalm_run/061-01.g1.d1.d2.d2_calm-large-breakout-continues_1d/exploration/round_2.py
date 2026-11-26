import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in (3,5,10)}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            r = pd.Series(c).pct_change()
            sd30 = r.rolling(30).std()
            z = r / sd30
            hi20 = pd.Series(c).rolling(20).max()
            lo20 = pd.Series(c).rolling(20).min()
            tr60 = pd.Series(c).pct_change(60) * 100
            sdmed = sd30.expanding(60).median()
            n = len(c)
            for h in allr:
                for i in range(0, n - h, h):
                    allr[h].append(c[i+h]/c[i]-1)
            for i in range(n):
                rows.append(dict(coin=coin, win=w, grid5=i//5, z=z.iloc[i],
                                 dist=c[i]/hi20.iloc[i]-1 if hi20.iloc[i]==hi20.iloc[i] else np.nan,
                                 atlow=(c[i] <= lo20.iloc[i]+1e-12) if lo20.iloc[i]==lo20.iloc[i] else False,
                                 tr60=tr60.iloc[i], calmw=sd30.iloc[i] <= sdmed.iloc[i] if sdmed.iloc[i]==sdmed.iloc[i] else np.nan,
                                 regime=df["regime"].iloc[i],
                                 year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                 f3=c[i+3]/c[i]-1 if i+3<n else np.nan,
                                 f5=c[i+5]/c[i]-1 if i+5<n else np.nan,
                                 f10=c[i+10]/c[i]-1 if i+10<n else np.nan))
        drift[coin] = {h: np.mean(v) for h, v in allr.items()}
    d = pd.DataFrame(rows)
    for h in (3,5,10):
        d[f"x{h}"] = d[f"f{h}"] - d["coin"].map(lambda k: drift[k][h])
    d["inprof"] = d["regime"] != "chop"
    d["athigh"] = d["dist"] >= -1e-12
    d["trend"] = np.where(d.tr60 > 10, "rising", np.where(d.tr60 < -10, "falling", np.where(d.tr60.isna(), "na", "choppy")))
    def one(s, asc=False):
        return s.sort_values("z", ascending=asc).groupby(["coin","win","grid5"]).head(1)
    def summ(s, h=5, sign=1):
        s = s.dropna(subset=[f"x{h}", "z"])
        if len(s) < 8: return pd.Series({"n": len(s)})
        y = s[f"x{h}"]*sign; x = s["z"].abs()
        sl = stats.linregress(x, y)
        return pd.Series({"n": len(s), "mean_x%": y.mean()*100, "t_mean": y.mean()/(y.std()/np.sqrt(len(s))),
                          "slope%": sl.slope*100, "t_slope": sl.slope/sl.stderr})
    out = {}
    up = d[d.z > 0]
    tab = {}
    for prof in ["inprof", "chop"]:
        base = up[up.inprof] if prof == "inprof" else up[~up.inprof]
        for tr in ["choppy", "rising", "falling"]:
            for cw in [True, False]:
                s = one(base[base.athigh & (base.trend == tr) & (base.calmw == cw)])
                for h in (3,5,10):
                    tab[(prof, tr, "calmw" if cw else "agitw", h)] = summ(s, h)
    out["high_up_by_profile"] = pd.DataFrame(tab).T
    # all up days (any close) by proxied calm, graded
    tab2 = {}
    for cw in [True, False]:
        s = one(up[(up.calmw == cw)])
        for h in (3,5,10):
            tab2[("allup", "calmw" if cw else "agitw", h)] = summ(s, h)
        s = one(up[(up.calmw == cw) & up.athigh])
        for h in (3,5,10):
            tab2[("highup", "calmw" if cw else "agitw", h)] = summ(s, h)
        dn = d[(d.z < 0) & (d.calmw == cw) & d.atlow]
        s = one(dn, asc=True)
        for h in (3,5,10):
            tab2[("lowdown_short", "calmw" if cw else "agitw", h)] = summ(s, h, sign=-1)
    out["by_proxy_calm"] = pd.DataFrame(tab2).T
    ch = one(up[~up.inprof & up.athigh])
    out["chop_high_by_year"] = ch.groupby("year").apply(summ)
    out["chop_high_by_coin"] = ch.groupby("coin").apply(summ)
    return out
