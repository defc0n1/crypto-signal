"""Provides some basic database functionality on which to build bots.
"""

import structlog

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import sessionmaker
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from db.base import BASE
from db.holdings import Holdings
from db.transactions import Transactions


class YoutubeSentiment(Base):
    """Class for use with the sqlalchemy ORM. Contains youtube sentiment.
    """

    __tablename__ = 'youtubesentiment'

    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    exchange = Column(String)
    base_symbol = Column(String)
    quote_symbol = Column(String)
    action = Column(String)
    base_value = Column(Float)
    quote_value = Column(Float)
    fee_rate = Column(Float)
    base_volume = Column(Float)
    quote_volume = Column(Float)

    def __repr__(self):
        return "<YoutubeSentiment(\
            exchange='%s',\
            create_time='%s',\
            update_time='%s',\
            quote_symbol='%s',\
            youtube_channel='%s',\
            channel_views='%s',\
            action='%s',\
            base_value='%s',\
            quote_value='%s',\
            fee_rate='%s',\
            base_volume='%s',\
            quote_volume='%s')>" % (
                self.exchange,
                self.create_time,
                self.update_time,
                self.quote_symbol,
                self.youtube_channel,
                self.channel_views,
                self.action, # buy/sell
                self.base_value,
                self.quote_value,
                self.base_volume,
                self.quote_volume
            )



class DatabaseHandler():
    """Class that serves as the interface for bots to use to interact with the database.
    """

    @retry(
        retry=retry_if_exception_type(OperationalError),
        stop=stop_after_attempt(3),
        wait=wait_fixed(10)
    )
    def __init__(self, database_config):
        """Initializes the DatabaseHandler class.

        Args:
            database_config (dict): A dictionary containing configuration for databases.
        """

        connection_string = self.__create_connection_string(database_config)
        engine = create_engine(connection_string)
        BASE.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        self.session = session()
        self.logger = structlog.get_logger()

        self.tables = {
            "holdings": Holdings,
            "transactions": Transactions
        }


    def __create_connection_string(self, database_config):
        """Creates a SQL connection string depending on what is configured.

        Args:
            database_config (dict): A dictionary containing configuration for databases.

        Returns:
            str: A SQL connection string.
        """

        connection_string = database_config['engine'] + "://"
        if database_config['username'] and database_config['password']:
            connection_string += ':'.join([
                database_config['username'],
                database_config['password']])

        if database_config['host']:
            connection_string += '@' + database_config['host']

        if database_config['port']:
            connection_string += ':' + database_config['port']

        if database_config['db_name']:
            connection_string += '/' + database_config['db_name']

        return connection_string


    def read_rows(self, table_name, filter_args={}):
        """Returns a query object containing the contents of the requested table.

        Args:
            table_name (str): the string representation of the database table to query.
            filter_args (dict): A dictionary of query filter values.

        Returns:
            sqlalchemy.Query: A sqlalchemy query object with applied filters.
        """

        return self.session.query(self.tables[table_name]).filter_by(**filter_args)


    def row_exists(self, table_name, filter_args={}):
        """Returns a query object containing the contents of the requested table.

        Args:
            table_name (str): the string representation of the database table to query.
            filter_args (dict): A dictionary of query filter values.

        Returns:
            sqlalchemy.Query: A sqlalchemy query object with applied filters.
        """

        exists = False
        instance = self.session.query(self.tables[table_name]).filter_by(**filter_args).first()
        if instance:
            exists = True

        return exists


    def create_row(self, table_name, create_args):
        """Attempts to create a record in the requested table.

        Args:
            table_name (str): the string representation of the database table to query.
            create_args (dict): A dictionary of column value mappings.

        Returns:
            bool: Was the create a success?
        """

        create_success = True
        try:
            self.session.add(self.tables[table_name](**create_args))
            self.session.commit()
        except SQLAlchemyError:
            create_success = False
            self.logger.error("Failed to create holding record!", create_args=create_args)
            self.session.rollback()
        return create_success


    def update_row(self, table_name, row, update_args={}):
        """Attempts to update a record isn the requested table.

        Args:
            holding (Holdings): An instance of the holding class to apply the update to.
            update_args (dict): A dictionary of column value mappings.

        Returns:
            bool: Was the update a success?
        """

        update_success = True
        try:
            self.session.query(self.tables[table_name]).filter_by(id=row.id).update(update_args)
            self.session.commit()
        except SQLAlchemyError:
            update_success = False
            self.logger.error("Failed to update holding record!", update_args=update_args)
            self.session.rollback()
        return update_success


    def read_rows_after_date(self, table_name, date):
        """Returns a query object containing the contents of the requested table.

        Args:
            table_name (str): the string representation of the database table to query.
            filter_args (dict): A dictionary of query filter values.

        Returns:
            sqlalchemy.Query: A sqlalchemy query object with applied filters.
        """

        return self.session.query(
            self.tables[table_name]
        ).filter(
            self.tables[table_name].create_time >= date
        )


    def expire_cache(self):
        """Expire database cache for session.
        """
        self.session.expire_all()


    def create_youtubesentiment(self, create_args):
        """Attempts to create a record in the youtubeSentiment table.

        Args:
            create_args (dict): A dictionary of column value mappings.

        Returns:
            bool: Was the create a success?
        """

        create_success = True
        try:
            self.session.add(YoutubeSentiment(**create_args))
            self.session.commit()
        except SQLAlchemyError:
            create_success = False
            self.logger.error("Failed to create youtube sentiment record!", create_args=create_args)
            self.session.rollback()
        return create_success

    def read_youtubesentiment(self, filter_args={}):
        """Returns a query object containing the contents of the youtubesentiment table.

        Args:
            filter_args (dict): A dictionary of query filter values.

        Returns:
            sqlalchemy.Query: A sqlalchemy query object with applied filters.
        """

        return self.session.query(YoutubeSentiment).filter_by(**filter_args)




