# Component wish list

One block per idea that needs components the catalogue does not have.

## 020-02_support-retest-bounces-up_1d
- Component: SupportTouchCountComponent: from high, low and close over the last 90 bars, it finds the swing lows (a bar whose low is below the lows of the k bars on each side, confirmed only k bars later so there is no lookahead). It counts those whose low lies within a band (for example 1.5 percent) of the current close, only while the close has come down to that band from above (close below its own value n bars ago). Each touch is weighted by how near the close sits to it, so the value is 0 with no nearby turns and grows continuously with the number of past turns at the level and with nearness | measures: situation

## 020-03_resistance-breakout-continues-up_1d
- Component: ResistanceBreakTouchCountComponent: on 1d bars, it finds the swing highs among the closes of the last 90 bars (a close above its neighbours, followed by a fall) and groups those within a small percent band into levels. It outputs the number of touches of the highest level the current close has just crossed above, times the close's percent distance above that level. It is 0 when no held level was crossed, and grows with both the touch count and the margin of the break. | measures: situation
- Component: LevelTouchCountComponent: from the closes (or highs) of the last 90 bars, the number of past turn-downs at the nearest level below the current close, within a percent band. It is 0 when there is none, and rises by one with each further reversal at that level. | measures: comparison

## 020-04_support-breakdown-continues-down_1d
- Component: SupportTouchCount: over bars t-90 .. t-1, finds the swing lows (a low below the lows of its n neighbouring bars on each side), groups those within a band (for example 1 percent) into levels, and for the level nearest above the close gives the number of swing lows in it; from low and close; grows by one with each further turn at that level | measures: comparison
- Component: HeldLevelBreakDepth: at bar t, the percent distance of the close below the most-touched support level of bars t-90 .. t-1 (as above), times its touch count, and 0 when the close is above every such level; from low and close; grows continuously with the depth of the break and with the count of times the level held | measures: situation
