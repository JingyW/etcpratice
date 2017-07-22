#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json
import time 


class Order():
    def __init__ (self, symbol, price, amount, direction, p, isConvert = False):
        self.symbol = symbol
        self.price = price
        self.amount = amount
        self.acked = False
        self.direction = direction
        self.isConvert = isConvert
        if symbol not in p.positions:
          p.positions[symbol] = 0

    #p is portfolio
    def fill(self, fillAmount, p):
        if self.isConvert:
          return
        self.amount -= fillAmount
        if self.direction == "BUY":
            p.positions[self.symbol] += fillAmount
        else:
            p.positions[self.symbol] -= fillAmount
        if self.symbol not in p.symbolsToAmountTraded:
          p.symbolsToAmountTraded[self.symbol] = 0
        p.symbolsToAmountTraded[self.symbol] += fillAmount

class Portfolio():
    def __init__(self, exchange):
        #symbol to Position
        self.xlfguess = 0
        self.lastOrderTime = time.time()
        self.positions = {"GS": 0, "MS": 0, "WFC": 0, "XLF": 0, "VALE": 0, "VALBZ": 0}
        self.halfSpread = {"GS": 1, "MS": 1, "WFC": 1, "XLF": 6, "VALBZ": 5, "BOND": 1, "VALE": 5}
        self.nextOrderId = 0
    	#order ID to Order
        self.highestBuy = {'GS':0, 'MS':0, 'WFC':0, 'XLF':0, 'VALBZ':0, 'VALE':0, 'BOND':0}
        self.cheapestSell = {'GS':0, 'MS':0, 'WFC':0, 'XLF':0, 'VALBZ':0, 'VALE':0, 'BOND':0}
        self.orders = {}
        self.symbolToLimit = {'BOND':100, 'GS': 100, 'MS': 100, 'WFC': 100, 'XLF': 100, 'VALBZ': 10, 'VALE': 10}
        #self.avgSymbols = {"GS": AvgSymbol(), "MS": AvgSymbol(), "XLF": AvgSymbol(), "WFC": AvgSymbol(), "VALBZ": AvgSymbol()}
        self.theEquities = {"WFC","MS","GS"}
        self.exchange = exchange
        self.outstandingCancels = []
        self.symbolsToAmountTraded = {}

    #always return a positive number, clean up filled orders while at it
    def OutstandingOrders(self, symbol, direction):
        result = 0
        for orderId in self.orders:
            order = self.orders[orderId]
            if order.symbol == symbol and order.direction == direction:
              result += order.amount

        return result

    def waitUntilServerReady(self):
        while time.time() - self.lastOrderTime < 0.01:
          continue
        self.lastOrderTime = time.time()
        return
    
    def CancelObsoleteOrders(self, symbol, fair_price, halfSpread):
        for orderId in self.orders:
          if orderId in self.outstandingCancels : 
            continue
          order = self.orders[orderId]
          if order.symbol != symbol: 
            continue
          if order.direction == "BUY":
            order_price = order.price + halfSpread
          else:
            order_price = order.price - halfSpread
          if abs(fair_price - order_price) >= 2:
            json_string = '{"type": "cancel", "order_id": %s}' % orderId
            self.waitUntilServerReady()
            print(json_string, file=sys.stderr)
            print(json_string, file=self.exchange)
            self.outstandingCancels.append(orderId)

