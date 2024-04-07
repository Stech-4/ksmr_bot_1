class State:    
    def __init__(self) -> None:
        self._in_order = False
        self._in_payment = False
        self._in_admin =False
    def resetState(self): 
        self._in_order = False
        self._in_payment = False
    def setOrder(self, new_order):
        self._in_order = new_order
    def setPayment(self, new_payment):
        self._in_order = new_payment
    def getState(self): 
        return {'in_order': self._in_order, 
                'in_payment': self._in_payment,
                'in_admin' :self._in_admin}
    def setAdmin(self,new_Admin):
        self._in_admin=new_Admin
        
