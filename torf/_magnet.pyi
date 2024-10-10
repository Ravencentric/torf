from collections import defaultdict
from collections.abc import Iterable
from re import Pattern
from typing import Any, Callable

from typing_extensions import Self

from ._errors import TorfError
from ._torrent import Torrent
from ._utils import URL, MonitoredList

class Magnet:
    _INFOHASH_REGEX: Pattern[str] = ...
    _XT_REGEX: Pattern[str] = ...
    def __init__(
        self,
        xt: str,
        *,
        dn: str | None = None,
        xl: int | None = None,
        tr: Iterable[str] | str | None = None,
        xs: str | None = None,
        as_: str | None = None,
        ws: Iterable[str] | str | None = None,
        kt: Iterable[str] | str | None = None,
        **kwargs: Any,
    ) -> None: ...
    @property
    def dn(self) -> str | None: ...
    @dn.setter
    def dn(self, value: str) -> None: ...
    @property
    def xt(self) -> str: ...
    @xt.setter
    def xt(self, value: str) -> None: ...
    @property
    def infohash(self) -> str: ...
    @infohash.setter
    def infohash(self, value: str) -> None: ...
    @property
    def xl(self) -> int | None: ...
    @xl.setter
    def xl(self, value: int) -> None: ...
    @property
    def tr(self) -> MonitoredList[str]: ...
    @tr.setter
    def tr(self, value: Iterable[str] | str | None) -> None: ...
    @property
    def xs(self) -> URL | None: ...
    @xs.setter
    def xs(self, value: str | None) -> None: ...
    @property
    def as_(self) -> URL | None: ...
    @as_.setter
    def as_(self, value: str | None) -> None: ...
    @property
    def ws(self) -> MonitoredList[str]: ...
    @ws.setter
    def ws(self, value: Iterable[str] | str | None) -> None: ...
    @property
    def kt(self) -> list[str] | None: ...
    @kt.setter
    def kt(self, value: Iterable[str] | str | None) -> None: ...
    @property
    def x(self) -> defaultdict[str, Any]: ...
    def torrent(self) -> Torrent: ...
    def get_info(
        self, validate: bool = True, timeout: int = 60, callback: Callable[[TorfError], None] | None = None
    ) -> bool: ...

    _KNOWN_PARAMETERS: tuple[str, ...] = ...
    @classmethod
    def from_string(cls, uri: str) -> Self: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...