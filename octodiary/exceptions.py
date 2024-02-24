#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Optional, Union


class APIError(Exception):
    """Base class for all API errors"""

    def __init__(
            self,
            url: str,
            status_code: int,
            error_types: Union[str, list[str]],
            description: Optional[str] = None,
            details = None
        ) -> None:
        errors = " & ".join(error_types) if isinstance(error_types, list) else error_types
        error_text = f"API-Error [{status_code}] - {errors}:\nURL: {url}"

        if description:
            error_text += f"\n{description}"

        super().__init__(error_text)

        self.url = url
        self.status_code = status_code
        self.description = description
        self.errors = self.error_types = error_types
        self.details = details
