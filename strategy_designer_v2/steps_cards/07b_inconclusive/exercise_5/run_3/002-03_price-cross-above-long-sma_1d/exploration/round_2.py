def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    dcol = "debug_info.components.above_ma.last_history_value"
    acol = "postRebalance_current_allocation"
    mu = {}
    for c in bars:
        mu[c] = pd.concat([df["close"].pct_change().dropna() for df in bars[c].values()]).mean()
    rows = []; blocks = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; n = len(df)
            d = df[dcol].values if dcol in df else np.full(n, np.nan)
            sma = cl / (1 + d / 100.0)
            above = d > 0
            # days since last cross above
            since = np.full(n, np.nan); cnt = np.nan
            for i in range(n):
                if np.isnan(d[i]): cnt = np.nan; continue
                if above[i]:
                    if i > 0 and not np.isnan(d[i-1]) and d[i-1] <= 0: cnt = 0
                    elif not np.isnan(cnt): cnt += 1
                else: cnt = np.nan
                since[i] = cnt
            vol = pd.Series(cl).pct_change().rolling(60).std().values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            al = df[acol].values
            ex = np.full(n, np.nan)
            for i in range(n - 20):
                ex[i] = cl[i+20]/cl[i]-1 - 20*mu[c]
            for i in range(0, n - 20, 20):
                slope = sma[i]/sma[i-20]-1 if i >= 20 and not np.isnan(sma[i-20]) else np.nan
                rows.append(dict(coin=c, year=yr[i], f=df["forecast"].iloc[i], d=d[i], since=since[i],
                                 slope=slope, vol=vol[i], al=al[i], ex=ex[i], wex=al[i]*ex[i]))
            for s in range(0, n, 20):
                seg = slice(s, min(s+20, n))
                v = al[seg]*ex[seg]; m = ~np.isnan(v)
                if m.sum() == 0: continue
                blocks.append(dict(coin=c, year=yr[s], val=v[m].sum(), nz=(al[seg][m] != 0).any(), meanal=al[seg][m].mean()))
    R = pd.DataFrame(rows); B = pd.DataFrame(blocks)
    def summ(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), median=x.median(), share_pos=(x > 0).mean(),
                              t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan))
    out = {}
    out["blocks_by_coin"] = B.groupby("coin").val.apply(summ).unstack()
    out["blocks_by_year"] = B.groupby("year").val.apply(summ).unstack()
    out["blocks_all"] = summ(B.val).to_frame().T
    A = R[R.f > 0].copy()
    A["since_q"] = pd.cut(A.since, [-1, 20, 60, 150, 10000])
    out["active_ex_by_days_since_cross"] = A.groupby("since_q").ex.apply(summ).unstack()
    A["slope_pos"] = A.slope > 0
    out["active_ex_by_sma_slope_sign"] = A.groupby("slope_pos").ex.apply(summ).unstack()
    R2 = R.dropna(subset=["slope"]).copy()
    R2["sq"] = pd.qcut(R2.slope, 5, labels=False)
    out["all_ex_by_sma_slope_q"] = R2.groupby("sq").apply(lambda g: pd.concat([summ(g.ex), pd.Series(dict(slope=g.slope.mean()))]))
    A["vq"] = pd.qcut(A.vol, 3, labels=False)
    out["active_ex_and_wex_by_vol_tercile"] = A.groupby("vq").apply(lambda g: pd.Series(dict(n=len(g), ex=g.ex.mean(), wex=g.wex.mean(), al=g.al.mean(), t_ex=g.ex.mean()/(g.ex.std()/np.sqrt(len(g))))))
    # book: market part vs timing
    bk = []
    for c in days:
        for w, df in days[c].items():
            dd = df.dropna(subset=["book_return", "coin_return"])
            bk.append(dd[["book_return", "coin_return"]].assign(coin=c))
    K = pd.concat(bk)
    al_mean = pd.concat([pd.Series(bars[c][w][acol].values) for c in bars for w in bars[c]]).mean()
    mud = K.groupby("coin").coin_return.mean().mean()
    out["book"] = pd.Series(dict(book_mean=K.book_return.mean(), mean_alloc=al_mean, market_part=al_mean*mud, coin_mean=mud))
    return out
