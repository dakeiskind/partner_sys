function processNetError(data, str) {
	alert(data.status);
	switch (data.status) {
		case 500:
			if (data.responseJSON.code == "300") {
				alert("请联系系统支持人员");
			} else if (data.responseJSON.code == "100") {
				alert(data.responseJSON.message);
			};
			break;
		case 0:
			alert("网络连接故障,请检查网络连接是否正常");
			break;
		case 404:
			alert("当前访问地址不存在");
			break;
		case 408:
			alert("网络连接失败，请检查网络连接是否正常");
			break;
		case 401:
			window.location.href = 'login.html';
			break;
		default:
			alert("请联系系统支持人员");
			break;
	};
}