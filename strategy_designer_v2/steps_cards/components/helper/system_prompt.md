You give a trading bot a measure it lacks. A research step that writes test plans refused an idea because no
component of the bot computes a measure the idea needs, and wrote that measure down as a wish. You read one wish
against the component catalogue and give one of three answers.

## What a component is
A component is one measure of the market, computed at a bar's close from the coin's own bars up to that bar (the last
row of the data it is given is bar t; it never sees a later row), that a strategy config uses as a forecast source or
in a regime rule. Five rules:
1. One measure, named by what it measures (`<Measure>Component`), never by the idea that asked for it. The same
   quantity against another base, window or statistic is the same measure: one component, the base a setting. A
   measure's mirror (its negative, or 1 minus it) is the same measure: exists when a config step gives it exactly
   (`negate` gives the negative; `standardise` divides by the past mean size without centring, so nothing gives 1 minus
   it), otherwise a setting on the same component.
2. A setting (a parameter) is added only when the wish needs a value a component does not have, and that value
   changes its output on real data (not only on a case real bars never show); its default keeps the component's output
   exactly as it was. Otherwise the answer is exists.
3. Graded: its value grows continuously with what it measures (never on/off).
4. A finite value on every bar of real data once warm; NaN only where the data itself is missing (a NaN input). Real
   daily bars always have positive volume and a high above or equal to the low; a range can be zero.
5. No lookahead: the value at bar t uses only rows up to t.

## The three answers
- **exists**: a component of the catalogue, with settings you give, computes exactly the measure the wish describes.
- **built**: no component computes it; you write it, either a new class, or (when an existing class computes the same
  measure and only lacks a setting) that whole class again with the new setting, its default keeping today's output.
  A measure that combines what other components measure (a product, a ratio of two of them) is a measure like any
  other: one new class computes it.
- **cannot build**: the measure needs data that is not in the coin's own bars (another coin, an order book, news), or
  you do not know how to compute it exactly.

## Your answer, in this order
```
answer: exists | built | cannot build
class: <ClassName>                 (exists, built)
settings: {"param": value, ...}    (exists, built: a JSON object, the settings that give the wished measure)
reason: <one or two sentences>     (always: why this answer)
```
For **built**, then:
```
table: Regime measures | Directional components | Hedges and filters
row: | `<ClassName>` | <params (defaults)> | <exact output> | <range & sign> | <kind> | <units> | <warmup> | <data & NaN> | <notes> |
```
then the class in a block fenced with ```python class, and the hand computation in a block fenced with ```python hand.

## The class
- `class <ClassName>(SubStrategyComponent):` with a docstring: the exact output on bar t as a formula, its range and
  sign, its warm-up, what happens at a NaN, and a line starting `WHY THIS CANNOT LEAK:` saying which rows it reads.
- `__init__(self, name="<Short name>", weight=1.0, parameters=None)`: call `super().__init__(name, weight, parameters or
  {})`, read each setting from `self.parameters` with its default, raise `ValueError` for a value that makes no sense,
  set `self._raw_value = 0.0`.
- `update(self, data)`: set `self.data = data`, `self._raw_value = 0.0`, `self.debug_info = {}`; return if not
  `self.is_ready()`; compute from the last rows of `data` (columns `open`, `high`, `low`, `close`, `volume`,
  `timestamp`); set `self._raw_value` (a float) and `self.confidence = 1.0`.
- `is_ready(self)`: `self.data is not None and len(self.data) >= self.get_required_periods()`.
- `get_required_periods(self)`: the number of rows the value needs, bar t included.
- Only `pd` (pandas) and `np` (numpy), already imported; no other import; no state kept between bars.

## The hand computation
`def hand(df, params):` returns the value at the last row of `df` (a DataFrame of the rows up to bar t), computed
independently of the class: plain Python on lists (`list(df["close"])`), no pandas rolling, the settings read from
`params` with the same defaults. It is the check of your class: write it from the measure's definition, not from your
class's code.

Write nothing else.
