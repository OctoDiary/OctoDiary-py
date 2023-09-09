import json
import typing
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Type(BaseModel):
    @staticmethod
    def __default__(type: "Type"):
        if isinstance(type, (bytes, typing.Match)):
            return repr(type)
        elif isinstance(type, (Enum, datetime)):
            return str(type)

        return {
            "_": type.__class__.__name__,
            **{
                attr: getattr(type, attr)
                for attr in filter(lambda x: not x.startswith("_"), type.__dict__)
                if getattr(type, attr) is not None
            }
        }

    def __str__(self) -> str:
        return json.dumps(
            self,
            indent=4,
            default=Type.__default__,
            ensure_ascii=False
        )


class TypeMobile(BaseModel):
    type: typing.Optional[str] = None
    description: typing.Optional[str] = None
    mobileSubscriptionStatus: typing.Optional[str] = None
    errorCode: typing.Optional[str] = None
    
    @staticmethod
    def __default__(type: typing.Union["TypeMobile", "Type"]):
        if isinstance(type, (bytes, typing.Match)):
            return repr(type)
        elif isinstance(type, (Enum, datetime)):
            return str(type)

        return {
            "_": type.__class__.__name__,
            **{
                attr: getattr(type, attr)
                for attr in filter(lambda x: not x.startswith("_"), type.__dict__)
                if getattr(type, attr) is not None
            }
        }

    def __str__(self) -> str:
        return json.dumps(
            self,
            indent=4,
            default=Type.__default__,
            ensure_ascii=False
        )
    

class AutoNameEnum(Enum):
    def _generate_next_value_(self, *args):
        return self.lower()

    def __repr__(self):
        return f"octodiary.types.{self}"
