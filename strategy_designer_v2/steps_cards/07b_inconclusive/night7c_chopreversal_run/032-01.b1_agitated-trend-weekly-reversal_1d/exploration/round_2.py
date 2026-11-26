import numpy as np, pandas as pd

def tstat(x):
    x = pd.Series(x).dropna()
    n = len(x)
    if n < 3 or x.std() == 0:
        return np.nan
    return x.mean() / (x.std() / np.sqrt(n))

def explore(data):
    recs = []
    for coin, wins in data["bars"].items():
        allgrid = {h: [] for h in (3, 7, 14)}
        crec = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30).std()
            r7 = c / c.shift(7) - 1
            z = r7 / (sd30 * np.sqrt(7))
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            volr = sd30 / sd30.rolling(60).mean()
            fc = b["forecast"].astype(float)
            fwd = {h: c.shift(-h) / c - 1 for h in (3, 7, 14)}
            day = pd.to_datetime(b["timestamp"]).dt.floor("D")
            yr = day.dt.year
            n = len(b)
            for h in (3, 7, 14):
                for i in range(0, n - h, h):
                    allgrid[h].append(fwd[h].iloc[i])
            # case marking on 7-grid: first bar in cell with forecast deepening >=2 from shallowest since last bet
            shallow = 0.0
            case_flag = np.zeros(n, bool)
            for cell in range(0, n, 7):
                taken = False
                for i in range(cell, min(cell + 7, n)):
                    f = fc.iloc[i] if not np.isnan(fc.iloc[i]) else 0.0
                    shallow = max(shallow, f) if f <= 0 else 0.0
                    if not taken and f <= shallow - 2:
                        case_flag[i] = True
                        taken = True
                        shallow = f
            for i in range(0, n - 7, 7):
                crec.append(dict(coin=coin, win=w, year=yr.iloc[i], day=day.iloc[i], z=z.iloc[i],
                                 er=er.iloc[i], volr=volr.iloc[i], f3=fwd[3].iloc[i], f7=fwd[7].iloc[i],
                                 f14=fwd[14].iloc[i], kind="grid"))
            for i in np.where(case_flag)[0]:
                if i + 7 < n:
                    crec.append(dict(coin=coin, win=w, year=yr.iloc[i], day=day.iloc[i], z=z.iloc[i],
                                     er=er.iloc[i], volr=volr.iloc[i], f3=fwd[3].iloc[i], f7=fwd[7].iloc[i],
                                     f14=fwd[14].iloc[i] if i + 14 < n else np.nan, fc=fc.iloc[i], kind="case"))
        dr = {h: np.nanmean(allgrid[h]) for h in (3, 7, 14)}
        for d in crec:
            for h in (3, 7, 14):
                d["u%d" % h] = d["f%d" % h] - dr[h]
        recs += crec
    df = pd.DataFrame(recs)
    out = {}
    cs = df[df["kind"] == "case"].copy()
    for h in (3, 7, 14):
        cs["s%d" % h] = -cs["u%d" % h]
    cs["absf"] = cs["fc"].abs()
    cs["fbin"] = pd.qcut(cs["absf"], 3, duplicates="drop")
    def csumm(g):
        dd = g.groupby("day")["s7"].sum()
        return pd.Series(dict(n=len(g), days=len(dd), short_u3=g["s3"].mean(), short_u7=g["s7"].mean(),
                              t7_day=tstat(dd), short_u14=g["s14"].mean(), t14=tstat(g["s14"])))
    out["cases_BC_all"] = csumm(cs).to_frame().T
    out["cases_by_absf"] = cs.groupby("fbin").apply(csumm)
    out["cases_by_coin"] = cs.groupby("coin").apply(csumm)
    out["cases_by_year"] = cs.groupby("year").apply(csumm)
    g = df[df["kind"] == "grid"].dropna(subset=["z", "er", "u7"]).copy()
    g["cont"] = np.sign(g["z"]) * g["u7"]
    g["chop"] = g["er"] < 0.3
    g["zabs"] = pd.cut(g["z"].abs(), [0, 0.5, 1.0, 1.5, 10])
    def gsumm(x):
        dd = x.groupby("day")["cont"].sum()
        sl = np.polyfit(x["z"], x["u7"], 1)[0] if len(x) > 5 else np.nan
        return pd.Series(dict(n=len(x), cont7=x["cont"].mean(), t_day=tstat(dd),
                              cont3=(np.sign(x["z"]) * x["u3"]).mean(),
                              cont14=(np.sign(x["z"]) * x["u14"]).mean(), slope_u7_on_z=sl))
    out["chop_by_zabs"] = g[g["chop"]].groupby("zabs").apply(gsumm)
    out["trend_by_zabs"] = g[~g["chop"]].groupby("zabs").apply(gsumm)
    out["chop_all"] = gsumm(g[g["chop"]]).to_frame().T
    out["chop_by_coin_side"] = g[g["chop"]].assign(side=np.where(g["z"] > 0, "up", "down")).groupby(["coin", "side"]).apply(gsumm)
    gv = g.dropna(subset=["volr"])
    out["chop_by_agit"] = gv[gv["chop"]].assign(agit=gv["volr"] >= 1).groupby("agit").apply(gsumm)
    return out
