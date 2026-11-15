import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []; brow = []
    for coin, wins in bars.items():
        mu = pd.concat([pd.Series(df["close"].values).pct_change().dropna() for df in wins.values()]).mean()
        dd = pd.concat([d["coin_return"].dropna() for d in days[coin].values()]).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c)
            a = df["postRebalance_current_allocation"].fillna(0).values
            f = df["forecast"].values
            raw = df["debug_info.components.above_ma.last_history_value"].values
            s = pd.Series(c)
            vol60 = s.pct_change().rolling(60).std().values
            ma50 = s.rolling(50).mean()
            slope50 = (ma50 / ma50.shift(20) - 1).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            h = 20
            for i in range(0, n - h, h):
                ex = c[i+h]/c[i]-1 - h*mu
                rows.append(dict(coin=coin, w=w, year=yr[i], f=f[i], a=a[i], raw=raw[i], vol=vol60[i],
                                 slope=slope50[i], ex=ex, aex=a[i]*ex))
            d = days[coin][w].dropna(subset=["book_return"])
            dpos = df.set_index(pd.to_datetime(df["timestamp"]).dt.floor("D"))["postRebalance_current_allocation"]
            dpos = dpos.groupby(level=0).last().shift(1)
            dk = pd.to_datetime(d["day"]).dt.floor("D")
            pos = dpos.reindex(dk.values).values
            for br, cr, p in zip(d["book_return"].values, d["coin_return"].values, pos):
                brow.append(dict(coin=coin, w=w, br=br, cr=cr, p=p, mk=(p if p==p else 0)*dd))
    R = pd.DataFrame(rows); B = pd.DataFrame(brow)
    def summ(g, col="ex"):
        x = g[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), median=x.median(),
                              t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, hit=(x>0).mean()))
    out = {}
    out["book_decomp"] = pd.Series(dict(book_mean=B.br.mean(), market_part=B.mk.mean(),
                                        timing=B.br.mean()-B.mk.mean(), hold_mean=B.cr.mean(), n=len(B)))
    pos = R[R.f > 0].copy()
    out["aex_by_coin"] = pos.groupby("coin").apply(lambda g: summ(g, "aex"))
    out["aex_by_year"] = pos.groupby("year").apply(lambda g: summ(g, "aex"))
    pos["volq"] = pd.qcut(pos.vol, 3, labels=["low","mid","high"])
    out["alloc_by_volq"] = pos.groupby("volq").a.mean()
    out["aex_by_volq"] = pos.groupby("volq").apply(lambda g: summ(g, "aex"))
    R["slq"] = pd.qcut(R.slope, 3, labels=["down","flat","up"])
    R["above"] = np.where(R.raw > 0, "above", "below")
    out["ex_by_slope_above"] = R.groupby(["slq","above"]).apply(summ)
    R["volq"] = pd.qcut(R.vol, 3, labels=["low","mid","high"])
    out["ex_by_vol_above"] = R.groupby(["volq","above"]).apply(summ)
    ab = R[R.above=="above"]; be = R[R.above=="below"]
    out["above_minus_below_welch"] = pd.Series(dict(diff=ab.ex.mean()-be.ex.mean(),
        t=stats.ttest_ind(ab.ex.dropna(), be.ex.dropna(), equal_var=False)[0], n_ab=len(ab), n_be=len(be)))
    lv = R[R.volq=="low"]
    out["lowvol_spearman_raw_ex"] = pd.Series(dict(rho=stats.spearmanr(lv.raw, lv.ex, nan_policy="omit")[0], n=len(lv)))
    return out
