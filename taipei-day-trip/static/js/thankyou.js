const number = window.location.search.split('number=')[1];

async function getOrder(number){
    try{
        const OrderAPI = "/api/order/"+number;
        const response = await fetch(OrderAPI,{method: 'GET'});
        const data = await response.json();

        if(data.data == null){
            const noOrderSection = document.getElementById("no-order-section");
            noOrderSection.classList.remove("hide");
            return;
        }

        const orederNumSection = document.getElementById("ordernum-section");
        const orederNumText = document.getElementById("ordernum-text");
        orederNumText.innerHTML = data['data']['number'];
        orederNumSection.classList.remove("hide");

        if(data.data.status == 0){
            const payFailText = document.getElementById("pay-fail-text");
            payFailText.innerHTML = "由於卡片扣款失敗，請在七日內重新付款，"
        }

    } catch(error){
        console.log(error);
    }
}

getOrder(number);
