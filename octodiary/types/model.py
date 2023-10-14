#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

import json
import typing
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel


class Type(BaseModel):
    @staticmethod
    def __default__(type: "Type"):
        if isinstance(type, (bytes, typing.Match)):
            return repr(type)
        elif isinstance(type, (Enum, datetime, date)):
            return str(type)

        return {
            "_": type.__class__.__name__,
            **(
                {
                    attr: getattr(type, attr)
                    for attr in filter(lambda x: not x.startswith("_"), type.__dict__)
                    if getattr(type, attr) is not None
                } if hasattr(type, "__dict__") else {}
            )
        }

    def __str__(self) -> str:
        return json.dumps(
            self,
            indent=4,
            default=Type.__default__,
            ensure_ascii=False
        )


class EveryType(Type):
    id: int
    name: str
    actual_from: str
    actual_to: str
