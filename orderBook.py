from sideBook import sideBook
from order import Order

class orderBook:
    def __init__(self, instrumentName, tickSize):
        self.instrumentName = str(instrumentName)
        self.tickSize = float(tickSize)

        self.bLim = sideBook('B')
        self.sLim = sideBook('S')
        self.bMkt = sideBook('B')
        self.sMkt = sideBook('S')
        
    def addOrder(self, order):
        if order.instrumentID == self.instrumentName:
            if order.side == 'B':
                if order.type == 'lim':
                    self.bLim.addOrder(order)
                elif order.type == 'mktStop':
                    self.bMkt.addOrder(order)
            elif order.side == 'S':
                if order.type == 'lim':
                    self.sLim.addOrder(order)
                elif order.type == 'mktStop':
                    self.sMkt.addOrder(order)
    
    def getAggressingOrder(self):
        mktBid, mktAsk = self.bMkt.bestOrder, self.sMkt.bestOrder
        limBid, limAsk = 'null', 'null'
        if mktBid is not None:
            limAsk = self.sLim.bestOrder
            if mktBid.price < limAsk.price:
                mktBid = None
        if mktAsk is not None:
            limBid = self.bLim.bestOrder
            if mktAsk.price > limBid.price:
                mktAsk = None
        mktBidPresent = mktBid is not None
        mktAskPresent = mktAsk is not None    
        if mktBidPresent and mktAskPresent:
            return mktBid if mktBid.orderID < mktAsk.orderID else mktAsk
        else:
            if mktBidPresent:
                return mktBid
            if mktAskPresent:
                return mktAsk
        
        if limBid == 'null':
            limBid = self.bLim.bestOrder
        if limAsk == 'null':
            limAsk = self.sLim.bestOrder
        if limBid is None:
            return None
        if limAsk is None:
            return None
        if limBid.price < limAsk.price:
            return None
        return limBid if limBid.orderID < limAsk.orderID else limAsk

    def matchOrders(self):
        matches = []
        while True:
            aggressingOrder = self.getAggressingOrder()
            if aggressingOrder is None:
                break
            print('aggressor', aggressingOrder.orderID)
            currentMatches = []
            if aggressingOrder.side == 'B':
                currentMatches = self.sLim.fillOrder(aggressingOrder)
            else:
                currentMatches = self.bLim.fillOrder(aggressingOrder)
            for match in currentMatches[0]:
                if aggressingOrder.side == 'B':
                    if aggressingOrder.type == 'lim':
                        self.bLim.fillBestOrder(match[3])
                    else:
                        self.bMkt.fillBestOrder(match[3])
                else:
                    if aggressingOrder.type == 'lim':
                        self.sLim.fillBestOrder(match[3])
                    else:
                        self.sMkt.fillBestOrder(match[3])
            matches.extend(currentMatches[0])
            matches.extend(currentMatches[1])
            
        return matches

