from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import JSONResponse

from wallets.dao import WalletDAO, OperationDAO

from wallets.schemas import OperationRequest, WalletResponse, OperationResponse, WalletCreateRequest, \
    WalletGetRequest

router = APIRouter(prefix="/wallets", tags=["Wallets"])


@router.post("/{walletId}/operation", response_model=OperationResponse)
async def operate_wallet(body: OperationRequest, walletId: UUID = Path(..., description="The ID of the wallet")):
    try:
        result: OperationResponse = await OperationDAO.process_operation(
            walletId, {**body.model_dump(exclude_none=True)}
        )
        if not result:
            raise HTTPException(status_code=404, detail="Wallet not found")
        return JSONResponse(content=result.model_dump(by_alias=True), status_code=200)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", response_model=WalletResponse)
async def create_wallet(body: WalletCreateRequest):
    try:
        wallet = await WalletDAO.create_wallet(data=body.model_dump())
        return JSONResponse(content=wallet.model_dump(by_alias=True), status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=WalletResponse)
async def get_wallet_balance(params: WalletGetRequest = Depends()):
    wallet = await WalletDAO.get_wallet(params.model_dump(exclude_none=True))
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return JSONResponse(content=wallet.model_dump(by_alias=True), status_code=200)
