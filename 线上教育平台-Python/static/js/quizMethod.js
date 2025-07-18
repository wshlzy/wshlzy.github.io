function checkSelect(){
    var i,name,test,testName,total,check,j;

    for (i = 0; i < 5; i++) {
        name = "cQ" + i;
        testName = 'input[name="' + name + '"]';
        total = document.querySelectorAll(testName).length;
        test = document.getElementsByName(name);

        check = true;			
        for (j = 0; j < total && check; j++) {
            if (test[j].checked)
                check = false; 
        }

        if (check) {
            alert("For Question " + (i + 1) + ", You haven't chosen any choices yet.");
            return false;
        }
    }
    //If select an option
    var message = {
        type1: '',
        type2: '',
        type3: '',
        type4: '',
        type5: ''
    };
    var ansName,answer,deter,name,type;
    
    for(i = 0;i < 5;i++){
        ansName = "answer"+(i+1);
        answer = document.getElementsByName(ansName)[0].value;
        name = "cQ"+i;
        name = 'input[name="'+name+'"]:checked';
        deter = document.querySelector(name).value;
        type = "type"+(i+1);
        if(deter != answer){
            alert("Question "+(i+1)+" is wrong, right answer is: "+answer);
            message[type] = 'Y';
        }
    }
    window.parent.postMessage(message, '*');
    return true;
}

function hideButton(){
    var button = document.querySelector('submitButton');
    button.style.display = 'none';
}

function submitForm() {
    var form = document.getElementById("questionForm");
    var formData = new FormData(form);
    var i = 1;

    fetch('/submit_Question', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // 更新页面显示用户答案和正确答案
        var resultDiv;
        for (const [question, { selected, answer }] of Object.entries(data.answers)) {
            resultDiv = document.getElementById("result" + i);
            var p = document.createElement('p');
            p.textContent = `Your Answer: ${selected}; Right Answer: ${answer}`;
            resultDiv.appendChild(p);
            i++;
        }
        // 隐藏提交按钮
        hideButton();
    })
    .catch(error => console.error('Error:', error));
    
    // 阻止表单默认提交行为
    return false;
}