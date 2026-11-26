import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    mus = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            rs.append((c.shift(-1)/c - 1).dropna())
        mus[coin] = pd.concat(rs).mean()
    rows = []
    for coin, wins in bars.items():
        mu = mus[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            ts = pd.to_datetime(df["timestamp"])
            d = c.diff().abs()
            er = (c - c.shift(30)).abs() / d.rolling(30).sum()
            r7 = c/c.shift(7)-1; r30 = c/c.shift(30)-1
            vol = (c/c.shift(1)-1).rolling(30).std()
            out = pd.DataFrame({"coin":coin,"win":w,"year":ts.dt.year,"dayid":ts.dt.floor("D"),
                "er":er,"r7":r7,"r30":r30,"vol":vol,"idx":np.arange(len(df))})
            out["sc7"] = r7/(vol*np.sqrt(7)); out["sc30"] = r30/(vol*np.sqrt(30))
            for h in (1,3,7):
                out[f"f{h}"] = c.shift(-h)/c - 1 - h*mu
            rows.append(out)
    A = pd.concat(rows, ignore_index=True)
    A["side"] = np.sign(A["r7"])
    for h in (1,3,7):
        A[f"x{h}"] = A["side"]*A[f"f{h}"]
    R = A[(A.er<=0.3)&(np.sign(A.r7)==np.sign(A.r30))&(A.r7!=0)].copy()
    def tclu(g, col):
        n = len(g); m = g[col].mean()
        sd = (g[col]-m).groupby(g["dayid"]).sum()
        se = np.sqrt((sd**2).sum())/n
        return pd.Series({"n":n,"mean":m,"t_clu":m/se if se>0 else np.nan})
    res = {}
    for h in (1,7):
        g = R[R.idx % h == 0].dropna(subset=[f"x{h}","sc7","sc30"]).copy()
        out = {}
        for var in ("sc7","sc30","er","vol"):
            x = g[var].abs()
            med = x.median()
            top = g.loc[x>med, f"x{h}"]; bot = g.loc[x<=med, f"x{h}"]
            tt = stats.ttest_ind(top, bot, equal_var=False)
            sl = stats.linregress(x, g[f"x{h}"])
            out[var] = {"top_minus_bot":top.mean()-bot.mean(),"welch_t":tt.statistic,
                        "slope_t":sl.slope/sl.stderr,"n":len(g)}
        res[f"grading_h{h}"] = pd.DataFrame(out).T
        g["sc30_q"] = pd.qcut(g["sc30"].abs(), 4, labels=False)
        g["er_q"] = pd.qcut(g["er"], 4, labels=False)
        res[f"by_abs_sc30_q_h{h}"] = g.groupby("sc30_q").apply(lambda z: tclu(z, f"x{h}"))
        res[f"by_er_q_h{h}"] = g.groupby("er_q").apply(lambda z: tclu(z, f"x{h}"))
    g = R[R.idx % 7 == 0].dropna(subset=["x7"])
    res["h7_by_coin"] = g.groupby("coin").apply(lambda z: tclu(z,"x7"))
    res["h7_by_year"] = g.groupby("year").apply(lambda z: tclu(z,"x7"))
    res["h7_by_side"] = g.groupby("side").apply(lambda z: tclu(z,"x7"))
    # ER regime beyond 0.3, aligned, h7 grid
    B = A[(np.sign(A.r7)==np.sign(A.r30))&(A.r7!=0)&(A.idx%7==0)].dropna(subset=["x7","er"]).copy()
    B["er_bin"] = pd.cut(B["er"], [0,0.15,0.3,0.45,0.6,1.0])
    res["aligned_h7_by_er_bin"] = B.groupby("er_bin").apply(lambda z: tclu(z,"x7"))
    return res
