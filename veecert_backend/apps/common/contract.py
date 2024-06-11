from typing import Optional
from algokit_utils import AlgoClientConfig, get_algod_client
from algosdk.v2client.algod import AlgodResponseType
from pydantic import BaseModel, Field
from veecert_backend.config.settings import settings


class TransactionInner(BaseModel):
    amt: int
    fee: int
    fv: int
    gen: str
    gh: str
    lv: int
    lx: Optional[str] = None
    note: str
    rcv: str
    snd: str
    type: str


class Transaction(BaseModel):
    sig: str
    txn: TransactionInner


class TransactionResponse(BaseModel):
    confirmed_round: int = Field(..., alias="confirmed-round")
    pool_error: str = Field(..., alias="pool-error")
    txn: Transaction


class Contract:
    algod_client = get_algod_client(AlgoClientConfig(settings.algod_server, ""))

    @classmethod
    def get_transaction_info(cls, txn_id: str) -> TransactionResponse:
        res = cls.algod_client.pending_transaction_info(txn_id)
        return TransactionResponse.model_validate(res)
