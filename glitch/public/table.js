var json = "https://productive-rayon.glitch.me/json";
var io = io();

$(function(){
  $.getJSON(json, function(d){ initTable(d) });
  socketio();
});

function initTable(d) {
  //addCaption(d);
  d.forEach(function(a){
    addToTable(a);
  });
}
//入力の順番で表組みができない
function socketio(){
  io.on('data',function(d){
    //console.log(d);
    addToTable(d);
    //addCaption([d]);
  });
}

function addToTable(d) {
  var text = '<tr>' 
             + '<td class="sheet">' + d.q_sheet + '</td>'
             + '<td class="question">' + d.q_number + '</td>'
             + '<td class="answer">' + d.answer + '</td>'
             + '<td class="time">' + d.time + '</td>'
           + '</tr>';
  var t_id = 'table#table' + Number(d.keyboard_id) + ' tbody';
  $(t_id ).prepend(text);
}

function addCaption(d) {
  var a = unique(d, 'keyboard_id').sort();
  a.forEach(function(x){
    var t_id = 'table#table' + Number(x);
    if($(t_id))
      $(t_id+' caption').text('user'+x); 
  });
}

function shapingData(data) {
  var array = unique(data, 'keyboard_id');
  var shaping = [];
  for(var n of array) {
    shaping.push(
      data.filter( function(e, i, a){
        return e.keyboard_id == n;
      })
    );
  }
  return shaping
}

function unique(a, k) {
  return a.map(function(e, i) {
    return e[k];
  }).filter(function(e, i, a) {
    return a.indexOf(e) === i;
  });
}
