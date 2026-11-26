"""Topic 47, measurement 1d-7: do the losing streaks of different effects cancel when books are combined? Five
night-5 sessions (different briefs: weekend, learned combination, settlement, absorption, Monday). 500 times: one real
book drawn at random from each session (no choice of the best), combined with equal risk (each book scaled to the same
daily swing, measured on its whole chain), equal-weight daily return; its Calmar against its five books' own. Also the
mean correlation between the drawn books. Writes combine.csv.  python3 topics/47_review/combine.py"""
import pathlib, warnings
import numpy as np, pandas as pd
import streaks as st
from levers import stats

warnings.simplefilter("ignore")
rng = np.random.default_rng(3)
gate = pd.read_csv(pathlib.Path(__file__).with_name("calmar_gate.csv"))
series = {}
for b in gate.itertuples():
    ret, _ = st.per_coin(st.STEPS / "04_backtest" / b.run / "backtests" / b.backtest)
    series[(b.run, b.backtest)] = ret.mean(axis=1).fillna(0.0)
runs = sorted(gate.run.unique())
by_run = {r: [k for k in series if k[0] == r] for r in runs}
rows = []
for i in range(500):
    pick = [by_run[r][rng.integers(len(by_run[r]))] for r in runs]
    df = pd.concat([series[k] for k in pick], axis=1, join="inner").fillna(0.0)
    df = df / df.std() * df.std().mean()                                # equal risk, the same overall size
    alone = [stats(df[c].to_numpy())[0] for c in df.columns]
    comb = stats(df.mean(axis=1).to_numpy())
    corr = df.corr().to_numpy()[np.triu_indices(len(pick), 1)].mean()
    rows.append({"draw": i, "calmar_combined": comb[0], "yearly_combined": comb[1], "fall_combined": comb[2],
                 "calmar_alone_median": float(np.median(alone)), "calmar_alone_best": float(np.max(alone)), "mean_correlation": corr,
                 "paying_in_draw": int(sum(gate.set_index(["run", "backtest"]).loc[k, "pays"] for k in pick))})
d = pd.DataFrame(rows); d.to_csv(pathlib.Path(__file__).with_name("combine.csv"), index=False, float_format="%.4g")
q = lambda s: f"median {s.median():.2f} (middle half {s.quantile(.25):.2f} to {s.quantile(.75):.2f})"
print("days in common per draw: about", len(df))
print("mean correlation between the five books:", q(d.mean_correlation))
print("Calmar of the five books alone (median of the five):", q(d.calmar_alone_median))
print("Calmar of the best of the five:", q(d.calmar_alone_best))
print("Calmar combined:", q(d.calmar_combined), "| combined above 0.75 in", f"{100 * (d.calmar_combined > 0.75).mean():.0f} % of draws")
print("deepest fall combined:", q(100 * d.fall_combined), "% | yearly combined:", q(100 * d.yearly_combined), "%")
z = d[d.paying_in_draw == 0]
print(f"draws with no paying book ({len(z)}): Calmar combined {q(z.calmar_combined)}; above 0.75 in {100 * (z.calmar_combined > 0.75).mean():.0f} %")

# Two checks of the result above.
# (1) Weights known in advance only: each book scaled by its swing over all previous days (at least 120), at most 3x.
# (2) The control: five books drawn from ONE session (one family of effects), the same way.
def combo(pick, lagged):
    df = pd.concat([series[k] for k in pick], axis=1, join="inner").fillna(0.0)
    if lagged:
        sd = df.expanding(min_periods=120).std().shift(1)              # every previous day, at least 120 of them
        wgt = (sd.mean(axis=1).to_numpy()[:, None] / sd).clip(upper=3.0)  # no book above 3 times the mean weight
        df = (df * wgt).fillna(0.0)
    else:
        df = df / df.std() * df.std().mean()
    return stats(df.mean(axis=1).to_numpy())[0], np.median([stats(df[c].to_numpy())[0] for c in df.columns])
out = {"different sessions, weights known in advance": [], "one session (one family)": []}
for i in range(300):
    out["different sessions, weights known in advance"].append(combo([by_run[r][rng.integers(len(by_run[r]))] for r in runs], True))
    r = runs[rng.integers(len(runs))]
    out["one session (one family)"].append(combo([by_run[r][j] for j in rng.choice(len(by_run[r]), 5, replace=False)], False))
for k, v in out.items():
    v = np.array(v)
    print(f"{k}: combined Calmar median {np.median(v[:, 0]):.2f} against alone {np.median(v[:, 1]):.2f}; above 0.75 in {100 * (v[:, 0] > 0.75).mean():.0f} %")
