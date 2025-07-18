function showAnswer(){
	var i,display,answer,deter,div,text,buttonA,buttonB;
				
	for(i = 0;i < 3;i++){
		display = document.querySelectorAll('div[style="display"]')[i];//找到随机显示的div
		answer = display.querySelector('input[type="hidden"]').value;//找到div内的answer

		if(display.querySelector('input[type="radio"]:checked'))//找到div内的选项
			deter = display.querySelector('input[type="radio"]:checked').value;//如果用户在div内选择了一个选项
		else
			deter = "";//如果用户未选择div内的任意选项
		
		div = document.createElement('div');//创建div element
		header = document.createElement('h1');//创建h1 element
		text = document.createTextNode("Your Answer: "+deter+"  Right Answer: "+answer);//创建文字 显示用户选择和答案
		br = document.createElement('br');//创建换行符
		header.appendChild(text);//将文字附加到h1中
		div.appendChild(header);//将h1附加到div中
		div.appendChild(br);//将换行符附加两次到div中
		div.appendChild(br);
		display.insertBefore(div,display.lastChild);//在display node中最后一个node前 插入 新创建的div
	}
	buttonA = document.querySelector('button[name="submit"]');//找到submit button
	buttonA.style.display = 'none';//设置为隐藏

	buttonB = document.querySelector('button[name="refresh"]');//找到refresh button，用以刷新页面
	buttonB.setAttribute('style','display');//设置为显示
}

function refresh(){
	location.reload();
}

function showup(){
	var i = 0;
	var j,rand,flag;
	var rand;
	var array = [];
	while(i < 3){
		rand = Math.floor(Math.random() * 10) + 1;
		for(j = flag = 0;j < array.length && flag != 1;j++){
			if(rand == array[j])
				flag = 1;
		}
		if(flag == 0){
			array.push(rand);
			var name = '#Q'+(rand);
			var test = document.querySelector(name);
			test.setAttribute('style','display');
			i++;
		}
	}
}