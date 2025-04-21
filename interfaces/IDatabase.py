from abc import ABC, abstractmethod
import pandas as pd

from model.Entry import Entry as IEntry
from typing import List

class IDatabase(ABC):

    @abstractmethod
    def __init__(self, connection_params):
        pass  # set configuration for connection

    @abstractmethod
    def _connect(self):
        """Устанавливает подключение к базе данных."""
        pass

    @abstractmethod
    def _close(self):
        """Закрывает соединение с базой данных."""
        pass

    @abstractmethod
    def create_tables(self, sql_files_directory=None):
        """Создает таблицы и индексы."""
        pass

    @abstractmethod
    def create_views(self, sql_files_directory=None):
        """Создает представления."""
        pass

    @abstractmethod
    def load_log(self, entries: List[IEntry]):
        """Загружает лог-файл в базу данных."""
        pass

    @abstractmethod
    def get_view_data(self, view_name: str) -> pd.DataFrame:
        """
        Абстрактный метод для получения данных из указанного представления.
        
        :param view_name: Название представления в базе данных.
        :return: DataFrame с данными из представления.
        """
        pass

    @abstractmethod
    def get_views(self) -> List[str]:
        pass

    # @abstractmethod
    # def get_requests_by_ip_and_date(self) -> pd.DataFrame:
    #     """
    #     Метод для получения сводных данных по запросам по IP и дат из датафрейма
    #
    #     :return: Сводная таблица с количеством запросов по IP и дате.
    #     """
    #     pass
