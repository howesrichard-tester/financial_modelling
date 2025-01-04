# cash_flows class

class CashFlows:
    def __init__(self):
        self.maturities = []
        self.amounts = []
    
    def add_cash_flow(self, maturity, amount):
        self.maturities.append(maturity)
        self.amounts.append(amount)

    def get_cash_flow(self, maturity):
        if maturity in self.maturities:
            return self.amounts[self.maturities.index(maturity)]
        else:
            return None
        
    def get_cash_flows(self):
        return list(zip(self.amounts, self.maturities))
        
# create a class for a bond that inherits from CashFlows

class Bank_bill(CashFlows):

    def __init__(self):
        super().__init__()
        self.face_value = 100
        self.maturity = 0
        self.ytm = 0
        self.price = 0
    
    def set_face_value(self, face_value):
        self.face_value = face_value

    def set_maturity(self, maturity):
        self.maturity = maturity

    def set_ytm(self, ytm):
        self.ytm = ytm
        self.price = self.face_value/(1 + self.ytm*self.maturity)

    def set_price(self, price):
        self.price = price
        self.ytm = (self.face_value/price - 1)/self.maturity

    def get_price(self):
        return self.price
    
    def get_face_value(self):
        return self.face_value
    
    def get_maturity(self):
        return self.maturity
    
    def get_ytm(self):
        return self.ytm
    
    def set_cash_flows(self):
        self.add_cash_flow(0, -self.price)
        self.add_cash_flow(self.maturity, self.face_value)