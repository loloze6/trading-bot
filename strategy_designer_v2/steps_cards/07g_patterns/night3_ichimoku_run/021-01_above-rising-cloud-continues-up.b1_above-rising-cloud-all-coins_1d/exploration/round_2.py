def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; crosses = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            s = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            c = s.values; n = len(c)
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            ret26 = (s / s.shift(26) - 1).values
            ret13 = (s / s.shift(13) - 1).values
            vol = s.pct_change().rolling(26).std().values
            mid9 = (hi.rolling(9).max() + lo.rolling(9).min()) / 2
            mid26 = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            mid52 = (hi.rolling(52).max() + lo.rolling(52).min()) / 2
            A = ((mid9 + mid26) / 2).shift(26); B = mid52.shift(26)
            top = np.maximum(A, B).values; bot = np.minimum(A, B).values
            thick = (top - bot) / c
            fc = b["forecast"].astype(float).values
            reg = (b["regime"] == "trending").astype(int).values
            for h in [10, 26]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, yr=yr[i], h=h, fwd=c[i+h]/c[i]-1, ret26=ret26[i],
                                     ret13=ret13[i], rv=ret26[i]/(vol[i]*np.sqrt(26)) if vol[i] > 0 else np.nan,
                                     fc=fc[i], reg=reg[i], above=float(c[i] > top[i]) if not np.isnan(top[i]) else np.nan))
            # crosses through cloud: close above top today, not yesterday (up) / below bot today, not yesterday (down)
            for i in range(1, n - 10):
                if np.isnan(top[i]) or np.isnan(top[i-1]): continue
                up = c[i] > top[i] and c[i-1] <= top[i-1]
                dn = c[i] < bot[i] and c[i-1] >= bot[i-1]
                if up or dn:
                    d = 1 if up else -1
                    crosses.append(dict(coin=coin, win=w, d=d, thick=thick[i], f10=d*(c[i+10]/c[i]-1),
                                        a10=abs(c[i+10]/c[i]-1)))
    df = pd.DataFrame(rows)
    df["mu"] = df.groupby(["coin","h"])["fwd"].transform("mean")
    df["sd"] = df.groupby(["coin","h"])["fwd"].transform("std")
    df["ex"] = df.fwd - df.mu; df["z"] = df.ex / df.sd
    res = []
    for h in [10, 26]:
        d = df[(df.h == h)].dropna(subset=["ret26","z"])
        for f in ["ret26","ret13","rv","fc"]:
            dd = d.dropna(subset=[f])
            rho, p = stats.spearmanr(dd[f], dd.z)
            res.append(dict(h=h, f=f, n=len(dd), rho=round(rho,3), p=round(p,4)))
        # ret26 within regime groups
        for rg in [0, 1]:
            dd = d[d.reg == rg]
            rho, p = stats.spearmanr(dd.ret26, dd.z)
            res.append(dict(h=h, f=f"ret26|reg={rg}", n=len(dd), rho=round(rho,3), p=round(p,4)))
        for ab in [0.0, 1.0]:
            dd = d[d.above == ab]
            if len(dd) > 20:
                rho, p = stats.spearmanr(dd.ret26, dd.z)
                res.append(dict(h=h, f=f"ret26|above={ab}", n=len(dd), rho=round(rho,3), p=round(p,4)))
        # regression z ~ rank ret26 + reg
        dd = d.copy()
        dd["rk"] = dd.groupby("coin").ret26.rank(pct=True) - 0.5
        X = np.column_stack([np.ones(len(dd)), dd.rk, dd.reg])
        beta, *_ = np.linalg.lstsq(X, dd.z.values, rcond=None)
        resid = dd.z.values - X @ beta
        se = np.sqrt(np.diag(np.linalg.inv(X.T @ X)) * resid.var(ddof=3))
        res.append(dict(h=h, f="OLS rk_ret26 | reg", n=len(dd), rho=round(beta[1]/se[1],2), p=round(beta[2]/se[2],2)))
    out["ret26_tests (OLS row: rho=t_rk, p=t_reg)"] = pd.DataFrame(res)
    d = df[df.h == 26].dropna(subset=["ret26","z"]).copy()
    d["q"] = d.groupby("coin").ret26.transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False) if len(x) >= 10 else np.nan)
    d = d.dropna(subset=["q"])
    d["sgn"] = np.where(d.ret26 > 0, 1, -1)
    out["h26_by_q"] = d.groupby("q").agg(n=("z","size"), ex=("ex","mean"), z=("z","mean"), fwd=("fwd","mean"))
    out["h26_by_year_spearman"] = d.groupby("yr").apply(lambda g: pd.Series(dict(n=len(g), rho=stats.spearmanr(g.ret26, g.z)[0], ex_q4_minus_q0=g[g.q==4].ex.mean()-g[g.q==0].ex.mean())))
    pc = d.groupby("coin").apply(lambda g: stats.spearmanr(g.ret26, g.z)[0] if len(g) >= 10 else np.nan).dropna()
    out["h26_per_coin"] = pd.Series(dict(coins=len(pc), positive=(pc > 0).sum(), median_rho=pc.median()))
    # signed strength: direction of ret26
    d["sz"] = d.sgn * d.z; d["sex"] = d.sgn * d.ex
    out["h26_signed_by_dir"] = d.groupby("sgn").agg(n=("sz","size"), strength=("sz","mean"), unusual=("sex","mean"),
                                                    t=("sz", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    cr = pd.DataFrame(crosses).dropna()
    cr["tq"] = pd.qcut(cr.thick.rank(method="first"), 3, labels=["thin","mid","thick"])
    out["cross_by_thickness_10d"] = cr.groupby(["d","tq"], observed=True).agg(n=("f10","size"), dir_ret=("f10","mean"), abs_ret=("a10","mean"))
    out["cross_spearman"] = pd.Series(dict(n=len(cr), rho_thick_abs=stats.spearmanr(cr.thick, cr.a10)[0],
                                           p_abs=stats.spearmanr(cr.thick, cr.a10)[1],
                                           rho_thick_dir=stats.spearmanr(cr.thick, cr.f10)[0],
                                           p_dir=stats.spearmanr(cr.thick, cr.f10)[1]))
    return out
