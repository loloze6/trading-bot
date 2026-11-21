import numpy as np, pandas as pd

def explore(data):
    out = {}
    H = 20
    rows = []
    daysrows = []
    for coin, wins in data["bars"].items():
        g_all = []
        dr_all = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                g_all.append(c[i + H] / c[i] - 1)
            dr_all.extend(list(pd.Series(c).pct_change().dropna().values))
        drift = np.mean(g_all); ddrift = np.mean(dr_all)
        for w, b in wins.items():
            c = b["close"].astype(float).values
            n = len(c)
            fc = b["forecast"].astype(float).fillna(0).values
            pos = b["postRebalance_current_allocation"].astype(float).fillna(0).values
            s = pd.Series(c)
            r1 = s.pct_change().shift(-1).values
            vol = s.pct_change().rolling(20, min_periods=10).std().values
            r20p = s.pct_change(20).values
            # days since forecast turned positive (age of breakout)
            age = np.full(n, np.nan); a = 0
            for i in range(n):
                a = a + 1 if fc[i] > 0 else 0
                age[i] = a
            # days since last positive forecast
            since = np.full(n, np.nan); last = -10**6
            for i in range(n):
                if fc[i] > 0: last = i
                since[i] = i - last if last > -10**6 else np.nan
            for i in range(n):
                f20 = c[i + H] / c[i] - 1 - drift if i + H < n else np.nan
                rows.append(dict(coin=coin, win=w, i=i, fc=fc[i], pos=pos[i], r1=r1[i],
                                 r1x=r1[i] - ddrift if not np.isnan(r1[i]) else np.nan,
                                 f20=f20, grid=(i % H == 0), age=age[i], since=since[i],
                                 vol=vol[i], r20p=r20p[i]))
    A = pd.DataFrame(rows)
    out["share_bars_fc_pos"] = float((A.fc > 0).mean())
    out["share_bars_in_pos"] = float((A.pos.abs() > 1e-6).mean())
    # daily forward drift-adjusted return when in position vs not
    A["inpos"] = A.pos.abs() > 1e-6
    out["r1x_by_inpos"] = A.groupby("inpos")["r1x"].agg(["count", "mean"])
    # in position: by age of breakout (fc>0) and by days since signal (held after fc dropped)
    P = A[A.inpos].copy()
    P["state"] = np.where(P.fc > 0, "fc_pos", "held_fc0")
    out["r1x_in_pos_by_state"] = P.groupby("state")["r1x"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    Fp = A[A.fc > 0].copy()
    Fp["agebin"] = pd.cut(Fp.age, [0, 3, 10, 25, 60, 500])
    out["r1x_fcpos_by_age"] = Fp.groupby("agebin")["r1x"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    # 20d forward (grid) after positive forecast by age
    Gp = Fp[Fp.grid].dropna(subset=["f20"])
    out["f20_grid_fcpos_by_age"] = Gp.groupby("agebin")["f20"].agg(["count", "mean"])
    # 20d forward (all bars, overlapping, descriptive) by forecast tercile when fc>0
    Fp2 = Fp.dropna(subset=["f20"]).copy()
    Fp2["fq"] = pd.qcut(Fp2.fc.rank(method="first"), 3, labels=["low", "mid", "high"])
    out["f20_fcpos_by_fc_tercile_overlap"] = Fp2.groupby("fq")["f20"].agg(["count", "mean", "median"])
    # 20d forward vs past 20d return, non-overlapping grid, all bars
    G = A[A.grid].dropna(subset=["f20", "r20p"]).copy()
    G["rq"] = pd.qcut(G.r20p, 5)
    out["f20_grid_by_past20"] = G.groupby("rq")["f20"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    # position size when in, by vol
    out["pos_when_in_desc"] = P.pos.describe()
    # book losses: in position days, r1 by past 20d return quintile among in-position
    P2 = P.dropna(subset=["r20p", "r1x"]).copy()
    P2["rq"] = pd.qcut(P2.r20p, 4)
    out["r1x_inpos_by_past20"] = P2.groupby("rq")["r1x"].agg(["count", "mean"])
    # per coin share in position & mean r1x in position
    out["by_coin"] = A.groupby("coin").agg(inpos=("inpos", "mean"), fcpos=("fc", lambda x: (x > 0).mean()))
    out["by_coin_r1x_inpos"] = P.groupby("coin")["r1x"].mean()
    return out
