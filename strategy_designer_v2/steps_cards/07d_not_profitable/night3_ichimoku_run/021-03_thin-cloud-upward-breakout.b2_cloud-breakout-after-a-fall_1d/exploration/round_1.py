import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 26
    out = {}
    rows = []      # cross bars
    grid = []      # broad grid cases
    book = []
    for coin, wins in data["bars"].items():
        # coin normal drift on non-overlapping 26-bar grid
        fr = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                fr.append(c[i + H] / c[i] - 1)
        drift = np.mean(fr); usual = np.std(fr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            hi = b["high"].values; lo = b["low"].values
            tr = (b["regime"] == "trending").values
            raw = b.get("debug_info.components.prior_fall.last_history_value")
            for i in np.where(tr)[0]:
                prior = c[i] / c[i - H] - 1 if i >= H else np.nan
                fwd = c[i + H] / c[i] - 1 - drift if i + H < n else np.nan
                rows.append(dict(coin=coin, win=w, pos=i, prior=prior,
                                 fc=b["forecast"].iloc[i], fwd=fwd,
                                 alloc=b["postRebalance_current_allocation"].iloc[i]))
            # broad situation on grid: prior 26d return and position vs 52d midpoint
            for i in range(0, n - H, H):
                if i >= 52:
                    mid = (hi[i-51:i+1].max() + lo[i-51:i+1].min()) / 2
                    rng = hi[i-51:i+1].max() - lo[i-51:i+1].min()
                    above = (c[i] - mid) / rng
                else:
                    above = np.nan
                prior = c[i] / c[i - H] - 1 if i >= H else np.nan
                grid.append(dict(coin=coin, prior=prior, above=above,
                                 fwd=c[i + H] / c[i] - 1 - drift, usual=usual))
            a = b["postRebalance_current_allocation"].fillna(0).values
            book.append(dict(coin=coin, n=n, inmkt=(np.abs(a) > 1e-6).mean()))
    X = pd.DataFrame(rows); G = pd.DataFrame(grid); B = pd.DataFrame(book)
    out["cross bars"] = pd.Series(dict(
        n_cross=len(X), with_prior_known=X["prior"].notna().sum(),
        prior_negative=(X["prior"] < 0).sum(), prior_positive=(X["prior"] > 0).sum(),
        forecast_ge2=(X["fc"] >= 2).sum(), forecast_pos=(X["fc"] > 0).sum(),
        with_fwd=X["fwd"].notna().sum(), share_days_in_market=B["inmkt"].mean()))
    X["side"] = np.where(X["prior"] < 0, "after fall", np.where(X["prior"] > 0, "after rise", "unknown"))
    def summ(g):
        f = g["fwd"].dropna()
        return pd.Series(dict(n=len(f), mean_unusual=f.mean(),
                              t=f.mean() / (f.std(ddof=1) / np.sqrt(len(f))) if len(f) > 2 else np.nan,
                              mean_prior=g["prior"].mean()))
    out["cross fwd by prior side"] = X.groupby("side").apply(summ)
    out["cross fwd all"] = summ(X)
    out["crosses per coin"] = X.groupby("coin").size()
    # broad: graded by prior 26d return quintile
    Gp = G.dropna(subset=["prior"]).copy()
    Gp["q"] = pd.qcut(Gp["prior"], 5, labels=False)
    out["grid fwd by prior26 quintile"] = Gp.groupby("q").apply(summ)
    Ga = G.dropna(subset=["above"]).copy()
    Ga["q"] = pd.qcut(Ga["above"], 4, labels=False)
    out["grid fwd by pos vs 52d mid quartile"] = Ga.groupby("q").apply(lambda g: pd.Series(dict(
        n=len(g), mean_unusual=g["fwd"].mean(),
        t=g["fwd"].mean() / (g["fwd"].std(ddof=1) / np.sqrt(len(g))), mean_above=g["above"].mean())))
    r = Gp[["prior", "fwd"]].corr(method="spearman").iloc[0, 1]
    out["grid spearman prior26 vs fwd"] = float(r)
    out["grid n"] = len(Gp)
    out["bars per window mean"] = float(B["n"].mean())
    return out
