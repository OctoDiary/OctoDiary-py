#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

import datetime
from typing import Optional

from pydantic import Field

from ...model import Type


class Rank(Type):
    average_mark_five: Optional[float] = Field(..., alias='averageMarkFive')
    rank_place: Optional[int] = Field(..., alias='rankPlace')
    rank_status: Optional[str] = Field(..., alias='rankStatus')
    trend: Optional[str] = None


class PreviousRankItem(Type):
    average_mark_five: Optional[float] = Field(..., alias='averageMarkFive')
    rank_place: Optional[int] = Field(..., alias='rankPlace')


class RatingRankClass(Type):
    person_id: Optional[str] = Field(..., alias='personId')
    rank: Optional[Rank] = None
    previous_rank: Optional[PreviousRankItem] = Field(..., alias='previousRank')
    image_id: Optional[int] = Field(..., alias='imageId')


class RatingRankShort(Type):
    date: datetime.date
    rankPlace: int


class RatingRankSubject(Type):
    subject_id: int = Field(..., alias='subjectId')
    subject_name: str = Field(..., alias='subjectName')
    rank: Rank
