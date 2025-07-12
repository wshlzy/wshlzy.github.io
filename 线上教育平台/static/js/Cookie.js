/*Cookie part*/
// function setCookie(name, value, days) {
	// var expires = "";
	// if (days) {
		// var date = new Date();
		// date.setTime(date.getTime() + (days*24*60*60*1000) - (8*60*60*1000));
		// expires = "; expires=" + date.toUTCString();
	// }
	
	// document.cookie = name + "=" + (value || "")  + expires + "; path=/Music_Web0531/Music_Web/";
// }

// function createCookie(createKey1,createKey2) {
	// var user = document.getElementById("account").value;
	// var pass = document.getElementById("pass").value;
	// if(user != ""&&user != null){
		// setCookie(createKey1,user,7);
	// }
	// if(pass != ""&&pass != null){
		// setCookie(createKey2,pass,7);
	// }
// }

function getCookie(name) {
	var nameE = name + "=";
	var ca = document.cookie.split(';');
	for (var i = 0; i < ca.length; i++) {
		var c = ca[i];
		
		if (c.indexOf(nameE) == 0) 
			return c.substring(nameE.length, c.length);
	}
	return null;
}

function checkCookie(checkKey) {
	var checkValue = getCookie(checkKey);
	if (checkValue != null) {
		document.getElementById("cookie").value = checkValue;
	} else {
		document.getElementById("cookie").value = "";
	}
}

function checkLogin(logKey1,logKey2,status){
	var singleSign = getCookie(status);
	if(singleSign != 0){
		var account = getCookie(logKey1);
		var pass = getCookie(logKey2);
		document.getElementById("account").value = account;
		document.getElementById("pass").value = pass;
	}else{
		document.getElementById("account").value = "";
		document.getElementById("pass").value = "";
	}
}

function createHistory(){
	var history = document.getElementById("history").src;
	setcookie();
}

function checkHistory(){
	
}


/*Link part*/
function returnLog() {
	parent.location.href = 'Login.html';
}

function sreturnLog() {
	parent.location.href = '../Login.html';
}

function returnUpload() {
	parent.location.href = 'PHP/insertScore.php';
}

function sreturnUpload() {
	parent.location.href = '../PHP/insertScore.php';
}

function lreturnUpload() {
	parent.location.href = 'insertScore.php';
}


/*Pass to PHP part*/
function sendButtonValue() {
	var button = getCookie("ID");
	document.getElementById("hiddenInput").value = button;
		
	document.getElementById("Cancel").submit();
}

function returnDownload(){
	var image = document.getElementById("image").value;
	var name = document.getElementById("scoreTitle").innerHTML;
	document.getElementById("download-button").value = image;
	document.getElementById("hiddenInputDownload").value = name;
}
	
	
	
	
	

    
	



    