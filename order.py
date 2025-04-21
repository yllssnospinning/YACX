class Order:
    def __init__(self, instrumentID, orderID, traderID, type, price, qty):
        self.orderID = int(orderID)
        self.traderID = str(traderID)
        self.instrumentID = instrumentID

        self.sell, self.buy = self.instrumentID.split('/')

        self.type = type
        self.price = float(price)

        self.side = 'B' if qty > 0 else 'S'
        self.gain = self.buy if self.side == 'S' else self.sell
        self.expenditure = self.sell if self.side == 'S' else self.buy
        self.expenditureAmount = qty if self.side == 'S' else qty * price

        self.qty = abs(float(qty))

        self.totCost = self.price * self.qty
