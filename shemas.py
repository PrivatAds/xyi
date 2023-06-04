from typing import Literal
from pydantic import BaseModel

class ConnectRequestModel(BaseModel):
    connect_token: str


class ConnectResponseModel(BaseModel):
    session_token: str
    crypt_key: str


class DisonnectRequestModel(BaseModel):
    session_token: str


class UpdateRequestModel(BaseModel):
    update_token: str
    session_token: str
    encrypted_data: str


class ShutdownRequsetModel(BaseModel):
    shutdown_token: str


class ShutdownResponseModel(BaseModel):
    deleted_keys: list
    active: bool


class ActivateRequestModel(BaseModel):
    activate_token: str


class ActivateResponseModel(BaseModel):
    deleted_keys: list
    active: bool


class GetRequestModel(BaseModel):
    # get_token: str
    eU9Xehtp30LXt3o14IhqTkhy3Ee1: str


class GetResponseModel(BaseModel):
    # session_token: str
    sN246BggZjXTB0bnH3xN6NewNy7a16N9mE9NF6KHcM: str
    # success: bool
    xywQynARfHj20q6t39ybWzCCLueEUihRMt6vxg: bool


class GetDataRequestModel(BaseModel):
    # get_data_token: str
    Us5vZjR7QA21VVI2D9xR2ZChfoQfEWH4vpcLZ: str
    # session_token: str
    KOtaocIzsb5rQgrxG10Sm1b2UqgHs: str


class GetDataResponseModel(BaseModel):
    # data: str
    iYOgo72xmUlFOiXS0cwx7LtlfeRmuR: str


class SetRequestModel(BaseModel):
    # session_token: str
    HcuDqZTReL1ActRjpLlaTgAogUCFnLmFChP8nUtCSoQ: str
    # status: str
    sHRNaIvKvRgcutW7iVsPOrdA6: Literal["ExhvNRSe1EOZ9JZu8uPqSffbO6", "m1eI5EN2M6kiyuWoXbMHLpW73Fx5suA"]
    #  ExhvNRSe1EOZ9JZu8uPqSffbO6 - active
    #  m1eI5EN2M6kiyuWoXbMHLpW73Fx5suA - locked


class GetStatusRequestModel(BaseModel):
    # session token
    BylnIL0Bkw4GbvFmtVJivdMPXlEiEbF: str


class GetStatusResponseModel(BaseModel):
    # status
    UW40olHWnbCnN1qFeGoSJqh3yMQNCET6xb2ARROFR10: Literal[
        "xsKXNa55MMGujASVrXfKLyjMtUICf7LqmGKNdCEDMpc",
        "srCOdvltUWogYgCX4b3hFwDVKj8Zv1dLHtTWqZL1HJE",
        "5CQ8SNLryXz1cYENr8tmcXpIgvf33XMEwfztobepl9g"
    ]
    #  xsKXNa55MMGujASVrXfKLyjMtUICf7LqmGKNdCEDMpc - active
    #  srCOdvltUWogYgCX4b3hFwDVKj8Zv1dLHtTWqZL1HJE - locked
    #  5CQ8SNLryXz1cYENr8tmcXpIgvf33XMEwfztobepl9g - expired