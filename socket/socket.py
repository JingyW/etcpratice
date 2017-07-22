import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()
print "received data:", data

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


//pennying 1 buck lower than highestBuy and 1 buch higher than lowerst sell

class Portfolio():
    def _init_(self):
        self.positions = {};
        self.highestBuy = {};
        self.lowestSell = {};

if __name__ == "__main__":
    main()
