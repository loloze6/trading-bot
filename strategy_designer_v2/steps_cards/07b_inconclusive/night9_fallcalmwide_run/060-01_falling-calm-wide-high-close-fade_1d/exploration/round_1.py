import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    # coin mean daily return over all visible windows
    rows = []
    allcase = []
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            rets.append(c[1:]/c[:-1]-1)
        mu = np.nanmean(np.concatenate(rets)) if rets else np.nan
        sd = np.nanstd(np.concatenate(rets))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"].values; l = df["low"].values
            r = pd.Series(c).pct_change()
            vol = r.rolling(30).std().values
            rng = (h-l)/c
            width = rng/vol
            loc = np.where(h>l, (c-l)/(h-l), np.nan)
            fc = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for t in range(n-1):
                fw = {}
                for H in (1,2,3,5):
                    fw[H] = c[t+H]/c[t]-1 - H*mu if t+H < n else np.nan
                allcase.append(dict(coin=coin, w=w, year=ts.iloc[t].year, day=ts.iloc[t].normalize(),
                    case=fc[t] < 0, f=abs(fc[t]) if fc[t]<0 else 0, width=width[t], loc=loc[t],
                    u1=-fw[1], u2=-fw[2], u3=-fw[3], u5=-fw[5], sd=sd,
                    ret1d=r.iloc[t]))
    A = pd.DataFrame(allcase)
    C = A[A.case].copy()
    def tday(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 3: return (np.nan, np.nan, len(x))
        m = x[col].mean()
        d = (x[col]-m).groupby(x["day"]).sum()
        se = np.sqrt((d**2).sum())/len(x)
        return (m, m/se if se>0 else np.nan, len(x))
    out = {}
    out["horizons"] = pd.DataFrame({c: tday(C, c) for c in ["u1","u2","u3","u5"]}, index=["mean","t","n"]).T
    out["by_coin"] = pd.DataFrame({k: tday(g,"u1") for k,g in C.groupby("coin")}, index=["mean","t","n"]).T
    out["by_year"] = pd.DataFrame({k: tday(g,"u1") for k,g in C.groupby("year")}, index=["mean","t","n"]).T
    C["fq"] = pd.qcut(C["f"], 3, labels=["low","mid","high"])
    out["by_forecast_tercile"] = pd.DataFrame({k: tday(g,"u1") for k,g in C.groupby("fq")}, index=["mean","t","n"]).T
    C["wq"] = pd.qcut(C["width"], 3, labels=["low","mid","high"], duplicates="drop")
    out["by_width_tercile"] = pd.DataFrame({k: tday(g,"u1") for k,g in C.groupby("wq")}, index=["mean","t","n"]).T
    C["lq"] = pd.cut(C["loc"], [0.74,0.85,0.95,1.01])
    out["by_loc"] = pd.DataFrame({str(k): tday(g,"u1") for k,g in C.groupby("lq")}, index=["mean","t","n"]).T
    C["up"] = C["ret1d"] > 0
    out["by_day_up"] = pd.DataFrame({str(k): tday(g,"u1") for k,g in C.groupby("up")}, index=["mean","t","n"]).T
    # unconditional wide high close days (no profile), on all bars visible
    W = A[(A.width>=2)&(A["loc"]>=0.75)]
    out["wide_high_any_profile"] = pd.DataFrame({c: tday(W, c) for c in ["u1","u2","u3"]}, index=["mean","t","n"]).T
    Wn = W[~W.case]
    out["wide_high_outside_case"] = pd.DataFrame({c: tday(Wn, c) for c in ["u1","u2","u3"]}, index=["mean","t","n"]).T
    sl = stats.linregress(C.dropna(subset=["u1"])["f"], C.dropna(subset=["u1"])["u1"])
    out["slope_u1_on_f"] = f"slope {sl.slope:.5f} t {sl.slope/sl.stderr:.2f}"
    out["n_cases_visible"] = len(C)
    return out
