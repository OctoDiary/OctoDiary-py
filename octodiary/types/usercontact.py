from typing import Any, Optional

from .model import Type
from .persondata import EveryType


class UserContact(Type):
    data: Optional[str] = None
    type: Optional[EveryType] = None
    is_deleted: Optional[Any] = None