def connect(serv_addr):
    """returns (socket connection, s.makefile()"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect(("10.0.128.131", 25000))
    s.connect((serv_addr, 25000))
    return (s, s.makefile('w+', 1))

#BUY means you get XLF
def convertXLF(direction, amount, p, exchange):
    orderID = p.nextOrderId
    p.nextOrderId += 1
    json_string = '{"type": "convert", "order_id": %d' % orderID + ', "symbol": "XLF", "dir": "' + direction + '", "size": %s}' % str(amount)
    print(json_string, file=sys.stderr)
    p.waitUntilServerReady()
    print(json_string, file=exchange)   
    p.orders[orderID] = Order("XLF", -1, amount, direction, p, isConvert = True)
    if direction == "BUY":
      sign = +1
    else:
      sign = -1
    p.positions["XLF"] += sign * amount
    p.positions["BOND"] -= sign * 3* amount/10
    p.positions["GS"] -= sign * 2 * amount/10
    p.positions["MS"] -= sign * 3 * amount/10
    p.positions["WFC"] -= sign * 2 * amount/10
    


#direction is "BUY" or "SELL"
def orderSec(symbol, direction, price, amount, p, exchange):
    orderId = p.nextOrderId
    p.nextOrderId += 1
    json_string = '{"type": "add", "order_id": '+ str(orderId) + ',"symbol": "' + symbol +'", "dir": "' +  direction + '", "price": ' + str(price) + ', "size" : ' + str(amount) + '}'
    print(json_string, file=sys.stderr)
    p.waitUntilServerReady()
    print(json_string, file=exchange)   
    p.orders[orderId] = Order(symbol, price, amount, direction, p)

def tradeSymbol(symbol, exchange, fair_price, spread, p):
    buy = p.positions[symbol] + p.OutstandingOrders(symbol, "BUY")
    sell = -1 * p.positions[symbol] + p.OutstandingOrders(symbol, "SELL")
    symbolLimit = p.symbolToLimit[symbol] 

    if symbol in p.theEquities:
        buy_amount = 30 - buy
        sell_amount = 30 - sell
    else:
        buy_amount = symbolLimit - buy
        sell_amount = symbolLimit - sell
    
    buy_amount = symbolLimit - buy
    sell_amount = symbolLimit - sell
    
    if buy < symbolLimit and buy_amount > 0 :
        orderSec(symbol, "BUY", fair_price - spread, buy_amount, p, exchange)
    if sell < symbolLimit and sell_amount > 0:
        orderSec(symbol, "SELL", fair_price + spread, sell_amount, p, exchange)

def tradeBondDumbly(exchange):
    fair_price = 1000
    global p
    p.positions["BOND"] = 0
    #put in two orders for bonds
    orderSec("BOND", "BUY", fair_price -1 , 100, p, exchange)
    orderSec("BOND", "SELL", fair_price + 1, 100, p, exchange)
          

def parseData(msg, p):
    dat = json.loads(msg)
    if dat['type'] == "reject" and dat['error'] == "TRADING_CLOSED":
      sys.exit(2)
    elif dat['type'] == 'out':
        orderId = dat["order_id"]
        if orderId in p.outstandingCancels:
          p.outstandingCancels.remove(orderId)
          del p.orders[orderId]
    elif dat['type'] == "fill":
        order = p.orders[dat['order_id']]
        order.fill(dat['size'], p)
    elif dat['type'] == "trade" and dat['symbol'] not in ["BOND", "VALE"]:
        price = dat['price']
        size = dat['size']
        #updateFairPrice(dat['symbol'], price, size, p)
    elif dat['type'] == "book":
        sym = dat['symbol']
        sell = dat['sell']
        buy = dat['buy']
        cheapSell = 10000000
        highBuy = 0
        for (val, size) in sell:
            if val < cheapSell:
              cheapSell = val
        for (val, size) in buy:
            if val > highBuy:
              highBuy = val
        p.highestBuy[sym] = highBuy
        p.cheapestSell[sym] = cheapSell

    elif dat['type'] == "hello":
        syms = dat['symbols']
        for info in syms:
          theSym = info['symbol']
          position = info['position']
          p.positions[theSym] = position

def main():
    if len (sys.argv) != 2: 
      print ("feed server address as argument!")
      sys.exit(2)
    s, exchange = connect(sys.argv[1])
    json_string = '{"type": "hello", "team":"WESSEL"}'
    print(json_string, file=exchange)
    hello_from_exchange = exchange.readline().strip()
    print("The exchange replied: %s" % str(hello_from_exchange),file = sys.stderr)
    
    global p
    p = Portfolio(exchange)
    parseData(hello_from_exchange, p)

    print("entering main loop", file = sys.stderr)
   
    disableBOND = False
    disableVale = False
    disableXLF = False
    
    if not disableBOND:
        tradeBondDumbly(exchange) 
    
    while 1:
      if not disableBOND:
        tradeSymbol("BOND", exchange, 1000, p.halfSpread["BOND"], p)
      
      if not disableVale:
        if  p.highestBuy["VALBZ"] != 0 and p.cheapestSell["VALBZ"] !=0:
            price_VALE = int(round((p.highestBuy["VALBZ"] + p.cheapestSell["VALBZ"])/2.0))
            p.CancelObsoleteOrders("VALE", price_VALE, p.halfSpread["VALE"])
            tradeSymbol("VALE", exchange, price_VALE, p.halfSpread["VALE"], p)

      
      message = exchange.readline().strip()
      parseData(message, p)
      
      if not disableXLF: 
        if p.highestBuy['GS'] != 0 and p.cheapestSell['GS']!=0 and p.highestBuy['MS'] !=0 and p.cheapestSell['MS'] !=0 and p.highestBuy['WFC'] !=0 and p.cheapestSell['WFC'] !=0 and p.cheapestSell['XLF'] != 0 and p.highestBuy['XLF'] != 0:
          price_WFC = int(round((p.highestBuy['WFC']+  p.cheapestSell['WFC'])/2.0))
          price_MS = int(round((p.highestBuy['MS']+  p.cheapestSell['MS'])/2.0))
          price_XLF = int(round((p.highestBuy['XLF']+  p.cheapestSell['XLF'])/2.0))
          price_GS = int(round((p.highestBuy['GS']+  p.cheapestSell['GS'])/2.0))
          p.xlfguess = (3 * 1000 + 2 * price_GS + 3 * price_MS + 2 * price_WFC)
          p.xlfguess = int(round(p.xlfguess / 10.0))

          amount = 40

          longAmount  = p.positions["XLF"] + p.OutstandingOrders("XLF", "BUY")
          shortAmount = -1 * p.positions["XLF"] + p.OutstandingOrders("XLF", "SELL")

          if abs(p.xlfguess - price_XLF) > 100/amount + 10:
            
            if p.xlfguess < price_XLF:
              direction = "BUY"
            else:
              direction = "SELL"
            
            if (direction == "BUY" and amount + longAmount < 100) or (direction == "SELL" and amount + shortAmount < 100):
              netDirection = ("BUY" if direction == "SELL" else "SELL")
              orderSec("XLF", netDirection, price_XLF + p.halfSpread["XLF"], amount, p, exchange)
              orderSec("GS", direction, price_GS, amount/10 * 2, p, exchange)
              orderSec("MS", direction, price_MS, amount/10 * 3, p, exchange)
              orderSec("WFC", direction, price_WFC, amount/10 * 2, p, exchange)
             
              convertXLF(direction, amount, p, exchange)

              print("xlfguess: %d price_xlf: %d" % (p.xlfguess, price_XLF), file=sys.stderr)
          #p.CancelObsoleteOrders("XLF", p.xlfguess, p.halfSpread["XLF"])
          #tradeSymbol("XLF", exchange, p.xlfguess, p.halfSpread["XLF"], p)              

      if message is not None:
        #chuck away book messages for now
        m_type = json.loads(message)['type']
        if m_type == 'book' or m_type == 'trade' or m_type == 'ack':
          pass
        else:  
          print("> %s" % str (message), file =sys.stderr)
      # have we got a message ? 

if __name__ == "__main__":
    main()
