#    ____       _        _____  _                  
#   / __ \     | |      |  __ \(_)                 
#  | |  | | ___| |_ ___ | |  | |_  __ _ _ __ _   _ 
#  | |  | |/ __| __/ _ \| |  | | |/ _` | '__| | | |
#  | |__| | (__| || (_) | |__| | | (_| | |  | |_| |
#   \____/ \___|\__\___/|_____/|_|\__,_|_|   \__, |
#                                             __/ |
#                                            |___/ 
# 
#                 © Copyright 2023
#        🔒 Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

import datetime
from typing import List, Optional

from ...model import Type


class PayloadItem(Type):
    description: Optional[str] = None
    subject_id: Optional[int] = None
    subject_name: Optional[str] = None
    date: Optional[datetime.date] = None
    date_assigned_on: Optional[str] = None
    homework_entry_student_id: Optional[int] = None
    materials_count: Optional[List] = None
    has_written_answer: Optional[bool] = None
    is_done: Optional[bool] = None
    type: Optional[str] = None


class ShortHomeworks(Type):
    payload: Optional[List[PayloadItem]] = None
