#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Optional

from pydantic import Field

from octodiary.types.model import Type


class ClientId(Type):
    contract_id: Optional[int] = Field(None, alias="contractId")
    staff_id: None = Field(None, alias="staffId")
    person_id: Optional[str] = Field(None, alias="personId")


class Organization(Type):
    name: Optional[str] = None
    type: Optional[str] = None
    address: Optional[str] = None


class MealsClients(Type):
    client_id: ClientId | None = Field(None, alias="clientId")
    organization: Organization | None = None
    preorder_allowed: Optional[bool] = Field(None, alias="preorderAllowed")
    balance: Optional[int] = None
    foodbox_allowed: Optional[bool] = Field(None, alias="foodboxAllowed")
    foodbox_available: Optional[bool] = Field(None, alias="foodboxAvailable")
