const { WebSocketServer } = require('ws');
const http = require('http');
const express= require('express')
const cors = require('cors');
const app = express()
app.use(cors())
const server = http.createServer();
const wsServer = new WebSocketServer({ server });
const port = 8000;
var amqp = require('amqplib/callback_api');
var connection
var channel
amqp.connect('amqp://rabbitmq:5672', function(error0, conn) {
    if (error0) {
        throw error0;
    }
    console.log('connected to rabbitmq')
    connection=conn
    connection.createChannel(function(error1, ch) {
        if (error1) {
            throw error1;
        }
        channel=ch
        
    });
});
wsServer.on('connection',wsConn)

function wsConn(ws){
    console.log('Connection')
    ws.on('message',(res)=>{
        try {
            if(channel){
                var text = JSON.parse(res)
                //channel.prefetch(1, false);
                channel.assertQueue('', {
                    exclusive: true,
                    autoDelete:true
                }, function(error2, q) {
                    if (error2) {
                        throw error2;
                    }
                    var correlationId = generateUuid();
                    var ct= generateUuid()
                    channel.consume(q.queue,function(msg,err) {
                        
                        if (msg.properties.correlationId === correlationId) {
                            console.log('Ответ парсера: %s', msg.content.toString());
                            ws.send( msg.content.toString())
                        }
                    }, {
                        consumerTag:ct, 
                        noAck: true
                    });
                    channel.sendToQueue('pupupu',
                        Buffer.from(res), {
                            correlationId: correlationId,
                            replyTo: q.queue
                        });
                        
                });
            }else{
                ws.emit('err', 'error')
            }
        }catch(e){
            console.warn(e)
        }
    })
}

function generateUuid() {
    return Math.random().toString() +
           Math.random().toString() +
           Math.random().toString();
  }

app.use(express.static(__dirname));

app.get('/', (req, res) => res.render('index'));

app.listen(4000)
server.listen(port, () => {
    console.log(`WebSocket server is running on port ${port}`);
  });