from interfaces.IEntry import IEntry
from datetime import datetime
from model.UserAgents import UserAgents
from typing import Optional

class Entry(IEntry):
    def __init__(self, log, parsed_ua):
        self.ip = log[0]  # Используется setter
        self.remote_user = log[1] if log[1] != '-' else None
        self.user_id = log[2] if log[2] != '-' else None
        self.datetime = self.parse_datetime(log[3], log[4], log[5])  # Используется setter
        self.request_type = log[6]
        self.api = log[7]
        self.protocol = log[8]
        self.status_code = int(log[9])  # Используется setter
        self.response_size = int(log[10])  # Используется setter
        self.referer = log[11] if log[11] != '-' else None
        self.response_time = int(log[13]) if log[13] != '-' else None
        self.ua = log[12]  # Используется setter
        self.parsed_ua = UserAgents(*parsed_ua)

        # id поля для справочников
        self.ip_id: Optional[int] = None
        self.referer_id: Optional[int] = None
        self.api_id: Optional[int] = None
        self.user_agent_id: Optional[int] = None
        self.request_type_id: Optional[int] = None
        self.protocol_id: Optional[int] = None

    def parse_datetime(self, date_str, time_str, time_zone_str):
        datetime_str = f"{date_str} {time_str} {time_zone_str}"
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S %z")

    @property
    def ip(self) -> str:
        return self._ip

    @ip.setter
    def ip(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("IP должен быть строкой")
        self._ip = value

    @property
    def remote_user(self) -> Optional[str]:
        return self._remote_user

    @remote_user.setter
    def remote_user(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("remote_user должен быть строкой или None")
        self._remote_user = value

    @property
    def user_id(self) -> Optional[str]:
        return self._user_id

    @user_id.setter
    def user_id(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("user_id должен быть строкой или None")
        self._user_id = value

    @property
    def datetime(self) -> datetime:
        return self._datetime

    @datetime.setter
    def datetime(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise ValueError("datetime должен быть объектом datetime")
        self._datetime = value

    @property
    def request_type(self) -> str:
        return self._request_type

    @request_type.setter
    def request_type(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("request_type должен быть строкой")
        self._request_type = value

    @property
    def api(self) -> str:
        return self._api

    @api.setter
    def api(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("api должен быть строкой")
        self._api = value

    @property
    def protocol(self) -> str:
        return self._protocol

    @protocol.setter
    def protocol(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("protocol должен быть строкой")
        self._protocol = value

    @property
    def status_code(self) -> int:
        return self._status_code

    @status_code.setter
    def status_code(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("status_code должен быть целым числом")
        self._status_code = value

    @property
    def response_size(self) -> int:
        return self._response_size

    @response_size.setter
    def response_size(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("response_size должен быть целым числом")
        self._response_size = value

    @property
    def response_time(self) -> Optional[int]:
        return self._response_time

    @response_time.setter
    def response_time(self, value: Optional[int]) -> None:
        if value is not None and not isinstance(value, int):
            raise ValueError("response_time должен быть целым числом или None")
        self._response_time = value

    @property
    def referer(self) -> Optional[str]:
        return self._referer

    @referer.setter
    def referer(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("referer должен быть строкой или None")
        self._referer = value

    @property
    def ua(self) -> str:
        return self._ua

    @ua.setter
    def ua(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("ua должен быть строкой")
        self._ua = value

    @property
    def parsed_ua(self):
        return self._parsed_ua

    @parsed_ua.setter
    def parsed_ua(self, value):
        # Убедитесь, что передаваемый объект parsed_ua является экземпляром UserAgents или правильно обработан
        if not isinstance(value, UserAgents):
            raise ValueError("parsed_ua должен быть экземпляром UserAgents")
        self._parsed_ua = value

    def __repr__(self):
        return f"Entry(ip={self.ip}, datetime={self.datetime}, api={self.api}, status_code={self.status_code}, response_time={self.response_time})"
