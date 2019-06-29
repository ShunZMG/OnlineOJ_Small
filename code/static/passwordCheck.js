//确认密码检测
function check(value) {
	correctPassword = document.getElementById("password").innerText;
	if (value != correctPassword) {
		document.getElementById("repasswordCheckBlock").innerText = "两次输入的密码不一致!";
	} else {
		document.getElementById("repasswordCheckBlock").innerText = "";
	}
}
