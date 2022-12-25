TPDirect.setupSDK(126856, 'app_hWqtBTqzjv2x9jBafED3i1QOF7bPxlrtTyzUEuElJEZHhuHqvBl2M361QBTY', 'sandbox');

// 信用卡 form 的 style，包含限制純數字等
let fields = {
    number: {
        element: '#card-number',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        element: '#card-expiration-date',
        placeholder: 'MM / YY'
    },
    ccv: {
        element: '#card-ccv',
        placeholder: 'ccv'
    }
}

TPDirect.card.setup({
    fields: fields,
    styles: {
        'input': {
            'color': 'gray'
        },
        '.valid': {
            'color': 'green'
        },
        '.invalid': {
            'color': 'red'
        }
    },
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 0,
        endIndex: 11
    }
})

const orderBtn = document.getElementById("total-btn");
orderBtn.addEventListener('click', (e)=>{
    const orderName = document.getElementById('contact-name').value;
    const orderEmail = document.getElementById('contact-email').value;
    const orderPhone = document.getElementById('contact-phone').value;

    const checkStatus = checkForm(orderName,orderEmail,orderPhone);

    if(checkStatus){
        getPrime(orderName,orderEmail,orderPhone);
    }
});

// 確認表單格式是否正確
function checkForm(orderName,orderEmail,orderPhone){
    const emailRegExp = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
    const phoneRegExp = /^09\d{8}$/;

    if(orderName == ''){
        openModal();
        switchModal(2,"請輸入聯絡姓名");
    }else if(orderEmail == ''){
        openModal();
        switchModal(2,"請輸入連絡信箱");
    }else if(orderPhone == ''){
        openModal();
        switchModal(2,"請輸入手機號碼");
    }else if(!emailRegExp.test(orderEmail)){
        openModal();
        switchModal(2,"請輸入正確的連絡信箱");
    }else if(!phoneRegExp.test(orderPhone)){
        openModal();
        switchModal(2,"請輸入正確的手機號碼");
    }else{
        return true;
    }
}

// 取得 prime 並跳轉
function getPrime(orderName,orderEmail,orderPhone) {
    const tappayStatus = TPDirect.card.getTappayFieldsStatus();

    if (tappayStatus.canGetPrime === false){
        openModal();
        switchModal(2,"訂購失敗，請確認是否填寫完整");
        return;
    }

    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            openModal();
            switchModal(2,"訂購失敗，"+ result.msg);
            return;
        }      
        const prime = result.card.prime;
        postOrder(prime,orderName,orderEmail,orderPhone);
        openModal();
        switchModal(2,"訂購成功，兩秒後網頁自動跳轉");
    })
}

// 建立訂單
async function postOrder(prime,orderName,orderEmail,orderPhone){
    try{
        const OrdersAPI = "/api/orders"
        const response = 
          await fetch(OrdersAPI,{
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prime: prime,
                name: orderName,
                email: orderEmail,
                phone: orderPhone
            })
          });
        const data = await response.json();

        setTimeout(function(){
            location.href = "/thankyou?number=" + data['data']['number'];
        },2000);
        
    } catch(error){
        console.log(error);
    }
}