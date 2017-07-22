//version 1
var net = require("net");

var client = new net.Socket();
var port = 1337;
var ip  = '127.0.0.1';

var portfolio = {
  highestBuy:{},
  lowestSell:{},
  orderId:'',
  positions:{}
};

client.connect(port, ip, function() {
	console.log('Connected');
	client.write('Hello, server! Love, Client.');
});

client.on('data', function(data) {
	console.log('Received: ' + data);
});

client.on('close', function() {
	console.log('Connection closed');
});

//version2
var client = net.connect({port: 8080}, function() {
   console.log('connected to server!');
});

client.on('data', function(data) {
   console.log(data.toString());
});

client.write({})
client.on('end', function() {
   console.log('disconnected from server');
});
https://www.npmjs.com/package/json-socket
