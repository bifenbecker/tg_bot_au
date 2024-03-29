from enum import Enum


class PartnerState(Enum):
    PARTNER_INIT_STATE = 0
    PARTNER_SET_REGION_NAME = 1
    PARTNER_SET_AMOUNT_DEALS = 2
    PARTNER_SET_AMOUNT_EXPENSE = 3
    PARTNER_SET_GUARANTEES = 4
    PARTNER_SET_EXPERIENCE = 5
    PARTNER_SET_TELEPHONE = 6
