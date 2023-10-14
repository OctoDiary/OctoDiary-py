#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from pydantic import Field

from octodiary.types.model import Type


class ClientId(Type):
    contract_id: int | None = Field(None, alias="contractId")
    staff_id: None = Field(None, alias="staffId")
    person_id: str | None = Field(None, alias="personId")


class Organization(Type):
    name: str | None = None
    type: str | None = None
    address: str | None = None


class MealsClients(Type):
    client_id: ClientId | None = Field(None, alias="clientId")
    organization: Organization | None = None
    preorder_allowed: bool | None = Field(None, alias="preorderAllowed")
    balance: int | None = None
    foodbox_allowed: bool | None = Field(None, alias="foodboxAllowed")
    foodbox_available: bool | None = Field(None, alias="foodboxAvailable")
