# Exploration windows only (E-072)

This run's windows were split before the backtests. You read the **exploration windows**
only (listed in `injected_context.explore_confirm.exploration_windows` and in each file's
`windows_shown`). Every result in your inputs comes from those windows.

- **Withheld on purpose:** the confirmation windows, every number computed over all
  windows (pooled `overall` slices, pooled grid criteria, the idea status, earlier runs'
  effects, registry correlations). A field marked `withheld` is not missing data and is not
  zero. Never guess it, never cite it, never infer it.
- **Your side findings are checked on windows you never saw.** After every reader, code
  measures each side finding's tests on the confirmation windows: a price-only finding in
  this run, a forecast or regime block claim in the run built from it. It records whether
  the **claimed sign held** there, counted against how many such looks were taken. That is
  the bar, not proof. The confirmation windows are within your training period, so "never
  saw" means never saw in this pipeline: do not recall what the market did then; read only
  what your inputs show.
- So state the direction you expect (`direction`) and choose tests that would show it on
  any window, not only on the ones you see here. A finding seen in one exploration window
  only is weak; say so in its scores.
