"""Defines the application behaviours for acting on an analysi.
"""

import structlog

from exchange import ExchangeInterface
from notification import Notifier
from analysis import StrategyAnalyzer
from sentiment import SentimentAnalyzer
from database import DatabaseHandler
from behaviours.default import DefaultBehaviour
<<<<<<< HEAD
from behaviours.rsi_bot import RSIBot
from behaviours.af_bot import AFBot
=======
from behaviours.rsi_bot import RsiBotBehaviour
from behaviours.reporter import ReporterBehaviour
from behaviours.ui.server import ServerBehaviour
>>>>>>> cf45720f5b9a47ee855d8222c3ffde69a5cfb717


class Behaviour(object):
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

        behaviour_config = self.config.behaviours[selected_behaviour]

        if selected_behaviour == 'default':
            behaviour = self.__configure_default(behaviour_config)

        if selected_behaviour == 'rsi_bot':
            behaviour = self.__configure_rsi_bot(behaviour_config)


        if selected_behaviour =='af_bot':
            behaviour = self.__configure_af_bot(behaviour_config)

        if selected_behaviour == 'reporter':
            behaviour = self.__configure_reporter(behaviour_config)

        if selected_behaviour == 'server':
            behaviour = self.__configure_server(behaviour_config)


        return behaviour


    def __configure_default(self, behaviour_config):
        """Configures and returns the default behaviour class.

        Args:
            behaviour_config (dict): A dictionary of configuration values pertaining to the
                behaviour.

        Returns:
            DefaultBehaviour: A class of functionality for the default behaviour.
        """

        exchange_interface = ExchangeInterface(self.config.exchanges)

        strategy_analyzer = StrategyAnalyzer(exchange_interface)


        sentiment_analyzer = SentimentAnalyzer(exchange_interface)

       

        notifier = Notifier(self.config.notifiers)


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
            RsiBotBehaviour: A class of functionality for the rsi bot behaviour.
        """

        exchange_interface = ExchangeInterface(self.config.exchanges)
        strategy_analyzer = StrategyAnalyzer(exchange_interface)
        notifier = Notifier(self.config.notifiers)
        db_handler = DatabaseHandler(self.config.database)

        behaviour = RsiBotBehaviour(
            behaviour_config,
            exchange_interface,
            strategy_analyzer,
            notifier,
            db_handler
        )

        return behaviour

    def __configure_reporter(self, behaviour_config):
        """Configures and returns the reporter behaviour class.

        Args:
            behaviour_config (dict): A dictionary of configuration values pertaining to the
                behaviour.

        Returns:
            ReporterBehaviour: A class of functionality for the reporter behaviour.
        """

        exchange_interface = ExchangeInterface(self.config.exchanges)
        notifier = Notifier(self.config.notifiers)
        db_handler = DatabaseHandler(self.config.database)

        behaviour = ReporterBehaviour(
            behaviour_config,
            exchange_interface,
            notifier,
            db_handler
        )

        return behaviour

    def __configure_server(self, behaviour_config):
        """Configures and returns the server (UI) behavior class.

        Args:
            behaviour_config (dict): A dictionary of configuration values pertaining to the
                behaviour.

        Returns:
            Server: A class of functionality for the Flask server behaviour.
        """

        exchange_interface = ExchangeInterface(self.config.exchanges)
        strategy_analyzer = StrategyAnalyzer(exchange_interface)
        notifier = Notifier(self.config.notifiers)
        db_handler = DatabaseHandler(self.config.database)

        behaviour = ServerBehaviour(
            behaviour_config,
            exchange_interface,
            strategy_analyzer,
            notifier,
            db_handler)

        return behaviour

    def __configure_server(self, behaviour_config):
        """Configures and returns the server (UI) behavior class.

        Args:
            behaviour_config (dict): A dictionary of configuration values pertaining to the
                behaviour.

        Returns:
            Server: A class of functionality for the Flask server behaviour.
        """

        exchange_interface = ExchangeInterface(self.config.exchanges)
        strategy_analyzer = StrategyAnalyzer(exchange_interface)
        notifier = Notifier(self.config.notifiers)
        db_handler = DatabaseHandler(self.config.database)

        behaviour = ServerBehaviour(
            behaviour_config,
            exchange_interface,
            strategy_analyzer,
            notifier,
            db_handler)

        return behaviour


    def __configure_af_bot(self, behaviour_config):
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
        

        behaviour = AFBot(
            behaviour_config,
            exchange_interface,
            strategy_analyzer,
            sentiment_analyzer,
            notifier)

        return behaviour
