from binance.client import Client
from config.settings import API_KEY, API_SECRET, USE_TESTNET
import pandas as pd
import logging
from typing import Dict, List, Optional, Union, Tuple, Any, Callable
import datetime
import os
import numpy as np
import ccxt
import time

from collections import defaultdict
from dataclasses import dataclass
import threading
import queue



logger = logging.getLogger("trading_bot")  # Use the logger set up elsewhere


@dataclass
class PriceTick:
    """Individual price tick."""
    symbol: str
    price: float
    timestamp: datetime.datetime
    volume: Optional[float] = None

@dataclass
class Candle:
    """Custom candle structure."""
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    start_time: datetime.datetime
    end_time: datetime.datetime
    tick_count: int = 0

class CandleBuilder:
    """Builds custom candles from real-time price ticks."""
    
    def __init__(self, interval_seconds: int, candle_completion_callback: Callable[[str, Candle], None] = None):
        """
        Initialize CandleBuilder.
        
        Args:
            interval_seconds: Candle interval in seconds
            candle_completion_callback: Function to call when a candle is completed
                                      Should accept (symbol: str, candle: Candle) parameters
        """
        self.interval_seconds = interval_seconds
        self.current_candles: Dict[str, Candle] = {}
        self.completed_candles: Dict[str, List[Candle]] = defaultdict(list)
        self.candle_completion_callback = candle_completion_callback
        
    def add_tick(self, tick: PriceTick) -> Optional[Candle]:
        """
        Add a price tick and return completed candle if interval finished.
        
        Returns:
            Completed candle if interval finished, None otherwise
        """
        symbol = tick.symbol
        
        # Get or create current candle
        if symbol not in self.current_candles:
            self.current_candles[symbol] = self._start_new_candle(tick)
            return None
            
        current = self.current_candles[symbol]
        
        # Check if we need to close current candle and start new one
        if (tick.timestamp - current.start_time).total_seconds() >= self.interval_seconds:
            # Close current candle
            completed_candle = current
            self.completed_candles[symbol].append(completed_candle)
            
            # Call completion callback if provided
            if self.candle_completion_callback:
                try:
                    self.candle_completion_callback(symbol, completed_candle)
                except Exception as e:
                    logger.error(f"Error in candle completion callback for {symbol}: {e}", exc_info=True)
            
            # Start new candle
            self.current_candles[symbol] = self._start_new_candle(tick)
            
            return completed_candle
        else:
            # Update current candle
            self._update_candle(current, tick)
            return None
    
    def _start_new_candle(self, tick: PriceTick) -> Candle:
        """Start a new candle with the given tick."""
        # Align to interval boundaries
        aligned_time = self._align_to_interval(tick.timestamp)
        
        return Candle(
            symbol=tick.symbol,
            open=tick.price,
            high=tick.price,
            low=tick.price,
            close=tick.price,
            volume=tick.volume or 0,
            start_time=aligned_time,
            end_time=aligned_time + datetime.timedelta(seconds=self.interval_seconds),
            tick_count=1
        )
    
    def _update_candle(self, candle: Candle, tick: PriceTick):
        """Update existing candle with new tick."""
        candle.high = max(candle.high, tick.price)
        candle.low = min(candle.low, tick.price)
        candle.close = tick.price
        candle.volume += tick.volume or 0
        candle.tick_count += 1
    
    def _align_to_interval(self, timestamp: datetime.datetime) -> datetime.datetime:
        """Align timestamp to interval boundary."""
        # Round down to nearest interval
        total_seconds = int(timestamp.timestamp())
        aligned_seconds = (total_seconds // self.interval_seconds) * self.interval_seconds
        return datetime.datetime.fromtimestamp(aligned_seconds)
    
    def get_candle_history(self, symbol: str, count: int = 1) -> pd.DataFrame:
        """Get historical candles as DataFrame."""
        candles = self.completed_candles.get(symbol, [])[-count:]
        
        if not candles:
            return pd.DataFrame()
        
        data = []
        for candle in candles:
            data.append({
                'timestamp': candle.start_time,
                'open': candle.open,
                'high': candle.high,
                'low': candle.low,
                'close': candle.close,
                'volume': candle.volume
            })
        
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        return df

class DataManager:
    """Manages real-time data fetching and candle building."""
    
    def __init__(self, symbols: List[str], price_fetch_interval: int, candle_builder: CandleBuilder):
        """
        Initialize DataManager.
        
        Args:
            symbols: List of trading symbols
            price_fetch_interval: Interval for fetching prices in seconds
            candle_builder: CandleBuilder instance for processing ticks
        """
        self.client = Client(API_KEY, API_SECRET, testnet=USE_TESTNET)
        self.symbols = symbols
        self.price_fetch_interval = price_fetch_interval
        self.candle_builder = candle_builder
        self.price_queue = queue.Queue()
        self.running = False

    def initiate_start_thread(self) -> Optional[threading.Thread]:
        """Start the price fetching thread."""
        try:
            price_thread = threading.Thread(target=self._rest_price_fetcher, daemon=True)
            price_thread.start()
            return price_thread
        except Exception as e:
            logger.error(f"Error initiating thread: {e}")
            return None

    def _rest_price_fetcher(self):
        """Fetch prices using REST API at regular intervals for all symbols and store them in a queue."""
        while self.running:
            try:
                # Fetch prices for all symbols in the list
                for symbol in self.symbols:
                    if not self.running:  # Check if we should stop
                        break
                        
                    price_data = self._get_current_price(symbol)
                    
                    if price_data:
                        tick = PriceTick(
                            symbol=symbol,
                            price=price_data['price'],
                            timestamp=datetime.datetime.now(),
                            volume=price_data.get('volume', 0)
                        )
                        self.price_queue.put(tick)
                    else:
                        logger.warning(f"Failed to fetch price for {symbol}")
                
                # Log fetching activity for multiple symbols
                if len(self.symbols) > 1:
                    logger.debug(f"Fetched prices for {len(self.symbols)} symbols")
                
                time.sleep(self.price_fetch_interval)
                
            except Exception as e:
                logger.error(f"Error fetching prices for symbols {self.symbols}: {e}", exc_info=True)
                time.sleep(1)  # Brief pause before retrying

    def _get_current_price(self, symbol: str) -> Optional[Dict]:
        """Get current price from exchange."""
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return {
                'price': float(ticker['price']),
                'volume': 0  # You'd get this from 24hr ticker if needed
            }
        except Exception as e:
            logger.error(f"Error getting price for {symbol}: {e}")
            return None

    def _main_candle_processing_loop(self):
        """Main loop that retrieve ticks from a queue and ask to process it."""
        while self.running:
            try:
                # Process all queued price ticks (handles multiple symbols)
                processed_ticks = 0
                while not self.price_queue.empty():
                    tick = self.price_queue.get_nowait()
                    self._process_price_tick(tick)
                    processed_ticks += 1
                
                # Log activity if processing multiple symbols
                if processed_ticks > 0:
                    logger.debug(f"Processed {processed_ticks} price ticks")
                
                time.sleep(0.1)  # Small sleep to prevent CPU spinning
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error in main processing loop: {e}", exc_info=True)

    def _process_price_tick(self, tick: PriceTick):
        """Process a single price tick."""
        try:
            # Add tick to candle builder - this will automatically call the callback
            # when a candle is completed
            completed_candle = self.candle_builder.add_tick(tick)
            
            # Log candle completion (the actual processing is handled by the callback)
            if completed_candle:
                logger.info(f"Candle completed for {tick.symbol}: "
                           f"O:{completed_candle.open} H:{completed_candle.high} "
                           f"L:{completed_candle.low} C:{completed_candle.close}")
                
        except Exception as e:
            logger.error(f"Error processing tick for {tick.symbol}: {e}", exc_info=True)

class MockCandleBuilder:
    """Mock candle builder for backtesting that provides historical data."""
    
    def __init__(self):
        self.candle_history = {}  # Store completed candles for each symbol

    def add_completed_candle(self, symbol: str, candle: Candle):
        """Add a completed candle to the history."""
        if symbol not in self.candle_history:
            self.candle_history[symbol] = []
        self.candle_history[symbol].append(candle)

    # def update_current_data(self, symbol: str, candle_data: pd.Series):
    #     """Update current data for a symbol."""
    #     self.current_data[symbol] = candle_data
    
    def get_candle_history(self, symbol: str, count: int = 1) -> pd.DataFrame:
        """Get historical candles as DataFrame for strategy analysis."""
        if symbol not in self.candle_history or not self.candle_history[symbol]:
            return pd.DataFrame()
        
        # Get the last 'count' candles
        candles = self.candle_history[symbol][-count:]
        
        # Convert to DataFrame
        data = []
        for candle in candles:
            data.append({
                'timestamp': candle.start_time,
                'open': candle.open,
                'high': candle.high,
                'low': candle.low,
                'close': candle.close,
                'volume': candle.volume
            })
        
        return pd.DataFrame(data)

class HistoricalDataManager:
    """Manager of historical data during backtesting."""
    def __init__(self, historical_data: Dict[str, pd.DataFrame] = None, interval_seconds: int = 240):
        """
        Initialize the historical data provider with data library.
        
        Args:
            historical_data: Dictionary mapping symbols to their historical data DataFrames - see structure above
        """
        self.historical_data = historical_data
        self.current_index = {}
        self.candle_builder = None
        
        # For interval aggregation
        self.current_candles = {}  # Accumulating candle data
        self.last_candle_start = {}  # Track when current candle started
        self.interval_seconds = interval_seconds
        
        logger.warning(f"DataManager initiated without data")

    def initialize (self):
        """
        Initialize the DataManager index with historical data.
        """
        for symbol in self.historical_data:
            self.current_index[symbol] = 0
            self.current_candles[symbol] = None
            self.last_candle_start[symbol] = None
            logger.info(f"DataManager initiated with data on {symbol}")

    def get_historical_klines(self, symbol: str, interval: str, limit: int = 1) -> pd.DataFrame:
        """
        Fetch historical kline (candlestick) data at current index (index simulated into HistoricalDataProvider)
        
        Args:
            symbol: Trading pair symbol
            interval: Kline interval (ignored in backtesting)
            limit: Number of klines to retrieve
            
        Returns:
            DataFrame with OHLCV data
        """
        if symbol not in self.historical_data:
            logger.warning(f"No historical data available for {symbol}")
            return pd.DataFrame()
        
        # Get data up to the current index
        current_idx = self.current_index[symbol]
        if current_idx >= len(self.historical_data[symbol][symbol]):
            logger.warning(f"DM - Historical data reached end for {symbol}")
            return pd.DataFrame()  # No more data
            
        # Get data slice
        start_idx = max(0, current_idx - limit + 1)
        data_slice = self.historical_data[symbol][symbol].iloc[start_idx:current_idx + 1].copy()
        return data_slice

    def process_next_tick(self, symbol: str) -> Optional[Candle]:
        """
        Process the next data point and return completed candle if interval is finished.
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Completed candle if interval finished, None otherwise
        """
        if symbol not in self.historical_data:
            return None
            
        data = self.historical_data[symbol][symbol]
        current_idx = self.current_index[symbol]
        
        if current_idx >= len(data):
            return None
            
        current_data = data.iloc[current_idx]
        current_time = pd.to_datetime(current_data['timestamp'])
        
        # Align timestamp to interval boundary
        aligned_time = self._align_to_interval(current_time)
        
        # Check if we need to start a new candle
        if (self.last_candle_start.get(symbol) is None or 
            aligned_time != self.last_candle_start[symbol]):
            
            # Complete previous candle if it exists
            completed_candle = None
            if self.current_candles[symbol] is not None:
                completed_candle = self.current_candles[symbol]
            
            # Start new candle
            self.current_candles[symbol] = Candle(
                symbol=symbol,
                open=current_data['close'],
                high=current_data['close'],
                low=current_data['close'],
                close=current_data['close'],
                volume=current_data['volume'],
                start_time=aligned_time,
                end_time=aligned_time + pd.Timedelta(seconds=self.interval_seconds),
                tick_count=1
            )
            self.last_candle_start[symbol] = aligned_time
            
            return completed_candle
        else:
            # Update existing candle
            candle = self.current_candles[symbol]
            candle.high = max(candle.high, current_data['close'])
            candle.low = min(candle.low, current_data['close'])
            candle.close = current_data['close']
            candle.volume += current_data['volume']
            candle.tick_count += 1
            
            return None

    def _align_to_interval(self, timestamp: pd.Timestamp) -> pd.Timestamp:
        """Align timestamp to interval boundary."""
        # Convert to seconds since epoch, align to interval, convert back
        epoch_seconds = timestamp.timestamp()
        aligned_seconds = (epoch_seconds // self.interval_seconds) * self.interval_seconds
        return pd.Timestamp.fromtimestamp(aligned_seconds)

    def get_final_candle(self, symbol: str) -> Optional[Candle]:
        """Get the final incomplete candle when backtesting ends."""
        return self.current_candles.get(symbol)

    def get_current_candle(self, symbol: str) -> Optional[pd.Series]:
        """Get the current candle for a symbol."""
        if symbol not in self.historical_data:
            return None
            
        data = self.historical_data[symbol][symbol]
        current_idx = self.current_index[symbol]
        
        if current_idx >= len(data):
            return None
            
        return data.iloc[current_idx]

    def advance(self, symbol: str, steps: int = 1) -> bool:
        """
        Advance the current index for a symbol.
        
        Args:
            symbol: Trading pair symbol
            steps: Number of steps to advance
            
        Returns:
            True if successful, False if no more data
        """
        if symbol not in self.historical_data:
            logger.warning(f"{symbol} is not existing - cannot advance index")
            return False

        logger.debug(f"index {self.current_index[symbol]}")
        new_index = self.current_index[symbol] + steps
        if new_index >= len(self.historical_data[symbol][symbol]):
            logger.warning(f"DM - Index of historical data reached end for {symbol}")
            return False
            
        self.current_index[symbol] = new_index
        return True

    def has_more_data(self, symbol: str) -> bool:
        """Check if there's more data available for a symbol."""
        if symbol not in self.historical_data:
            return False
        
        data = self.historical_data[symbol][symbol]
        return self.current_index[symbol] < len(data) - 1

class HistoricalDataFetcher:
    """Provider for historical data during backtesting with intelligent merging."""
    def __init__(self, start_date, end_date, symbols=["BTCUSDT"], candle_interval_seconds=60, exchange="binance", localStorage= False):
        """
        Initialize the data fetcher with date range and symbols.
        
        Args:
            start_date: Start date for data collection (string or datetime)
            end_date: End date for data collection (string or datetime)
            symbols: List of trading symbols to fetch
            candle_interval_seconds: Data interval in seconds 
            exchange: CCXT-supported exchange name (default: binance)
            localStorage: Whether to store data locally (default: False)
        """
        # Convert dates to datetime if they're strings
        self.start_date = pd.to_datetime(start_date) if isinstance(start_date, str) else start_date
        self.end_date = pd.to_datetime(end_date) if isinstance(end_date, str) else end_date
        self.symbols = symbols
        self.candle_interval_ccxt = self._seconds_to_ccxt_interval(candle_interval_seconds)
        self.exchange_id = exchange
        self.localStorage = localStorage

        self.data_cache = {}
        self.data_loaded = False
        
        # Set up data directory
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize exchange
        try:
            exchange_class = getattr(ccxt, self.exchange_id)
            self.exchange = exchange_class({
                'enableRateLimit': True,  # Important to avoid rate limit issues
                'options': {
                    'defaultType': 'spot'  # Use spot markets by default
                }
            })
            logger.info(f"Initialized {self.exchange_id} exchange interface")
        except Exception as e:
            logger.error(f"Failed to initialize exchange {self.exchange_id}: {e}")
            self.exchange = None
    
    def _seconds_to_ccxt_interval(self, seconds):
        intervals = {
            60: '1m',
            300: '5m',
            900: '15m',
            1800: '30m',
            3600: '1h',
            14400: '4h',
            86400: '1d'
        }

        closest_match = min(intervals.keys(), key=lambda x: abs(x - seconds))
        return intervals[closest_match]

    def _timeframe_to_milliseconds(self, timeframe):
        """Convert CCXT timeframe to milliseconds for API requests."""
        # Parse timeframe value and unit
        amount = int(''.join(filter(str.isdigit, timeframe)))
        unit = ''.join(filter(str.isalpha, timeframe))
        
        # Calculate milliseconds
        if unit == 'm':
            return amount * 60 * 1000
        elif unit == 'h':
            return amount * 60 * 60 * 1000
        elif unit == 'd':
            return amount * 24 * 60 * 60 * 1000
        elif unit == 'w':
            return amount * 7 * 24 * 60 * 60 * 1000
        else:
            # Default to 1 hour if unknown
            return 60 * 60 * 1000
    
    def _identify_missing_periods(self, existing_data, start_date, end_date):
        """
        Identify date ranges that are missing from the existing data.
        
        Args:
            existing_data: DataFrame with timestamp column
            start_date, end_date: The overall date range we want to cover
            
        Returns:
            List of (start, end) tuples representing missing periods
        """
        if existing_data.empty:
            logger.debug(f"Existing data empty")
            # No existing data, need to fetch the entire range
            return [(start_date, end_date)]
        
        # Make sure timestamps are datetime
        existing_data['timestamp'] = pd.to_datetime(existing_data['timestamp'])
        
        # Sort the data
        existing_data = existing_data.sort_values('timestamp')
        
        # Generate list of missing periods
        missing_periods = []
        
        # Check if we need data before the earliest timestamp
        earliest_timestamp = existing_data['timestamp'].min()
        if start_date < earliest_timestamp:
            logger.info(f"Potential need of data before the earliest timestamp stored, from: {start_date} to {earliest_timestamp - datetime.timedelta(milliseconds=1)}")
            adjusted_missingPeriod_end = min(earliest_timestamp - datetime.timedelta(milliseconds=1), end_date)
            missing_periods.append((start_date, adjusted_missingPeriod_end))
            
       # Check if we need data after the latest timestamp
        latest_timestamp = existing_data['timestamp'].max()
        logger.debug(f"latest_timestamp: {latest_timestamp}, end_date: {end_date}")

        if end_date > latest_timestamp:
            logger.info(f"Potential need of data after the latest timestamp stored, from: {latest_timestamp + datetime.timedelta(milliseconds=1)} to {end_date}")
            adjusted_missingPeriod_start = max(latest_timestamp + datetime.timedelta(milliseconds=1), start_date)
            missing_periods.append((adjusted_missingPeriod_start, end_date))
        
       # Check for gaps within the data
        timestamps = existing_data['timestamp'].sort_values().values
        
        # Get expected interval
        interval_map = {
            '1m': np.timedelta64(1,'m'),
            '5m': np.timedelta64(5,'m'),
            '15m': np.timedelta64(15,'m'),
            '30m': np.timedelta64(30,'m'),
            '1h': np.timedelta64(1,'h'),
            '4h': np.timedelta64(4,'h'),
            '1d': np.timedelta64(1,'D'),
        }
        expected_interval = interval_map.get(self.candle_interval_ccxt, datetime.timedelta(hours=1))
        
        # Find gaps in existing data
        for i in range(1, len(timestamps)):
            gap = timestamps[i] - timestamps[i-1]
            
            if gap > expected_interval * 1.5:  # Allow some tolerance
                gap_start = timestamps[i-1] + expected_interval
                gap_end = timestamps[i] - np.timedelta64(1, 'ms')
                # Only include gap if it's within our requested range
                logger.debug(f"tgap_start: {gap_start} end_date(milliseconds=1) {end_date} type gap_start[i]: {type(gap_start)}  type timedeltat: {type(end_date)}")

                if gap_start <= np.datetime64(end_date) and gap_end >= np.datetime64(start_date):
                    adjusted_start = max(gap_start, start_date)
                    adjusted_end = min(gap_end, end_date)
                    logger.info(f"Missing data inside the file, from: {adjusted_start} to {adjusted_end}")
                    missing_periods.append((adjusted_start, adjusted_end))
        
        # Merge overlapping periods
        if missing_periods:
            missing_periods.sort()
            merged_periods = [missing_periods[0]]
            
            for current_start, current_end in missing_periods[1:]:
                prev_start, prev_end = merged_periods[-1]
                
                # If periods overlap or are adjacent, merge them
                if current_start <= prev_end + datetime.timedelta(milliseconds=1):
                    merged_periods[-1] = (prev_start, max(prev_end, current_end))
                else:
                    merged_periods.append((current_start, current_end))
            
            return merged_periods
        
        return []

    def _find_existing_data(self, symbol):
        """Find existing local data"""
       
        data_path = os.path.join(self.data_dir, f"{symbol}_{self.candle_interval_ccxt}.csv")
        existing_data = pd.DataFrame()
        
        # Load existing data if available
        if os.path.exists(data_path):
            logger.info(f"Found local data file for {symbol}. Checking coverage...")
            
            try:
                existing_data = pd.read_csv(data_path)
                
                # Ensure timestamp column is in datetime format
                if 'timestamp' in existing_data.columns:
                    existing_data['timestamp'] = pd.to_datetime(existing_data['timestamp'])
                else:
                    logger.warning(f"No timestamp column found in {data_path}")
                    existing_data = pd.DataFrame()  # Reset to empty if invalid format
            
            except Exception as e:
                logger.error(f"Error reading local data for {symbol}: {e}")
                existing_data = pd.DataFrame()
        return existing_data
            
    def _merge_save_data(self, symbol, new_data_pieces, save=False) -> None:
        # Combine existing and new data
        combined_data = pd.concat(new_data_pieces, ignore_index=True)
        
        # Remove duplicates based on timestamp
        combined_data = combined_data.drop_duplicates(subset=['timestamp'])
        
        # Sort by timestamp
        combined_data = combined_data.sort_values('timestamp')
        
        # Save the combined data
        self.data_cache[symbol] = combined_data
        if save:
            data_path = os.path.join(self.data_dir, f"{symbol}_{self.candle_interval_ccxt}.csv")
            combined_data.to_csv(data_path, index=False)
            logger.info(f"Saved merged data for {symbol} and stored locally ")  
        else: logger.info(f"Saved merged data for {symbol} but not stored locally ")
  
    def _fetch_historical_data(self, symbol, start_date, end_date):
        """
        Fetch historical data from cryptocurrency exchange API.
        
        Args:
            symbol: Trading pair to fetch data for (e.g., "BTCUSDT")
            start_date: Start of period to fetch
            end_date: End of period to fetch
            
        Returns:
            DataFrame containing historical price data
        """

        if self.exchange is None:
            logger.error("Exchange not initialized, cannot fetch data")
            return pd.DataFrame()
                
        try:
            # Convert dates to timestamps
            since = int(start_date.timestamp() * 1000)
            until = int(end_date.timestamp() * 1000)
            
            # Convert CCXT timeframe (e.g., '5m', '1h')
            timeframe = self.candle_interval_ccxt
            
            # Prepare lists to store results
            all_candles = []
            current_since = since
            logger.debug(f"since: {since}, until: {until}, since: {since}, ")

            # CCXT has limits on how many candles can be fetched at once
            # We need to make multiple requests for longer periods
            while current_since < until:
                # Some exchanges don't accept 'until' parameter, so we use limit instead
                try:
                    # Standardize symbol format (different exchanges have different requirements)
                    exchange_symbol = symbol
                    # For some exchanges like Binance, we may need to remove the quote currency
                    # e.g., convert BTCUSDT to BTC/USDT
                    if '/' not in symbol and len(symbol) > 3:
                        for quote in ['USDT', 'USD', 'BUSD', 'USDC', 'ETH', 'BTC']:
                            if symbol.endswith(quote):
                                base = symbol[:-len(quote)]
                                exchange_symbol = f"{base}/{quote}"
                                break
                    logger.debug(f"timeframe: {timeframe}, since: {since}, ")
                    
                    # Fetch OHLCV data (Open, High, Low, Close, Volume)
                    candles = self.exchange.fetch_ohlcv(
                        symbol=exchange_symbol,
                        timeframe=timeframe,
                        since=current_since,
                        limit=1000  # Most exchanges limit to 1000 candles per request
                    )

                    if not candles:
                        logger.warning(f"No candles returned for {symbol}")
                        break
                    
                    all_candles.extend(candles)
                    
                    # Update the current_since for the next iteration
                    # Last candle timestamp + one timeframe
                    last_timestamp = candles[-1][0]
                    current_since = last_timestamp + self._timeframe_to_milliseconds(timeframe)
                    
                    # Add a small pause to respect rate limits
                    time.sleep(self.exchange.rateLimit / 1000)
                    
                    # Stop if we've reached the until time or if returned data is too small
                    if last_timestamp >= until or len(candles) < 100:
                        break
                    
                except Exception as e:
                    logger.error(f"Error fetching data for {symbol}: {e}")
                    break
            
            if not all_candles:
                logger.warning(f"No data retrieved for {symbol}")
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(all_candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
            # Convert timestamp from milliseconds to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Add additional columns to match the expected format
            df['close_time'] = df['timestamp'] + pd.Timedelta(milliseconds=self._timeframe_to_milliseconds(timeframe) - 1)
            df['quote_asset_volume'] = df['volume'] * df['close']  # Estimate
            df['number_of_trades'] = np.nan  # Not provided by CCXT's fetch_ohlcv
            df['taker_buy_base_asset_volume'] = np.nan  # Not provided by CCXT's fetch_ohlcv
            df['taker_buy_quote_asset_volume'] = np.nan  # Not provided by CCXT's fetch_ohlcv
            df['ignore'] = 0
            
            return df
        
        except Exception as e:
            logger.error(f"Error in _fetch_historical_data: {e}")
            return pd.DataFrame()

    def _fetch_backtest_data(self) -> None:
        """Load historical data for backtesting, with intelligent merging."""
        for symbol in self.symbols:
            
            # Find existing local data
            if self.localStorage: 
                existing_data = self._find_existing_data(symbol)
            else: 
                existing_data = pd.DataFrame()

            # Identify missing periods
            logger.info(f"Identifying missing periods")
            missing_periods = self._identify_missing_periods(existing_data, self.start_date, self.end_date)
            
            # Fetch data online based on missing periods
            if missing_periods:
                logger.info(f"Need to fetch {len(missing_periods)} missing period(s) for {symbol} ; details: {missing_periods}")
                new_data_pieces = []
                
                if not existing_data.empty:
                    new_data_pieces.append(existing_data)
                # Fetch each missing period              
                for period_start, period_end in missing_periods:
                    logger.info(f"Fetching {symbol} data from {period_start} to {period_end}")
                    period_data = self._fetch_historical_data(symbol, period_start, period_end)
                    
                    if not period_data.empty:
                        new_data_pieces.append(period_data)
                    else:
                        logger.warning(f"DM - Failed to fetch data for {symbol} from {period_start} to {period_end}")
                
                #Merge & Save data pieces
                if new_data_pieces:
                    self._merge_save_data(symbol, new_data_pieces, save=self.localStorage) 
                else:
                    logger.warning(f"No valid data available for {symbol}")
                    self.data_cache[symbol] = pd.DataFrame()
            
            else:
                logger.info(f"Local data for {symbol} is complete for the requested period")
                self.data_cache[symbol] = existing_data
            
            # Filter to requested date range
            if symbol in self.data_cache and not self.data_cache[symbol].empty:
                self.data_cache[symbol] = self.data_cache[symbol][
                    (self.data_cache[symbol]['timestamp'] >= self.start_date) & 
                    (self.data_cache[symbol]['timestamp'] <= self.end_date)
                ]
                
                # Final check of data
                if self.data_cache[symbol].empty:
                    logger.warning(f"No data available for {symbol} in requested date range after filtering")
                else:
                    logger.info(f"Final dataset for {symbol}: {len(self.data_cache[symbol])} records")
        
        self.data_loaded = True
        logger.info("Data loading complete")
        
        # Log summary of data coverage
        for symbol in self.symbols:
            if symbol in self.data_cache and not self.data_cache[symbol].empty:
                data = self.data_cache[symbol]
                logger.info(f"{symbol}: {len(data)} records from {data['timestamp'].min()} to {data['timestamp'].max()}")
            else:
                logger.warning(f"{symbol}: No data available")

    def get_data(self, symbol=None):
        """
        Get the loaded data for a specific symbol or all symbols.
        
        Args:
            symbol: Specific symbol to get data for. If None, returns all data.
            
        Returns:
            Data for the requested symbol(s)
        """
        if not self.data_loaded:
            self._fetch_backtest_data()
            
        if symbol:
            return self.data_cache.get(symbol, pd.DataFrame())
        return self.data_cache



    def validate_data_continuity(self, symbol):
        """
        Check if data has any gaps based on the interval.
        
        Args:
            symbol: Trading symbol to check
            
        Returns:
            Tuple of (is_continuous, gaps) where gaps is a list of missing periods
        """
        if symbol not in self.data_cache or self.data_cache[symbol].empty:
            return False, []
            
        data = self.data_cache[symbol].copy()
        
        # Sort by timestamp to ensure order
        data = data.sort_values('timestamp')
        
        # Convert interval to timedelta
        interval_map = {
            '1m': np.timedelta64(1,'m'),
            '5m': np.timedelta64(5,'m'),
            '15m': np.timedelta64(15,'m'),
            '30m': np.timedelta64(30,'m'),
            '1h': np.timedelta64(1,'h'),
            '4h': np.timedelta64(4,'h'),
            '1d': np.timedelta64(1,'D'),
        }
        
        expected_interval = interval_map.get(self.candle_interval_ccxt, datetime.timedelta(hours=1))
        
        # Get consecutive timestamps
        timestamps = data['timestamp'].sort_values().values
        
        # Find gaps
        gaps = []
        for i in range(1, len(timestamps)):
            diff = timestamps[i] - timestamps[i-1]
            if diff > expected_interval * 1.5:  # Allow some tolerance
                gap_start = timestamps[i-1]
                gap_end = timestamps[i]
                gaps.append((gap_start, gap_end))
        
        is_continuous = len(gaps) == 0
        return is_continuous, gaps