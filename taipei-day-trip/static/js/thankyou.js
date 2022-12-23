const number = window.location.search.split('number=')[1];

async function getOrder(number){
    try{
        const OrderAPI = "/api/order/"+number;
        const response = await fetch(OrderAPI,{method: 'GET'});
        const data = await response.json();

        if(data.data != null){
            const orederNumSection = document.getElementById("ordernum-section");
            const orederNumText = document.getElementById("ordernum-text");
            orederNumText.innerHTML = data['data']['number'];
            orederNumSection.classList.remove("hide");
        }
        else{
            const noOrderSection = document.getElementById("no-order-section");
            noOrderSection.classList.remove("hide");
        }
    } catch(error){
        console.log(error);
    }
}

getOrder(number);
