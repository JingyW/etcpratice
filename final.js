var net = require("net");
var client = new net.Socket();
var port = 25000;
var address = '1.1.1.1';
var buyid = 0;
var sellid = 0;
var strid = 10;
//var portFolio={"GOOG":[0,0], "MSFT":[0,0],"AAPL":[0,0],"XLK":[0,0]};
var portFolio={"GOOG":[0,0], "MSFT":[0,0],"AAPL":[0,0],"XLK":[0,0],"NOKUS":[0,0], "NOKFH":[0,0]};
client.connect(port, address, function() {
        console.log('Connected');
  //var helloMessage = '{“type”: "hello","team":"MOMOGOGO"}\n'
  var helloAgain = '{"type":"hello","team":"MOMOGOGO"}\n';
  //var trybuy = '{"type": "add", "order_id": 2, "symbol": "BOND", "dir": "BUY", "price": 999, "size": 10}\n';
 // var trysell = '{"type": "add", "order_id": 3, "symbol": "BOND", "dir": "SELL", "price": 1001, "size": 10}\n'
  //var trybuy = '{“type”: “add”, “order_id”: 2, “symbol”: “BOND”, “dir”: BUY, “price”: 999, “size”: 10}\n'
  //var trysell = '{“type”: "sell", “order_id”: 3, “symbol”: “BOND”, “dir”: “SELL”, “price”: 1001, “size”: 10}\n'
  client.write(helloAgain);
  //client.write(trybuy);
 // client.write(trysell);
  console.log("after write")
});

