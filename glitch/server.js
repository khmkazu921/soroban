const fs = require('fs');
var express = require('express');
var app = express();
var http = require('http').Server(app);
const io = require('socket.io')(http);
const PORT = process.env.PORT || 7000;
var bodyParser = require('body-parser');
var database = __dirname + '/data.json';
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

io.on('connection', function(socket){
  console.log('socket.io connected');
});

var originData = JSON.parse(fs.readFileSync(database, 'utf8'));

app.post('/', function(req, res) {
  var data = req.body;
  io.emit('data', data);
  res.send("sent");
  originData.push(data);
  console.log(originData);
  var text = JSON.stringify(originData);
  fs.writeFile(database, text, 'utf8',
               function(err) {if(err)console.log(err);});
});

app.set("view engine", "ejs");

app.use(express.static(__dirname + '/public'));

app.get('/' , function(req, res){
  res.render('index');
});

app.get('/json' , function(req, res){
  res.sendFile(__dirname + '/data.json');
});

http.listen(PORT, function(){
  console.log('server listening. Port:' + PORT);
});

