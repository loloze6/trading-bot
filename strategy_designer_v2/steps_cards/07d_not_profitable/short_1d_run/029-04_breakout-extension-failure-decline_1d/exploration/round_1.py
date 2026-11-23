import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    H = 5
    col = "debug_info.components.fail_exc.last_history_value"
    rows = []; allrows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c)
            fwd = np.full(n, np.nan); fwd[:n-H] = c[H:]/c[:n-H]-1
            r20 = np.full(n, np.nan); r20[20:] = c[20:]/c[:-20]-1
            r60 = np.full(n, np.nan); r60[60:] = c[60:]/c[:-60]-1
            hi20 = pd.Series(c).rolling(20).max().shift(1).values
            dd = c/pd.Series(c).rolling(60, min_periods=20).max().values-1
            lr = np.log(c[1:]/c[:-1]); vol = np.r_[np.nan, pd.Series(lr).rolling(20).std().values]
            fc = df["forecast"].values
            exc = df[col].values if col in df else np.full(n, np.nan)
            for g in range(0, n-H, H):
                allrows.append((coin, w, fwd[g]))
            # cases: first bar in each grid cell with forecast drop >=2 vs last
            prev = 0.0; seen = set()
            for t in range(n):
                f = fc[t]
                if f <= prev-2 and f < 0:
                    cell = t//H
                    if cell not in seen and not np.isnan(fwd[t]):
                        seen.add(cell)
                        rows.append(dict(coin=coin, w=w, fwd=fwd[t], exc=exc[t], r20=r20[t], r60=r60[t], dd=dd[t], vol=vol[t],
                                         year=pd.Timestamp(df["timestamp"].iloc[t]).year, fwd1=c[t+1]/c[t]-1))
                prev = f if f != 0 else 0.0
    A = pd.DataFrame(allrows, columns=["coin","w","fwd"])
    drift = A.groupby("coin")["fwd"].mean()
    usual = A.groupby("coin")["fwd"].std()
    C = pd.DataFrame(rows)
    C["unus_long"] = C["fwd"] - C["coin"].map(drift)
    C["str_long"] = C["unus_long"]/C["coin"].map(usual)
    def agg(g):
        x = g["unus_long"]; return pd.Series({"n":len(x),"mean_unus_long":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,"mean_total":g["fwd"].mean(),"strength":g["str_long"].mean()})
    out = {}
    out["drift_usual"] = pd.DataFrame({"drift":drift,"usual":usual})
    out["overall"] = agg(C)
    C["excq"] = pd.qcut(C["exc"].rank(method="first"),5,labels=False)
    out["by_exc_q"] = C.groupby("excq").apply(agg).join(C.groupby("excq")["exc"].median())
    C["r60q"] = pd.qcut(C["r60"].rank(method="first"),4,labels=False)
    out["by_r60_q"] = C.dropna(subset=["r60"]).groupby("r60q").apply(agg).join(C.groupby("r60q")["r60"].median())
    C["ddq"] = pd.qcut(C["dd"].rank(method="first"),4,labels=False)
    out["by_dd_q"] = C.groupby("ddq").apply(agg).join(C.groupby("ddq")["dd"].median())
    out["by_coin"] = C.groupby("coin").apply(agg)
    out["by_year"] = C.groupby("year").apply(agg)
    s = C.dropna(subset=["exc"]); lr = stats.linregress(s["exc"], s["fwd"])
    out["slope_exc"] = f"slope {lr.slope:.5f} t {lr.slope/lr.stderr:.2f}"
    s = C.dropna(subset=["r60"]); lr = stats.linregress(s["r60"], s["unus_long"])
    out["slope_r60"] = f"slope {lr.slope:.5f} t {lr.slope/lr.stderr:.2f}"
    out["fwd1_mean"] = f"{C['fwd1'].mean():.5f} t {C['fwd1'].mean()/(C['fwd1'].std()/np.sqrt(len(C))):.2f}"
    # book
    D = pd.concat([d.assign(coin=k, w=w) for k, ws in days.items() for w, d in ws.items()])
    m = D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book_by_w"] = m.groupby(level=0).agg(["mean","count"]).round(5)
    return out
