import pandas as pd, numpy as np
from scipy import stats

def rsi_wilder(c, n=14):
    d = c.diff()
    up = d.clip(lower=0).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    return 100 - 100/(1+up/dn)

def explore(data):
    out = {}
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            f = b["forecast"]
            rsi = 50 - b["debug_info.components.rsi_high.last_history_value"]
            out["rsi_quantiles_" + coin + w] = rsi.quantile([0.05,0.25,0.5,0.75,0.95,1.0])
            out["rsi_when_fc<=-10"] = rsi[f <= -10].describe()
            out["rsi_when_fc_between_-10_0"] = rsi[(f < 0) & (f > -10)].describe()
            out["rsi_when_fc_0"] = rsi[f == 0].describe()
            c = b["close"].reset_index(drop=True)
            fwd = c.shift(-5)/c - 1
            grid = (np.arange(len(c)) % 5 == 0) & fwd.notna().values
            out["grid_blocks_total_" + coin + w] = int(grid.sum())
            # per-case grid outcomes at fc<=-10
            ff = f.reset_index(drop=True)
            m = grid & (ff <= -10).values
            out["grid_ext_cases_excess"] = pd.Series((fwd[m] - fwd.mean()).values)
            # needed n for t=-2 given observed std/mean (all-bar estimate)
            x = (fwd[(ff <= -10).values & fwd.notna().values] - fwd.mean())
            out["cases_needed_for_t2_at_observed_effect"] = float((2*x.std()/abs(x.mean()))**2) if len(x)>1 else np.nan
            # share of bars with fc<=-10 -> blocks needed
            share = float((ff <= -10).mean())
            out["share_bars_fc<=-10"] = share
            out["bars_needed_for_30_grid_cases_at_share"] = float(30*5/share) if share>0 else np.nan
            # RSI recomputed on closes to check stays below 60
            r = rsi_wilder(c)
            out["recomputed_rsi_max"] = float(r.max())
            out["recomputed_rsi_min"] = float(r.min())
            # standardised z among bars
            out["post_pipeline_quantiles"] = b["debug_info.components.rsi_high.post_pipeline_value"].quantile([0.0,0.05,0.1,0.25,0.5])
            # daily coin return std
            d = data["days"][coin][w]
            out["daily_ret_std"] = float(d["coin_return"].std())
            out["total_coin_return_window"] = float(c.iloc[-1]/c.iloc[0]-1)
    return out
