class MockUser:
    def __init__(self, email, password):
        self.email = email
        self.password = password



class MockUserPasswordHash:
    def __init__(self, email, password_hash, is_verified=True, user_id="d3f865a9-2e1c-45cb-8130-05462f562e69"):
        self.user_id = user_id
        self.email = email
        self.password_hash = password_hash
        self.is_verified = is_verified


class MockUserInvestment:
    def __init__(self, email, created_at, updated_at, investments=None, is_verified=True, user_id="d3f865a9-2e1c-45cb-8130-05462f562e69"):
        if investments is None:
            investments = []
        self.user_id = user_id
        self.email = email
        self.is_verified = is_verified
        self.created_at = created_at
        self.updated_at = updated_at
        self.investments = investments

class MockUserInvestmentPasswordHash:
    def __init__(self, email, password_hash, created_at, updated_at, investments=None, is_verified=True, user_id="d3f865a9-2e1c-45cb-8130-05462f562e69"):
        if investments is None:
            investments = []
        self.user_id = user_id
        self.email = email
        self.password_hash = password_hash
        self.is_verified = is_verified
        self.created_at = created_at
        self.updated_at = updated_at
        self.investments = investments


class MockInvestment:
    def __init__(self, investment_id, scheme_code, scheme_name, units, fund_family, nav, date, current_value):
        self.scheme_code = scheme_code
        self.scheme_name = scheme_name
        self.units = units
        self.fund_family = fund_family
        self.nav = nav
        self.date = date
        self.current_value = current_value
        self.investment_id = investment_id


class MockInvestmentUpdate:
    def __init__(self, scheme_code, units, current_value):
        self.scheme_code = scheme_code
        self.units = units
        self.current_value = current_value


class MockInvestmentDelete:
    def __init__(self, scheme_code):
        self.scheme_code = scheme_code

class MockInvestmentFetch:
    def __init__(self, scheme_code):
        self.scheme_code = scheme_code
