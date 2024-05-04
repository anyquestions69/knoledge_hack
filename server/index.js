const { WebSocketServer } = require('ws');
const http = require('http');
const express= require('express')
const app = express()
const server = http.createServer();
const wsServer = new WebSocketServer({ server });
const port = 8000;
var amqp = require('amqplib/callback_api');
var connection
var channel

wsServer.on('connection',wsConn)

function wsConn(ws){
    ws.on('message',(message)=>{
        try {
            const jsonMessage = JSON.parse(message);
            console.log(jsonMessage.text)
            ws.send('hi')
        }catch(e){
            console.warn(e)
        }
    })
}
app.use(express.static(__dirname));

app.get('/', (req, res) => res.render('index'));

app.listen(3000)
server.listen(port, () => {
    console.log(`WebSocket server is running on port ${port}`);
  });