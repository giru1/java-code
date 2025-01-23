from fastapi import HTTPException

from wallets.models import Wallet, Operation
from wallets.schemas import WalletResponse, OperationType, OperationResponse

from dao.base import BaseDAO


class WalletDAO(BaseDAO):
    model = Wallet

    @classmethod
    async def get_wallet(cls, filter_by: dict = {}):
        wallet: Wallet | None = await cls.get_one_or_none(filter_by)
        if not wallet:
            return None
        return WalletResponse.model_validate(wallet)

    @classmethod
    async def update_wallet(cls, filter_by: dict, data: dict = {}) -> WalletResponse:
        updated_wallets = await cls.update(filter_by={**filter_by}, data={**data})
        if not updated_wallets:
            return None
        return WalletResponse.model_validate(updated_wallets[0])

    @classmethod
    async def create_wallet(cls, data: dict = {}) -> WalletResponse:

        wallet = await cls.add({**data})
        if not wallet:
            raise HTTPException(status_code=400, detail="Failed to create wallet")

        return WalletResponse.model_validate(wallet)


class OperationDAO(BaseDAO):
    model = Operation

    @classmethod
    async def process_operation(cls, wallet_id, data: dict = {}) -> OperationResponse:

        wallet: Wallet | None = await WalletDAO.get_wallet({"id": wallet_id})
        if not wallet:
            raise HTTPException(
                status_code=404,
                detail=f"Wallet with id {wallet_id} not found"
            )

        operation_type = data.get('operation_type')

        # Выполняем операцию
        if operation_type == OperationType.DEPOSIT.value:
            new_balance = wallet.balance + data['amount']
        else:  # WITHDRAW
            if wallet.balance < data['amount']:
                raise ValueError("Insufficient funds")
            new_balance = wallet.balance - data['amount']

        await WalletDAO.update_wallet(
            filter_by={"id": wallet_id},
            data={"balance": new_balance}  # передаем только баланс
        )

        operation_data = {
            "wallet_id": wallet_id,
            **data
        }

        operation = await cls.add(operation_data)
        return OperationResponse.model_validate(operation)
