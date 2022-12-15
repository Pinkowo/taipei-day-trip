// 判斷使用者是否為登入狀態
let isUserLogin = false;

// 按下預定行程按鈕但尚未登入，登入後自動跳轉 booking 頁
let goBooking = false;

// 預定行程
function bookTrip(){
    if(isUserLogin){
        location.href = "/booking";
    }else{
        goBooking = true;
        openModal();
    }
}

// 登入註冊 modal
// 開啟關閉
const modal = document.getElementById("modal");
const modalCross = document.getElementsByClassName("modal-cross");
const signInModal = document.getElementById("modal-signin");
const signUpModal = document.getElementById("modal-signup");
const scrollBarWidth = window.innerWidth - document.body.clientWidth;

function openModal(){
    modal.style.display = "block";
    // 隱藏滾動條
    document.body.style.overflow = "hidden";
    document.body.style.marginRight = scrollBarWidth + "px";
}
function closeModal(){
    modal.style.display = "none";
    // 開啟滾動條
    document.body.style.overflow = "auto";
    document.body.style.marginRight = 0;
    goBooking = false;
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
formHint = [signUpHint,signInHint];

function hint(form, msg, color="red"){
    formHint[form].style.color = color;
    formHint[form].innerHTML = msg;
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
            isUserLogin = true;
            if(goBooking){
                location.href = "/booking";
            }
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
            location.reload(true);
            
            //在 booking 頁登出時跳轉至首頁 
            if(location.pathname == "/booking"){
                location.href = "/";
            }
        }
        else if(data.error){
            print(data.error);
        }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

// 每次開啟頁面時檢查會員登入狀態
const AuthAPI = "/api/user/auth"
async function checkStatus(url){
    try{
        const response = await fetch(url,{method: 'GET'});
        const data = await response.json();
        if(data.data != null){
            btns[1].style.display = "none";
            btns[2].style.display = "inline-block";
            isUserLogin = true;

            if(location.pathname == "/booking"){
                document.getElementById('nickname').innerHTML = data.data['name'];
            }
        }
        else{
            btns[1].style.display = "inline-block";
            btns[2].style.display = "none";
            isUserLogin = false;
            
            if(location.pathname == "/booking"){
                location.href = "/";
            }
        }
    } catch(error){
        console.log(error);
    }
}

checkStatus(AuthAPI);
