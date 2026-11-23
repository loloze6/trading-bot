import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    allbars = []
    drift = {}
    for coin, wins in bars.items():
        nonov = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            for i in range(0, n - 3, 3):
                nonov.append(c[i+3]/c[i]-1)
        drift[coin] = (np.mean(nonov), np.std(nonov, ddof=1))
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"]
            r1 = c.pct_change()
            f3 = c.shift(-3)/c - 1
            sd20 = r1.rolling(20).std(); sd60 = r1.rolling(60).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "year": ts.dt.year, "wd": ts.dt.weekday,
                "r1": r1, "f3": f3, "vr": sd20/sd60, "fc": df["forecast"],
                "vol": df["volume"], "volrel": df["volume"]/df["volume"].rolling(20).mean(),
                "r20": c/c.shift(20)-1,
            })
            d["ex"] = d["f3"] - drift[coin][0]
            d["exz"] = d["ex"]/drift[coin][1]
            allbars.append(d)
    A = pd.concat(allbars, ignore_index=True).dropna(subset=["f3", "r1"])
    cases = A[(A.wd == 6) & (A.fc > 0)].copy()

    def reg(df, x="fc", y="ex"):
        df = df.dropna(subset=[x, y])
        if len(df) < 10: return pd.Series({"n": len(df)})
        s = stats.linregress(df[x], df[y])
        return pd.Series({"n": len(df), "mean_ex": df[y].mean(),
                          "t_mean": df[y].mean()/(df[y].std()/np.sqrt(len(df))),
                          "slope": s.slope, "t_slope": s.slope/s.stderr})
    out = {}
    out["all_cases"] = reg(cases).to_frame().T
    out["by_coin"] = cases.groupby("coin").apply(reg)
    out["by_year"] = cases.groupby("year").apply(reg)
    cases["fq"] = pd.qcut(cases.fc, 5, labels=False, duplicates="drop")
    out["by_fc_quintile"] = cases.groupby("fq").agg(n=("ex", "size"), mean_ex=("ex", "mean"), mean_fc=("fc", "mean"), mean_r1=("r1", "mean"), mean_vr=("vr", "mean"))
    # all Sunday falls, regress excess on raw fall and on vr
    sf = A[(A.wd == 6) & (A.r1 < 0)].copy()
    sf["neg_r1"] = -sf.r1
    sf["neg_r1_vr"] = -sf.r1*sf.vr
    out["sunday_falls_on_fall"] = reg(sf, "neg_r1").to_frame().T
    out["sunday_falls_on_fall_x_vr"] = reg(sf, "neg_r1_vr").to_frame().T
    out["sunday_falls_on_vr"] = reg(sf, "vr").to_frame().T
    sf["vrq"] = pd.qcut(sf.vr, 3, labels=["low", "mid", "high"])
    out["sunday_falls_by_vr_tercile"] = sf.groupby("vrq").apply(lambda g: reg(g, "neg_r1"))
    sf["vlq"] = pd.qcut(sf.volrel, 3, labels=["lowvol", "mid", "highvol"])
    out["sunday_falls_by_volume_tercile"] = sf.groupby("vlq").apply(lambda g: reg(g, "neg_r1"))
    sf["trq"] = pd.qcut(sf.r20, 3, labels=["down", "mid", "up"])
    out["sunday_falls_by_r20_tercile"] = sf.groupby("trq").apply(lambda g: reg(g, "neg_r1"))
    # same fall on other weekdays
    allf = A[A.r1 < 0].copy(); allf["neg_r1"] = -allf.r1
    out["falls_by_weekday"] = allf.groupby("wd").apply(lambda g: reg(g, "neg_r1"))
    out["n_coins"] = len(bars)
    out["coins"] = ",".join(sorted(bars.keys()))
    return out
