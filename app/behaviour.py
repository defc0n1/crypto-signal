"""Defines the application behaviours for acting on an analysi.
"""

import structlog

from exchange import ExchangeInterface
from notification import Notifier
from analysis import StrategyAnalyzer
from database import DatabaseHandler
from behaviours.default import DefaultBehaviour
from behaviours.rsi_bot import RSIBot


class Behaviour():
    """A class containing all of the possible behaviours
    """

    def __init__(self, config):
        """Initializes the Behaviour class

        Args:
            config (dict): A dictionary of configurations.
        """

        self.config = config


    def get_behaviour(self, selected_behaviour):
        """Returns a behaviour class depending on which behaviour you want to run.

        Args:
            selected_behaviour (str): Which behaviour you want to execute.

        Returns:
            Behaviour: An instance of the behaviour class for the selected behaviour.
        """

        behaviour_config = self.config.get_behaviour_config(selected_behaviour)

        if selected_behaviour == 'default':
            behaviour = self.__configure_default(behaviour_config)

        if selected_behaviour == 'rsi_bot':
            behaviour = self.__configure_rsi_bot(behaviour_config)

        return behaviour


    def __configure_default(self, behaviour_config):
        """Configures and returns the default behaviour class.

        Args:
            behaviour_config (dict): A dictionary of configuration values pertaining to the
                behaviour.

        Returns:
            DefaultBehaviour: A class of functionality for the default behaviour.
        """

        exchange_interface = ExchangeInterface(self.config.get_exchange_config())

        strategy_analyzer = StrategyAnalyzer(exchange_interface)

        notifier = Notifier(self.config.get_notifier_config())

        behaviour = DefaultBehaviour(
            behaviour_config,
            exchange_interface,
            strategy_analyzer,
            notifier
            )

        return behaviour


    def __configure_rsi_bot(self, behaviour_config):
        """Configures and returns the rsi bot behaviour class.

        Args:
            behaviour_config (dict): A dictionary of configuration values pertaining to the
                behaviour.

        Returns:
            RSIBot: A class of functionality for the rsi bot behaviour.
        """

        exchange_interface = ExchangeInterface(self.config.get_exchange_config())
        strategy_analyzer = StrategyAnalyzer(exchange_interface)
        notifier = Notifier(self.config.get_notifier_config())
        db_handler = DatabaseHandler(self.config.get_database_config())

        behaviour = RSIBot(
            behaviour_config,
            exchange_interface,
            strategy_analyzer,
            notifier,
            db_handler)

        return behaviour
