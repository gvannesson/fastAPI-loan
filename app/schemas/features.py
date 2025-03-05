from pydantic import BaseModel

class Features(BaseModel):
    
    state: str
    term: int
    no_emp: int
    urban_rural: int
    cat_activities: int
    bank_loan_float: float
    sba_loan_float: float
    franchise_code: int
    lowdoc: bool
    bank: str
