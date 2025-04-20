from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

class IEntry(ABC):
    @property
    @abstractmethod
    def ip(self) -> str:
        pass

    @property
    @abstractmethod
    def remote_user(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def user_id(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def datetime(self) -> datetime:
        pass

    @property
    @abstractmethod
    def request_type(self) -> str:
        pass

    @property
    @abstractmethod
    def api(self) -> str:
        pass

    @property
    @abstractmethod
    def protocol(self) -> str:
        pass

    @property
    @abstractmethod
    def status_code(self) -> int:
        pass

    @property
    @abstractmethod
    def response_size(self) -> int:
        pass

    @property
    @abstractmethod
    def response_time(self) -> int:
        pass

    @property
    @abstractmethod
    def referer(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def ua(self) -> str:
        pass

    @property
    @abstractmethod
    def parsed_ua(self):
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass
