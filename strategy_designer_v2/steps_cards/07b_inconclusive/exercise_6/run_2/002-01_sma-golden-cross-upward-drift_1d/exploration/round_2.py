def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for h in [10, 20]:
        for c in bars:
            for w, df in bars[c].items():
                df = df.reset_index(drop=True)
                cl = df["close"].values; fc = df["forecast"].values
                raw = df["debug_info.components.sma_cross.last_history_value"].values
                yr = pd.to_datetime(df["timestamp"]).dt.year.values
                n = len(df)
                # age since raw turned positive, within window (NaN if not seen)
                age = np.full(n, np.nan); last = None
                for i in range(n):
                    if i > 0 and raw[i] > 0 and raw[i-1] <= 0: last = i
                    if raw[i] <= 0: last = None; age[i] = np.nan
                    elif last is not None: age[i] = i - last
                for i in range(0, n - h, h):
                    past = cl[i] / cl[i-h] - 1 if i >= h else np.nan
                    draw = raw[i] - raw[i-h] if i >= h else np.nan
                    rows.append((h, c, w, i, fc[i], raw[i], draw, past, age[i], yr[i], cl[i+h]/cl[i]-1))
    s = pd.DataFrame(rows, columns=["h","coin","win","pos","fc","raw","draw","past","age","yr","ret"])
    s["ex"] = s.ret - s.groupby(["coin","h"]).ret.transform("mean")
    s["ex_win"] = s.ret - s.groupby(["coin","win","h"]).ret.transform("mean")
    s["ex_yr"] = s.ret - s.groupby(["coin","yr","h"]).ret.transform("mean")
    def reg(d, x, y):
        d = d.dropna(subset=[x, y])
        if len(d) < 10 or d[x].std() == 0: return dict(n=len(d), slope=np.nan, t=np.nan)
        r = stats.linregress(d[x], d[y]); return dict(n=len(d), slope=r.slope, t=r.slope/r.stderr)
    out = {}
    res = []
    for h in [10, 20]:
        d = s[s.h == h]
        for x in ["fc", "draw", "past"]:
            for y in ["ex", "ex_yr", "ex_win"]:
                res.append(dict(h=h, x=x, y=y, **reg(d, x, y)))
        dp = d[d.fc > 0]
        for x in ["draw", "past", "age"]:
            res.append(dict(h=h, x=x + "|fc>0", y="ex", **reg(dp, x, "ex")))
    out["regs"] = pd.DataFrame(res)
    d10 = s[(s.h == 10) & (s.fc > 0)].copy()
    d10["agebk"] = pd.cut(d10.age, [-1, 10, 30, 60, 1000])
    out["age_bk_h10"] = d10.groupby("agebk").agg(n=("ex","size"), mean_ex=("ex","mean"), sd=("ex","std"))
    d10["pastbk"] = pd.qcut(d10.past, 4)
    out["past_q_h10_fcpos"] = d10.groupby("pastbk").agg(n=("ex","size"), mean_ex=("ex","mean"), sd=("ex","std"))
    da = s[s.h == 10].copy()
    da["pastbk"] = pd.qcut(da.past, 5)
    out["past_q_h10_all"] = da.groupby("pastbk").agg(n=("ex","size"), mean_ex=("ex","mean"), mean_exyr=("ex_yr","mean"), sd=("ex","std"))
    da["up"] = da.fc > 0
    out["yr_corr_fc_vs_yearmean"] = da.groupby(["coin","yr"]).agg(fcm=("fc","mean"), retm=("ret","mean")).corr().iloc[0,1]
    return out
