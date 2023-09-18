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

from typing import Optional

from ...model import Type


class Theme(Type):
    type: Optional[str] = None
    is_automatic: Optional[bool] = None
    color_pattern: Optional[str] = None


class UserSettings(Type):
    goal: Optional[bool] = None
    theme: Optional[Theme] = None
    schedule_type: Optional[str] = None
    estimation_type: Optional[str] = None
