""" Runs the default behaviour, which performs two functions...
1. Output the signal information to the prompt.
2. Notify users when a threshold is crossed.
"""

import ccxt
import structlog
import coinmarketcap

class AFBot():
    """Default behaviour which gives users basic trading information.
    """

    def __init__(self, behaviour_config, exchange_interface, strategy_analyzer,sentiment_analyzer,notifier,db_handler):
        """Initializes DefaultBehaviour class.

        Args:
            behaviour_config (dict): A dictionary of configuration for this behaviour.
            exchange_interface (ExchangeInterface): Instance of the ExchangeInterface class for
                making exchange queries.
            strategy_analyzer (StrategyAnalyzer): Instance of the StrategyAnalyzer class for
                running analysis on exchange information.
            notifier (Notifier): Instance of the notifier class for informing a user when a
                threshold has been crossed.
        """

        self.behaviour_config = behaviour_config
        self.exchange_interface = exchange_interface
        self.strategy_analyzer = strategy_analyzer
        self.sentiment_analyzer = sentiment_analyzer
        self.notifier = notifier
        self.db_handler = db_handler

    def run(self, market_pairs):
        """The behaviour entrypoint

        Args:
            market_pairs (list): List of symbol pairs to operate on, if empty get all pairs.
        """

        if market_pairs:
            market_data = self.exchange_interface.get_symbol_markets(market_pairs)
        else:
            market_data = self.exchange_interface.get_exchange_markets()
            #open_orders = self.exchange_interface.get_open_orders()



        self.__test_strategies(market_data)

    def __test_strategies(self, market_data):
        """Test the strategies and perform notifications as required

        Args:
            market_data (dict): A dictionary containing the market data of the symbols to analyze.
        """

        channels = ['UCLXo7UDZvByw2ixzpQCufnA',
        'UCTKyJALgd09WxZBuWVbZzXQ',
        'UCmA06PHZc6O--2Yw4Vt4Wug',
        'UCkpMhY4N4ZjpqKMIjzLplKw',
        'UCLXo7UDZvByw2ixzpQCufnA',
        'UCLXo7UDZvByw2ixzpQCufnA',
        'UCLXo7UDZvByw2ixzpQCufnA',
        'UC67AEEecqFEc92nVvcqKdhA',
        'UCTKyJALgd09WxZBuWVbZzXQ',
        'UCmaAtMHgspY0au0NR5oz8PA',
        'UCt_oM56Ui0BCCgi0Yc-Wh3Q',
        'UCcx5piGsKocIXdgnEIASKFA',
        'UCLnQ34ZBSjy2JQjeRudFEDw',
        'UCLXo7UDZvByw2ixzpQCufnA',
        'UCCoF3Mm-VzzZXSHtQKD8Skg',
        'UCEhFzdgTPR8MmeL0z-xbA3g',
        'UCLXo7UDZvByw2ixzpQCufnA',
        'UCLXo7UDZvByw2ixzpQCufnA',
        'UCLXo7UDZvByw2ixzpQCufnA',
        'UCkpt3vvZ0Y0wvTX2L-lkxsg',
        'UCLXo7UDZvByw2ixzpQCufnA',
        'UCv6-ssVyI8zNcZsghkwudHA',
        'UCUullOp2tc92dsu-yW3p_0g',
        'UC-f5nPBEDyUBZz_jOPBwAfQ',
        'UCu7Sre5A1NMV8J3s2FhluCw']

        #twitter_sentiment = self.sentiment_analyzer.analyze_twitter_sentiment(market_data[exchange][market_pair]['symbol'])

        
        symbols = []
        symbol_name = {}
        name_symbol = {}
        #get all coins from coinmarketcap
        coinmarketcapTicker = coinmarketcap.Market()
        coins = coinmarketcapTicker.ticker()
        

        for exchange in market_data:
            print(exchange)
            print(self.exchange_interface.fetch_balance())
            if exchange == "binance":
                 
                
                for market_pair in market_data[exchange]:
                    #print(market_data[exchange][market_pair])
                    symbols.append(market_data[exchange][market_pair]['info']['symbol'])
                    symbol = market_data[exchange][market_pair]['info']['baseAsset']
                    #print(symbol)
                    #lookup altcoin name by altcoin symbol
                    for coin in coins:
                        #print(coin['symbol'])
                        #print(coin['name'])
                        if coin['symbol'] == symbol:
                            name = coin['name'].lower()
                            name_symbol[name] = symbol
                            symbol_name[symbol] = name
                            #print(name)

                    
                    #name = market_data[exchange][market_pair]['info']['MarketCurrencyLong'].lower()
                    
                    
                #print(symbol_name)
                #print(name_symbol)
                
                try:

                    youtube_sentiment = self.sentiment_analyzer.analyze_youtube_sentiment(channels,symbols,symbol_name,name_symbol)
                    #print(youtube_sentiment)

                    for coin in youtube_sentiment:
                        print(coin)
                        print(youtube_sentiment.count(coin))
                    #sentiment_payload = {'exchange': exchange,'symbol': symbol,'volume_free': 0,'volume_used': 0,'volume_total': 0}

                    #self.db_handler.create_youtubesentiment(sentiment_payload)
                except Exception as e:
                    print(e)


