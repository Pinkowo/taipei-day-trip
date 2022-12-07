// 登入註冊 modal
// 開啟關閉
const modal = document.getElementById("modal");
const modalCross = document.getElementsByClassName("modal-cross");

function openModal(){
    modal.style.display = "block";
}
function closeModal(){
    modal.style.display = "none";
}

window.addEventListener('click', function (e) {
    if(modal.style.display == "block"){
        if(e.target==modalCross[0] || e.target==modalCross[1]){
            closeModal();
        }else{
            openModal();
        }
    }
}, true);

// 切換
const signInModal = document.getElementById("modal-signin");
const signUpModal = document.getElementById("modal-signup");

function switchModal(status = 0){
    switch (status){
        case 0:
            signInModal.style.display = 'none';
            signUpModal.style.display = 'block';
            break;
        case 1:
            signUpModal.style.display = 'none';
            signInModal.style.display = 'block';
            break;
    }
}


// 註冊登入表單 & 串接 API
// 文字提示 0=signUpHint 1=signInHint
const signUpHint = document.getElementById("hint-signup");
const signInHint = document.getElementById("hint-signin");
formArray = [signUpHint,signInHint];

function hint(form, msg, color="red"){
    formArray[form].style.color = color;
    formArray[form].innerHTML = msg;
}

// 註冊
const signUpForm = document.getElementById("form-signup");
signUpForm.addEventListener('submit', (e)=>{
    e.preventDefault();
    signUp();
});

function signUp() { 
    fetch("/api/user",{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: signUpForm[0].value,
            email: signUpForm[1].value,
            password: signUpForm[2].value
        })
    })
    .then((response) => response.json())
    .then((data) => {
        if(data.ok){
            hint(0, '註冊成功', 'green');
        }
        else if(data.error){
            hint(0, data.message);
        }
    })
    .catch((error) => {
    console.error('Error:', error);
    });
}

// 登入
const signInForm = document.getElementById("form-signin");
signInForm.addEventListener('submit', (e)=>{
    e.preventDefault();
    signIn();
});

const btns = document.getElementsByClassName('nav-btn');

function signIn() { 
    fetch("/api/user/auth",{
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: signInForm[0].value,
            password: signInForm[1].value
        })
    })
    .then((response) => response.json())
    .then((data) => {
        if(data.ok){
            btns[1].style.display = "none";
            btns[2].style.display = "inline-block";
            closeModal();
        }
        else if(data.error){
            hint(1, data.message);
        }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

// 登出
function logOut(){
    fetch("/api/user/auth",{method: 'DELETE'})
    .then((response) => response.json())
    .then((data) => {
        if(data.ok){
            btns[1].style.display = "inline-block";
            btns[2].style.display = "none";
            resetForm();
        }
        else if(data.error){
            print(data.error);
        }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function resetForm(){
    formArray[0].innerHTML = '';
    formArray[1].innerHTML = '';
    signUpForm.reset();
    signInForm.reset();
}

// 檢查會員登入狀態
fetch("/api/user/auth",{method: 'GET'})
    .then((response) => response.json())
    .then((data) => {
        if(data.data == null){
            btns[1].style.display = "inline-block";
            btns[2].style.display = "none";
        }
        else{
            btns[1].style.display = "none";
            btns[2].style.display = "inline-block";
        }
    })
    .catch((error) => {
      console.error('Error:', error);
    });