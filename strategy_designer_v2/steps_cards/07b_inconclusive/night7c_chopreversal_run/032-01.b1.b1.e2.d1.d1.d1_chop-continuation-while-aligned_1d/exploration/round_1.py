import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    allret = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            rs.append((c.shift(-1)/c - 1).dropna())
        allret[coin] = pd.concat(rs).mean()
    for coin, wins in bars.items():
        mu = allret[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            ts = pd.to_datetime(df["timestamp"])
            d = c.diff().abs()
            er = (c - c.shift(30)).abs() / d.rolling(30).sum()
            r7 = c/c.shift(7)-1; r30 = c/c.shift(30)-1
            vol = (c/c.shift(1)-1).rolling(30).std()
            sc = r7/(vol*np.sqrt(7))
            out = pd.DataFrame({"coin":coin,"win":w,"year":ts.dt.year,"dayid":ts.dt.floor("D"),
                "pos":df["postRebalance_current_allocation"].astype(float),
                "reg":df["regime"],"fc":df["forecast"].astype(float),
                "er":er,"r7":r7,"r30":r30,"sc":sc,"vol":vol,"idx":np.arange(len(df))})
            for h in (1,3,7):
                out[f"f{h}"] = c.shift(-h)/c - 1 - h*mu
            rows.append(out)
    A = pd.concat(rows, ignore_index=True)
    A["side"] = np.sign(A["r7"])
    for h in (1,3,7):
        A[f"x{h}"] = A["side"]*A[f"f{h}"]
    C = A[(A.reg=="trending") & (A.pos!=0)].dropna(subset=["x1"])
    def tclu(g, col="x1"):
        s = g.groupby("dayid")[col].sum(); n = g.groupby("dayid")[col].size()
        m = s.sum()/n.sum()
        dev = g[col]-m
        sd = dev.groupby(g["dayid"]).sum()
        se = np.sqrt((sd**2).sum())/n.sum()
        return pd.Series({"n":len(g),"mean":m,"t_clu":m/se if se>0 else np.nan})
    res = {}
    res["all"] = tclu(C)
    res["by_coin"] = C.groupby("coin").apply(tclu)
    res["by_win"] = C.groupby("win").apply(tclu)
    res["by_year"] = C.groupby("year").apply(tclu)
    res["by_side"] = C.groupby("side").apply(tclu)
    C = C.copy()
    C["abs_sc_q"] = pd.qcut(C["sc"].abs(), 5, labels=False)
    C["abs_fc_q"] = pd.qcut(C["fc"].abs().rank(method="first"), 5, labels=False)
    C["er_q"] = pd.qcut(C["er"], 4, labels=False)
    C["vol_q"] = pd.qcut(C["vol"], 4, labels=False)
    res["by_abs_scaled7_q"] = C.groupby("abs_sc_q").apply(tclu)
    res["by_abs_fc_q"] = C.groupby("abs_fc_q").apply(tclu)
    res["by_er_q"] = C.groupby("er_q").apply(tclu)
    res["by_vol_q"] = C.groupby("vol_q").apply(tclu)
    # horizons on non-overlapping grid among aligned-chop bars (recomputed regime)
    R = A[(A.er<=0.3)&(np.sign(A.r7)==np.sign(A.r30))&(A.r7!=0)]
    hz = {}
    for h in (1,3,7):
        g = R[R.idx % h == 0].dropna(subset=[f"x{h}"])
        hz[h] = tclu(g, f"x{h}")
    res["horizons_regime_grid"] = pd.DataFrame(hz).T
    # outside regime: same scaled7 continuation, non-aligned or non-chop
    O = A[~A.index.isin(R.index)].dropna(subset=["x1","sc"])
    res["outside_regime_x1"] = tclu(O)
    # slope of x1 on scaled7 sign*value inside regime
    g = R.dropna(subset=["x1","sc"])
    sl = stats.linregress(g["sc"].abs(), g["x1"])
    res["slope_x1_on_abs_sc"] = pd.Series({"slope":sl.slope,"t":sl.slope/sl.stderr,"n":len(g)})
    return res
