from order import Order
import copy
class sideBook:
    def __init__(self, side):
        self.orders = {}
        self.side = side
    
    def addOrder(self, order):
        if not order.price in self.orders:
            self.orders[order.price] = {}
            self.orders = {i:self.orders[i] for i in sorted(list(self.orders.keys()), reverse = self.side == 'B')}
        insertionPrice = self.orders[order.price]
        insertionPrice[order.orderID] = order
        
    def fillBestOrder(self, qty):
        bestOrder = self.bestOrder
        
        bestOrder.qty -= qty
        # print(bestOrder.traderID, bestOrder.qty)
        if bestOrder.qty <= 0:
            del self.orders[bestOrder.price][bestOrder.orderID]
            if self.orders[bestOrder.price] == {}:
                del self.orders[bestOrder.price]
            return True
        
    def delOrder(self, order):
        if order.price in self.orders:
            priceLevel = self.orders[order.price]
            if order.orderID in priceLevel:
                del self.orders[order.price][order.orderID]
                if self.orders[order.price] == {}:
                    del self.orders[order.price]
        
    @property
    def bestOrder(self):
        try:
            bestLevel = self.orders[self.bestPrice]
            return bestLevel[next(iter(bestLevel))]
        except:
            return None
        
    
    @property
    def bestPrice(self):
        if self.orders:
            return next(iter(self.orders))
        
    def fillOrder(self, incomingOrder):
        aggressingOrder = copy.deepcopy(incomingOrder)
        # the following line has a bug
        #aggressingOrder = incomingOrder
        bookFills = []
        aggressingOrderFills = []
        exchangeCommissions = 0
        while aggressingOrder.qty >= 0:
            bp = self.bestOrder
            if bp is None:
                break
            if aggressingOrder.side == 'B' and bp.price > aggressingOrder.price:
                break
            if aggressingOrder.side == 'S' and bp.price < aggressingOrder.price:
                break
            qtyToFill = min(aggressingOrder.qty, bp.qty)
            #print(bp.qty)
            makerPrice = bp.price
            takerPrice = bp.price
            aggressingOrderFills.append([aggressingOrder.traderID, aggressingOrder.orderID, takerPrice, qtyToFill])
            bookFills.append([bp.traderID, bp.orderID, makerPrice, qtyToFill])
            fillResult = self.fillBestOrder(qtyToFill)
            aggressingOrder.qty -= qtyToFill
            if fillResult:
                break
            if aggressingOrder.qty == 0:
                break
        return aggressingOrderFills, bookFills



