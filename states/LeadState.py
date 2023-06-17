from enum import Enum


class LeadState(Enum):
    LEAD_INIT_STATE = 0
    LEAD_SET_REGION_NAME = 1
    LEAD_SET_BUSINESS_INFO = 2
    LEAD_SET_AMOUNT_CLIENTS = 3
    LEAD_SET_TELEPHONE = 4
