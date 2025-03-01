class MockUser:
    def __init__(self, email, password_hash, is_verified=True):
        self.user_id = "d3f865a9-2e1c-45cb-8130-05462f562e69"
        self.email = email
        self.password_hash = password_hash
        self.is_verified = is_verified


class MockInvestment:
    def __init__(self, investment_id, scheme_code, scheme_name, units, nav, current_value, date, fund_family):
        self.investment_id = "d3f865a9-2e1c-45cb-8130-05462f562e73"
        self.scheme_code = scheme_code
        self.scheme_name = scheme_name
        self.units = units
        self.nav = nav
        self.date = date
        self.current_value = current_value
        self.fund_family = fund_family