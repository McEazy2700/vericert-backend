from typing import Optional
from algokit_utils import (
    Account,
    AlgoClientConfig,
    get_algod_client,
    get_indexer_client,
)
from algosdk import mnemonic
from algosdk.v2client.algod import AlgodResponseType
from pydantic import BaseModel, Field
from veecert_backend.apps.common.smart_contract_client import CertClient
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


def get_account() -> Account:
    return Account(private_key=mnemonic.to_private_key(settings.deployer_mnemonic))


algod_config = AlgoClientConfig(settings.algod_server, "")


class Contract:
    algod_client = get_algod_client(algod_config)
    indexer_client = get_indexer_client(algod_config)
    account = get_account()

    @classmethod
    def get_transaction_info(cls, txn_id: str) -> TransactionResponse:
        res = cls.algod_client.pending_transaction_info(txn_id)
        return TransactionResponse.model_validate(res)

    @classmethod
    def get_app_client(cls) -> CertClient:
        return CertClient(
            cls.algod_client,
            app_id=settings.smart_contract_application_id,
            signer=cls.account.signer,
        )