client.on('data', function(data) {
var trybuy = '{"type": "add", "order_id": '+ buyid.toString()+', "symbol": "BOND", "dir": "BUY", "price": 999, "size": 100}\n';
  var trysell = '{"type": "add", "order_id": '+ sellid.toString() +', "symbol": "BOND", "dir": "SELL", "price": 1001, "size": 100}\n'
        client.write(trybuy);
        client.write(trysell);
        buyid++;
        sellid++;
    var strData = data.toString('utf-8')
if (strData.indexOf('"type":"book"') !== -1) {
        var buyIndex = strData.indexOf('"buy"');
        var sellIndex = strData.indexOf('"sell"');
        var symbolIndex = strData.indexOf('"symbol"');
        var company = strData.substring(symbolIndex+10,symbolIndex+14);
        if (company === 'XLK"') {
          var net = require("net");
var client = new net.Socket();
var port = 25000;
var address = '1.1.1.1';
var buyid = 0;
var sellid = 0;
var strid = 10;
//var portFolio={"GOOG":[0,0], "MSFT":[0,0],"AAPL":[0,0],"XLK":[0,0]};
var portFolio={"GOOG":[0,0], "MSFT":[0,0],"AAPL":[0,0],"XLK":[0,0],"NOKUS":[0,0], "NOKFH":[0,0]};
client.connect(port, address, function() {
        console.log('Connected');
  //var helloMessage = '{“type”: "hello","team":"MOMOGOGO"}\n'
  var helloAgain = '{"type":"hello","team":"MOMOGOGO"}\n';
  //var trybuy = '{"type": "add", "order_id": 2, "symbol": "BOND", "dir": "BUY", "price": 999, "size": 10}\n';
 // var trysell = '{"type": "add", "order_id": 3, "symbol": "BOND", "dir": "SELL", "price": 1001, "size": 10}\n'
  //var trybuy = '{“type”: “add”, “order_id”: 2, “symbol”: “BOND”, “dir”: BUY, “price”: 999, “size”: 10}\n'
  //var trysell = '{“type”: "sell", “order_id”: 3, “symbol”: “BOND”, “dir”: “SELL”, “price”: 1001, “size”: 10}\n'
  client.write(helloAgain);
  //client.write(trybuy);
 // client.write(trysell);
  console.log("after write")
});

client.on('data', function(data) {
var trybuy = '{"type": "add", "order_id": '+ buyid.toString()+', "symbol": "BOND", "dir": "BUY", "price": 999, "size": 100}\n';
  var trysell = '{"type": "add", "order_id": '+ sellid.toString() +', "symbol": "BOND", "dir": "SELL", "price": 1001, "size": 100}\n'
        client.write(trybuy);
        client.write(trysell);
        buyid++;
        sellid++;
    var strData = data.toString('utf-8')
if (strData.indexOf('"type":"book"') !== -1) {
        var buyIndex = strData.indexOf('"buy"');
        var sellIndex = strData.indexOf('"sell"');
        var symbolIndex = strData.indexOf('"symbol"');
        var company = strData.substring(symbolIndex+10,symbolIndex+14);
        if (company === 'XLK"') {
          company = "XLK";
         } else if (company === 'NOKU') {
           company = "NOKUS"
         } else if (company === 'NOKF') {
           company = "NOKFH"
         }
         console.log(company)
         var highestBuy = strData.substring(buyIndex+8,buyIndex+12)
         var lowestSell = strData.substring(sellIndex+9,sellIndex+13);
         if (portFolio[company]) {
             portFolio[company][0] = parseInt(highestBuy);
             portFolio[company][1] = parseInt(lowestSell);
             strategy2();
             strategy3();
         }
     }
 });


 function strategy2() {
    var rightSide = (2*(portFolio.AAPL[0] + portFolio.AAPL[1])/2 +
                    3*(portFolio.MSFT[0] + portFolio.MSFT[1])/2 +
                    2*(portFolio.GOOG[0] + portFolio.GOOG[1])/2 + 3000)/10
    console.log(rightSide);
    console.log(portFolio);
    if ( portFolio["XLK"][0] > rightSide) {
      var gap  = portFolio["XLK"][0] - rightSide;
      var size = 0;
      var selling = true;
      if ( gap > 9 ) {
        size = 100
      } else if (gap > 6) {
        size = 75
      } else if (gap > 3 ) {
        size = 50
      } else {
        selling = false;
      }
      if (selling) {
        var sell = '{"type":"add","order_id":'+ strid + ',"symbol":"XLK","dir":"SELL","price":' + portFolio["XLK"][0] + ',"size":'+size+'}\n'
        client.write(sell)
        console.log("---------------------------------------------SELLING XLK")
     }
    }
    if (portFolio["XLK"][1] < rightSide) {
          var gap  =  rightSide - portFolio["XLK"][1];
          var size = 0;
          var buying = true;
          if ( gap > 9) {
            size = 100
          } else if (gap >6) {
            size = 75
          } else if (gap > 3 ) {
            size = 50
          } else {
            buying = false;
          }
          if (buying) {
            var buy = '{"type":"add","order_id":'+ strid + ',"symbol":"XLK","dir":"BUY","price":' + portFolio["XLK"][1] + ',"size":'+size+'}\n'
            client.write(buy);
            console.log("*************************************BUYING XLK")
          }
        }
            strid++;
    }


function strategy3() {
  var rightSide = (portFolio.NOKFH[0] + portFolio.NOKFH[1])/2
  console.log(rightSide);
  console.log(portFolio);
  if ( portFolio["NOKUS"][0] > rightSide) {
    var sell = '{"type":"add","order_id":'+ strid + ',"symbol":"NOKUS","dir":"SELL","price":' + portFolio["NOKUS"][0] + ',"size":10}\n'
    var buy = '{"type":"add","order_id":'+ (strid+1) + ',"symbol":"NOKFH","dir":"BUY","price":' + portFolio["NOKFH"][1] + ',"size":10}\n'
    client.write(sell);
    client.write(buy);
    console.log("---------------------------------------------SELLING NO")
  }
  if ( portFolio["NOKUS"][1] < rightSide) {
    var buy = '{"type":"add","order_id":'+ strid + ',"symbol":"NOKUS","dir":"BUY","price":' + portFolio["NOKUS"][1] + ',"size":10}\n'
    var sell = '{"type":"add","order_id":'+ (strid+1) + ',"symbol":"NOKFH","dir":"SELL","price":' + portFolio["NOKFH"][0] + ',"size":10}\n'
    client.write(buy);
    client.write(sell);
    console.log("*************************************BUYING NO")
  }
  strid = strid+2;
}
client.on('close', function() {
        console.log('Connection closed');
});
