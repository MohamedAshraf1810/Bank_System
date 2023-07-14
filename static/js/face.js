var loader = document.getElementById("preloader");
var auth = document.getElementById("authbtn");



directionImg = document.getElementsByClassName("DirectionImg");
window.addEventListener("load" , function()
{
    setTimeout(() =>
    {
      loader.style.display="none";
    },1);
})


// Set constraints for the video stream
var constraints = { video: { facingMode: "user",advanced:[{zoom:150}] } , audio: false };

// Define constants
const cameraView = document.querySelector("#videoElement"),
    cameraOutput = document.querySelector("#camera--output"),
    cameraSensor = document.querySelector("#CANVAS"),
    cameraTrigger = document.querySelector("#facebtn")

// Access the device camera and stream to cameraView
function cameraStart() {
  navigator.mediaDevices
      .getUserMedia(constraints)
      .then(function(stream) {
      track = stream.getTracks()[0];
      cameraView.srcObject = stream;
  })
  .catch(function(error) {
      console.error("Oops. Something is broken.", error);
  });
}

var x = false;
count = 1
pic1 = document.getElementById("userPic1")
pic2 = document.getElementById("userPic2")
pic3 = document.getElementById("userPic3")
var shutterSound = document.getElementById("shutter_sound");
// Take a picture when cameraTrigger is tapped

var Positions = ["Front", "Left", "Right", "Up", "Down"];
var result = [];
while (result.length < 3) 
{
    var index = Math.floor(Math.random() * Positions.length);
    var selectedWord = Positions[index];
    // Add the selected Position to the result array
    result.push(selectedWord)
    // Remove the selected Position from the Positions array
    Positions.splice(index, 1);
}

mypos1 = result[0];
mypos2 = result[1];
mypos3 = result[2];


BaseURL_GIF = "http://192.168.1.5:5000/static/images/Assistant/GIF/"
BaseURL_STATIC = "http://192.168.1.5:5000/static/images/Assistant/ST/"

var ASSIST_URL = BaseURL_GIF + mypos1 + ".gif";
document.getElementById("DirectionImg").src=ASSIST_URL;


pic1.src = BaseURL_STATIC + mypos1 + ".jpg";
pic2.src = BaseURL_STATIC + mypos2 + ".jpg";
pic3.src = BaseURL_STATIC + mypos3 + ".jpg";








cameraTrigger.onclick = function()
{   
    shutterSound.play();
    cameraSensor.width = cameraView.videoWidth;
    cameraSensor.height = cameraView.videoHeight;
    cameraSensor.getContext("2d").drawImage(cameraView, 0, 0);
    myImage = cameraSensor.toDataURL("image/png");
    
    console.log(count);
    if (count == 1)
    {
        // alert("Fontal Face Captured Successfully !");
        UserPicture1 = pic1.src = myImage; // User picture 1 Is The Frontal Image
        console.log(document.getElementById("DirectionImg").src);
        document.getElementById("DirectionImg").src = BaseURL_GIF + mypos2 + ".gif"
        count++;
        posSPN.innerHTML = mypos2;
    }
    else if (count == 2)
    {
        // alert("Right Face Captured Successfully !");
        UserPicture2 = pic2.src = myImage; // User picture 2 Is The Right Image
        document.getElementById("userPic2").style.transform = "rotateY(180deg)";
        document.getElementById("DirectionImg").src = BaseURL_GIF + mypos3 + ".gif"
        count++;
        posSPN.innerHTML = mypos3;
    }
    else if (count == 3)
    {
        UserPicture3 = pic3.src = myImage; // User picture 3 Is The Left Image
        document.getElementById("authenticationLoader").setAttribute('style','display:flex;');
        document.getElementById("userPic3").style.transform = "rotateY(180deg)";
        var xhr = new XMLHttpRequest();
        xhr.open('POST','/uploadimage',true);
        xhr.setRequestHeader('Content-Type','application/json');
        setTimeout(() =>
        {
            xhr.onload = () => 
            {
                MyResponse = xhr.response;
                console.log( "My_Response is : ",MyResponse);
                console.log("type of my response ",typeof (MyResponse));
                console.log("***********************");
        
                if (MyResponse == 'True')
                {
                    console.log("Type ",typeof(MyResponse));
                    console.log("Tmaam Response :",MyResponse);
                    window.open("http://192.168.1.5:5000/voiceAuth",'_self')
                }
                else
                {
                    console.log("Type ",typeof(MyResponse));
                    console.log("Me4 Tmaam response :",MyResponse);
                    window.open("http://192.168.1.5:5000/login",'_self')
                }
        
            };
            xhr.send(JSON.stringify(
            {
                USER_CAP1 : UserPicture1,
                USER_CAP2 : UserPicture2,
                USER_CAP3 : UserPicture3,
                pos1 : mypos1,
                pos2 : mypos2,
                pos3 : mypos3,
            }))
        },500);

    }     
};

// Start the video stream when the window loads
window.addEventListener("load", cameraStart, false);

