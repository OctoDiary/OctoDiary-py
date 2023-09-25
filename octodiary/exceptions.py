#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, Optional


class APIError(Exception):
    """Обработка всех ошибок"""

    def __init__(self, url: str, status_code: int, error_type: str, description: Optional[str] = None,
                 details: Optional[Any] = None) -> None:
        error_text = f"API-Error [{status_code}] - {error_type}:\nURL: {url}"

        if description:
            error_text += f"\n{description}"

        super().__init__(error_text)

        self.url = url
        self.status_code = status_code
        self.description = description
        self.error_type = error_type
        self.details = details
