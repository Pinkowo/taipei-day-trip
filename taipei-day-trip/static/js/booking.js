// 打開 booking 頁時抓取資料
const BookAPI = "/api/booking"
const token = document.cookie.split('=')[1];
async function getBookData(){
    try{
        const response = 
          await fetch(BookAPI,{
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token
            }
          });
        const data = await response.json();

        if(data.data == null) emptyCart();
        else printCart(data.data);
        
    } catch(error){
        console.log(error);
    }
}

getBookData();


// 根據資料印出頁面
const sections = document.getElementsByTagName("section");
const hrs = document.getElementsByTagName("hr");
const emptyText = document.getElementById("trip-hint");

function emptyCart(){
    for(let i=0;i<sections.length-1;i++){
        sections[i].classList.add("hide");
        hrs[i].classList.add("hide");
    }
    sections[3].classList.add("hide");
}

function printCart(data){
    emptyText.classList.add("hide");
    let totPrice = 0;
    for(let i=0;i<data.length;i++){
        totPrice += data[i].price;

        let tripTime;
        if(data[i].time == "morning"){
            tripTime = "早上 9 點到下午 4 點";
        }else if(data[i].time == "afternoon"){
            tripTime = "下午 4 點到晚上 9 點";
        }

        addCard(data[i],tripTime);
    }
    document.getElementById("total-price").innerHTML = totPrice;
}

function addCard(data,tripTime){
    const tripSection = document.getElementById("trip-section");
    const content = `
        <div class="trip-card">
            <div class="trip-intro">
                <img src=${data.attraction.image} alt="">
                <div class="trip-text">
                    <a href="#">台北一日遊：${data.attraction.name}</a>
                    <dl>
                        <dt>日期：</dt>
                        <dd>${data.date}</dd>
                        <dt>時間：</dt>
                        <dd>${tripTime}</dd>
                        <dt>費用：</dt>
                        <dd>新台幣 ${data.price} 元</dd>
                        <dt>地點：</dt>
                        <dd>${data.attraction.address}</dd>
                    </dl>
                </div>
            </div>
            <div class="trip-delete">
                <button class="delete-btn" onclick="deleteBook(${data.attraction.id})">
                    <img src="/static/images/icon/icon_delete.svg" alt="">
                </button>
            </div>
        </div>
    `
    tripSection.insertAdjacentHTML('afterbegin',content);
}


// 刪除預定行程
async function deleteBook(attId){
    try{
        const response = 
          await fetch(BookAPI,{
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({
                attractionId: attId,
            })
          });
        await response.json();

        location.reload(true);

    } catch(error){
        console.log(error);
    }
}