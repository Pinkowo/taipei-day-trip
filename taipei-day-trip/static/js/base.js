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
const scrollBarWidth = window.innerWidth - document.body.clientWidth;

function openModal(){
    modal.style.display = "block";
    // 隱藏滾動條
    document.body.style.overflow = "hidden";
    document.body.style.marginRight = scrollBarWidth + "px";
}
function closeModal(){
    switchModal(1);
    modal.style.display = "none";
    // 開啟滾動條
    document.body.style.overflow = "auto";
    document.body.style.marginRight = 0;
    // 判斷是否前往 Booking 頁(點擊預訂行程)
    if(goBooking && isUserLogin){
        location.href = "/booking";
    }
    goBooking = false;
}

window.addEventListener('click', function (e) {
    if(modal.style.display == "block"){
        if(e.target==modalCross[0]){
            closeModal();
        }else{
            openModal();
        }
    }
}, true);

// 切換
const signUpForm = document.getElementById("form-signup");
const signInForm = document.getElementById("form-signin");
const signInModal = document.getElementById("modal-signin");
const signUpModal = document.getElementById("modal-signup");
const successModal = document.getElementById("modal-success");
const bookSuccessModal = document.getElementById("modal-book-success");
const bookFailModal = document.getElementById("modal-book-fail");
const modals = [signInModal, signUpModal, successModal, bookSuccessModal, bookFailModal];

function switchModal(status = 0){
    switch (status){
        case 0: //註冊
            signInModal.style.display = 'none';
            signUpModal.style.display = 'block';
            hint('signIn', '');
            signInForm.reset();
            break;
        case 1: //登入
            signUpModal.style.display = 'none';
            signInModal.style.display = 'block';
            hint('signUp', '');
            signUpForm.reset();
            break;
        case 2: //登入成功
            signInModal.style.display = 'none';
            successModal.style.display = 'block';
            break;
        case 3: //預訂成功
            modals.forEach(function(modal) {
                modal.style.display = 'none';
            });
            bookSuccessModal.style.display = 'block';
            goBooking = true;
            break;
        case 4: //預訂失敗
            modals.forEach(function(modal) {
                modal.style.display = 'none';
            });
            bookFailModal.style.display = 'block';
            break;
    }
}


// 註冊登入表單 & 串接 API
const signUpHint = document.getElementById("hint-signup");
const signInHint = document.getElementById("hint-signin");
const formHint = {"signUp":signUpHint, "signIn":signInHint};

function hint(form, msg, color="red"){
    formHint[form].style.color = color;
    formHint[form].innerHTML = msg;
}


const UserAPI = "/api/user"
// 註冊
signUpForm.addEventListener('submit', (e)=>{
    e.preventDefault();
    signUp();
});

function signUp() { 
    fetch(UserAPI,{
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
            hint('signUp', '註冊成功', 'green');
        }
        else if(data.error){
            hint('signUp', data.message);
        }
    })
    .catch((error) => {
    console.error('Error:', error);
    });
}


const AuthAPI = "/api/user/auth"
// 登入
signInForm.addEventListener('submit', (e)=>{
    e.preventDefault();
    signIn();
});

const btns = document.getElementsByClassName('nav-btn');

function signIn() { 
    fetch(AuthAPI,{
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
            switchModal(2);
        }
        else if(data.error){
            hint('signIn', data.message);
        }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

// 登出
function logOut(){
    fetch(AuthAPI,{method: 'DELETE'})
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
async function checkStatus(){
    try{
        const response = await fetch(AuthAPI,{method: 'GET'});
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

checkStatus();
