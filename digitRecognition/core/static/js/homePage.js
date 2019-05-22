var canvas = document.getElementById('canvas');
var ctx = canvas.getContext("2d");
var paths = [[]];
var isMouseDown = false;

function handleMouseMove(e){
  if(isMouseDown){
    var mouseX = parseInt(e.clientX - e.target.offsetLeft);
    var mouseY = parseInt(e.clientY - e.target.offsetTop);
    paths[paths.length - 1].push([mouseX, mouseY]);
    
    for (var path of paths) {
      ctx.beginPath();
      ctx.moveTo(path[0][0], path[0][1]);
      for (let i = 1, imax = path.length; i < imax; i++) {
        ctx.lineTo(path[i][0], path[i][1]);
      }
      ctx.stroke();
    }
  }
}

function handleMouseDown(e){
  isMouseDown = true;
}


function stopDraw(e){
  if(isMouseDown){
    isMouseDown = false;
    let lastPath = paths[paths.length - 1];
    if (lastPath.length > 1) {
      paths.push([]);
    } else {
      lastPath.length = 0;
    }
  }
}

function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.beginPath();
  paths = [[]];
   $("#result").html('')
}

ctx.strokeStyle = 'black';
ctx.lineWidth = 20;
ctx.lineJoin = ctx.lineCap = 'round';

canvas.addEventListener('mousedown', function(e){handleMouseDown(e);});
canvas.addEventListener('mousemove', function(e){handleMouseMove(e);});
canvas.addEventListener('mouseup', function(e){stopDraw(e);});
canvas.addEventListener('mouseout', function(e){stopDraw(e);});

function loadImage(){
    if (paths.length == 1) {
      showErrorAlert("Image doesn't contain any digit")
    } else {
      data = {};
      data.image = canvas.toDataURL("image/png",1.0)
                       .replace('data:image/png;base64,', '');
    $.ajax({
      url: "/recognizer/image",
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify(data),
      success: function(response) {
        printNumber(response);
      },
      error: function(response) {
        if(response.responseText !== undefined) {
          showErrorAlert(response.responseText);
        } else {
          showErrorAlert("Inner server error");
        }
      }
    })
  }
}

function printNumber(response) {
  if(response.status == 'success') {
    $("#result").html(response.digit);
  } else {
    showErrorAlert(response.responseText);
  }
}

function showErrorAlert(message) {
  $(".alert-danger").html(message);
  $(".alert-danger").fadeTo(2000, 500).slideUp(500, function(){
    $(".alert-danger").slideUp(500);
  });
}