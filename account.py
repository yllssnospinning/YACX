import copy as c

class account:
    def __init__(self):
        self.assets = {}
        self.openOrders = {}   
        self.buyingPower = {}
        
    def getOutstandingOrderValue(self, valueToAssess):
        totalValue = 0
        for pairTicker in self.openOrders:
            sell, buy = pairTicker.split()
            if buy == valueToAssess or sell == valueToAssess:
                orders = self.openOrders[pairTicker]
                for order in orders:
                    totalValue.append(order.expenditure)
        return totalValue
    
    def getBuyingPower(self):
        self.buyingPower = c.deepcopy(self.assets)
        for pairTicker in self.openOrders:
            orders = self.openOrders[pairTicker]
            for order in orders:
                if not order.expenditure in self.buyingPower:
                    raise SystemError
                else:
                    self.buyingPower[order.expenditure] -= order.expenditureAmount
    
    def postOrder(self, order):
        if order.expenditure in self.buyingPower:
            maxOrderAmount = self.buyingPower[order.expenditure]
            if order.expenditureAmount <= maxOrderAmount:
                self.openOrders[order.instrumentID][order.orderID] = order
                self.buyingPower[order.expenditure] -= order.expenditure
                
    def fillOrder(self, order, qty, price):
        if order.instrumentID in self.openOrders:
            orders = self.openOrders[order.instrumentID]
            if order.orderID in orders:
                orderToFill = self.openOrders[order.instrumentID][order.orderID]
                if orderToFill.qty >= qty:
                    orderToFill.qty -= qty
                    gain = qty if order.side == 'B' else price * qty
                    loss = price * qty if order.side == 'B' else qty
                    gainAsset = order.gain
                    expenditureAsset = order.expenditure
                    if expenditureAsset in self.assets:
                        self.assets[expenditureAsset] -= loss
                        if not gainAsset in self.assets:
                            self.assets[gainAsset] = 0
                        self.assets[gainAsset] += gain
                    
    
    def changeAsset(self, assetName, chgDelta):
        newAssetCreated = False
        if assetName not in self.assets:
            self.assets[assetName] = 0
            newAssetCreated = True
        if self.assets[assetName] + chgDelta >= 0:
            self.assets[assetName] += chgDelta  
