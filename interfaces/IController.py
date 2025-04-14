from abc import ABC, abstractmethod
from typing import List

from model.Entry import Entry as IEntry


class IController(ABC):
    """
    Maybe a better name would be DB+Parser to Visualizer bridge,
    or something like that

    purpose of this class is to hide DB and Parser behavior from Visualizer so
    it can execute "easier" functions for understanding
    """

    @abstractmethod
    def parse(self, path) -> None:
        """
        Parses the file at specified path, saves output in internal cache
        throws errors that should be handled with 'try... catch' block, like
        if no file was found
        :param path Relative path to file from directory where the script is run, or absolute path
        """
        pass

    @abstractmethod
    def get_cache(self) -> List[IEntry]:
        """
        Returns all of entries in cache
        :return: list of entries
        """

    @abstractmethod
    def post(self) -> None:
        """
        Posts all of the saved logs in the cache and empties it
        """
        pass

    @abstractmethod
    def get_all(self) -> List[IEntry]:
        """
        Gets all of the entries from database
        :return: list of entries
        """
        pass

    @abstractmethod
    def query(self, query):
        """
        Execute query to DB
        :param query:
        :return: is dependent of the query.
        """
        pass