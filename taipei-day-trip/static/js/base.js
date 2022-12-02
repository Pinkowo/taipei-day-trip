// 登入註冊 modal

// 開啟關閉
let modal = document.getElementById("modal");
let modalCross = document.getElementsByClassName("modal-cross");

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
let signInModal = document.getElementById("modal-signin");
let signUpModal = document.getElementById("modal-signup");

function switchModal(status = 0){
    switch (status){
        case 0:
            signInModal.style.visibility = 'hidden';
            signUpModal.style.visibility = 'visible';
            break;
        case 1:
            signUpModal.style.visibility = 'hidden';
            signInModal.style.visibility = 'visible';
            break;
    }
}