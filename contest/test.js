var net = require("net");
// edge = dir_sign * (fair value - order price)
// where dir_sign = 1 for buying and -1 for selling

/*

symbol	limit
BOND	100
AAPL	100
MSFT	100
GOOG	100
XLK	100
NOKFH	10
NOKUS	10
*/

/*
The symbol XLK is an ETF. 10 shares of XLK can be converted to/from a basket of:

3 BOND
2 AAPL
3 MSFT
2 GOOG
*/
var client = new net.Socket();
var port = 25000;
var address = '10.0.214.108';

client.connect(port+'\n', address, function() {
	console.log('Connected');
  var helloMessage = '{"type": "hello", "team": "MOMOGOGO"}'
  console.log(helloMessage);
	client.write(helloMessage);
  console.log("after write")
});

client.on('data', function(data) {
	console.log('Received: ' + Object.keys(JSON.parse(data)));
});

client.on('close', function() {
	console.log('Connection closed');
});

//version2
// var client = net.connect({port: 8080}, function() {
//    console.log('connected to server!');
// });
