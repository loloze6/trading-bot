import os
from dotenv import load_dotenv

load_dotenv(override=True)

USE_TESTNET = os.getenv("USE_TESTNET", "True").lower() == "true"

if USE_TESTNET:
    API_KEY = os.getenv("BINANCE_API_KEY_TEST")
    API_SECRET = os.getenv("BINANCE_API_SECRET_TEST")
    BASE_URL = os.getenv("BASE_URL_TEST", "https://testnet.binance.vision/api")

else:
    API_KEY = os.getenv("BINANCE_API_KEY")
    API_SECRET = os.getenv("BINANCE_API_SECRET")
    BASE_URL = os.getenv("BASE_URL", "https://api.binance.com")

from typing import Dict, List, Optional, Union, Any
import json
import logging

logger = logging.getLogger("trading_bot")  # Use the logger set up elsewhere


class ConfigManager:
    """Manages the configuration of the trading bot."""

    def __init__(self, config_path: str = "config.json"):
        """
        Initialize the ConfigManager.

        Args:
            config_path: Path to the configuration file
        """
        config_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(config_dir)
        self.config_path = os.path.join(base_dir, config_path)
        self.logger = logging.getLogger("trading_bot")
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file.

        Returns:
            Configuration dictionary
        """
        # Default configuration

        # Try to load from file
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded_config = json.load(f)

                # Merge with default config to ensure all keys exist
                self.logger.debug(f"Configuration loaded from {self.config_path}")

            except json.JSONDecodeError as e:
                self.logger.error(f"Invalid JSON in configuration file: {e}")
                self.logger.warning("Using default configuration")
            except Exception as e:
                self.logger.error(f"Error loading configuration: {e}")
                self.logger.debug("Using default configuration")
        else:
            logger.error(f"Configuration file {self.config_path} not found.")
            # Save default config
            return {}

        return loaded_config

    def save_config(self, config: Optional[Dict] = None) -> bool:
        """
        Save configuration to file.

        Args:
            config: Configuration to save (uses current config if None)

        Returns:
            True if successful, False otherwise
        """
        try:
            config_to_save = config if config is not None else self.config

            config_dir = os.path.dirname(self.config_path)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir)

            with open(self.config_path, "w") as f:
                json.dump(config_to_save, f, indent=4)
            self.logger.debug(f"Configuration saved to {self.config_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
            return False

    def get(self, section: str, key: Optional[str] = None, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            section: Configuration section
            key: Configuration key (if None, returns entire section)
            default: Default value if key is not found

        Returns:
            Configuration value
        """
        if section not in self.config:
            # self.logger.debug (f"Section '{section}' not found in config, returning default")
            return default

        if key is None:
            return self.config[section]

        value = self.config[section].get(key, default)
        # if value == default and default is not None:
        # self.logger.debug (f"Key '{section}.{key}' not found, using default: {default}")

        return self.config[section].get(key, default)

    def validate(self) -> bool:
        """
        Validate the configuration.

        Returns:
            True if valid, False otherwise
        """
        validation_errors = []
        try:
            # Check if there are symbols to trade
            symbols = self.config.get("trading", {}).get("symbols")
            if not symbols or len(symbols) == 0:
                self.logger.error("No trading symbols specified")
                return False

            self.logger.debug("Configuration validation passed")
            return True

        except Exception as e:
            self.logger.error(f"Configuration validation exception: {e}")
            return False

    def get_log_level(self) -> int:
        """
        Get logging level as integer constant.

        Returns:
            Logging level constant (e.g., logging.INFO)
        """
        level_str = self.get("logging", "level", "INFO").upper()
        return getattr(logging, level_str, logging.INFO)

    def __repr__(self) -> str:
        """String representation of ConfigManager."""
        return f"ConfigManager(config_path='{self.config_path}')"

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"Config loaded from {self.config_path} with {len(self.config)} sections"
