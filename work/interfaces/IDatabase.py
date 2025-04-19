from abc import ABC, abstractmethod
import pandas as pd

class IDatabase(ABC):
    @abstractmethod
    def _connect(self):
        """Устанавливает подключение к базе данных."""
        pass

    @abstractmethod
    def _close(self):
        """Закрывает соединение с базой данных."""
        pass

    @abstractmethod
    def create_tables(self, sql_files_directory):
        """Создает таблицы и индексы."""
        pass

    @abstractmethod
    def create_views(self, sql_files_directory):
        """Создает представления."""
        pass

    @abstractmethod
    def load_log(self, log_path: str):
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
    def get_requests_by_ip_and_date(self) -> pd.DataFrame:
        """
        Абстрактный метод для получения сводных данных по запросам по IP и дате.
        
        :return: Сводная таблица с количеством запросов по IP и дате.
        """
        pass
