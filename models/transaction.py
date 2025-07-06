from typing import Literal
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

curencies = ["AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV", "BRL", "BSD", "BTN", "BWP", "BYR", "BZD", "CAD", "CDF", "CHE", "CHF", "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", "IDR", "ILS", "INR", "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LTL", "LVL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRO", "MUR", "MVR", "MWK", "MXN", "MXV", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLL", "SOS", "SRD", "SSP", "STD", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "USN", "USS", "UYI", "UYU", "UZS", "VEF", "VND", "VUV", "WST", "XAF", "XAG", "XAU", "XBA", "XBB", "XBC", "XBD", "XCD", "XDR", "XFU", "XOF", "XPD", "XPF", "XPT", "XTS", "XXX", "YER", "ZAR", "ZMW"]  # noqa: 501


class Transaction(BaseModel):

    transaction_id: str | None = Field(
        default=None, description="Unique transaction ID"
    )
    amount: float = Field(default=0, gt=0, description="Transaction amount")
    currency: str = Field(..., description="Transaction currency in ISO 4217")
    type: Literal["income", "expense"]
    category_id: int = Field(..., description="Transaction category id")
    date: str | None = Field(default=None, description="Added dated in DD.MM.YYYY")
    description: str | None = Field(default=None, description="Transaction description")

    @field_validator("date")
    @classmethod
    def is_correct_date_format(cls, value: str) -> str:
        try:
            if datetime.strptime(value, "%d.%m.%Y"):
                return value
        except ValueError:
            raise ValueError("date format should be DD.MM.YYYY")

    @field_validator("currency")
    @classmethod
    def is_valid_currency(cls, value: str) -> str:
        try:
            if value.upper() in curencies:
                return value
        except ValueError:
            raise ValueError(f"{value} not found in the list of supported currencies")

