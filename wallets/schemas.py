from enum import Enum
from uuid import UUID
from pydantic.alias_generators import to_camel
from pydantic import BaseModel, ConfigDict, Field, field_serializer, validator


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class Base(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        from_attributes=True,
        arbitrary_types_allowed = True,
        alias_generator = to_camel
    )

    @field_serializer("id", check_fields=False,)
    def uuid_to_str(uuid: UUID | None):
        return str(uuid) if uuid else None

class OperationRequest(Base):
    operation_type: OperationType = Field(alias="operationType")
    amount: float

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v

class OperationResponse(Base):
    id: UUID
    operationType: OperationType = Field(alias="operation_type")
    amount: int

class WalletResponse(Base):
    id: UUID
    name: str
    balance: int

class WalletCreateRequest(Base):
    name: str = Field(default='Кошелек')
    balance: float = Field(default=0.0)

    @validator('balance')
    def balance_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('Balance must be non-negative')
        return v

class WalletGetRequest(Base):
    id: UUID = Field(alias="id")
