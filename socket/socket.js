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
var net = require('net'),
    JsonSocket = require('json-socket');
 
var port = 9838; //The same port that the server is listening on 
var host = '127.0.0.1';
var socket = new JsonSocket(new net.Socket()); //Decorate a standard net.Socket with JsonSocket 
socket.connect(port, host);
socket.on('connect', function() { //Don't send until we're connected 
    socket.sendMessage({a: 5, b: 7});
    socket.on('message', function(message) {
        console.log('The result is: '+message.result);
    });
});
