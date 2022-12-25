// fetch 載入頁面
const attId = location.href.split("attraction/")[1];
let slideIndex = 1;
let slides = [];
let dots = [];
let isLoaded = false;

async function getData(){
  try{
      const url = "/api/attraction/"+attId;
      const response = await fetch(url,{method: 'GET'});
      const data = await response.json();
      const section = document.querySelector("section");
        if(data.error){
          section.innerHTML = "請重新輸入編號";
          section.classList.add("section-empty");
        }else{
          document.title = data.data.name;
          printHtml(data.data);
          if(data.data.images.length != 1 && isLoaded){
            printSlides(data.data.images.length);
            showSlides(slideIndex);
          }
        }
    } catch(error){
      console.log(error);
  }
}

getData();

// html
const slideBox = document.getElementById("box-content");

function printHtml(data){
  if(data.mrt == null){
    data.mrt = data.name;
  }
  printImg(data.images);
  printForm(data.name, data.category, data.mrt);
  printBottom(data.description, data.address, data.transport);
}

// print top-box (img)
function printImg(images){
  const slideDiv = document.createElement("div");
  slideDiv.className = "slides";

  for(let i=0;i<images.length;i++){
    const slideImg = document.createElement("img");
    slideImg.onload = () => {
      slideDiv.appendChild(slideImg);
    }
    slideImg.src = images[i];
    slides.push(slideImg);
  }
  isLoaded = true;
  slideBox.appendChild(slideDiv);
}

// print right-box
const rightBox = document.getElementById("right-box");
function printForm(name, cat, mrt){
  const content = `
    <h3 class="fz-24 fw-700" style="text-align: left;">${name}</h3>
    <div class="intro">${cat} at ${mrt}</div>
  `
  rightBox.insertAdjacentHTML('afterbegin',content);
}

// print bottom
const bottom = document.getElementById("bottom");
function printBottom(description, address, transport){
  const content = `
    <div>
      <p>${description}</p>
    </div>
    <div>
      <div class="bottomTitle fw-700">景點地址：</div>
      <div>${address}</div>
    </div>
    <div>
      <div class="bottomTitle fw-700">交通方式：</div>
      <div>${transport}</div>
    </div>
  `
  bottom.insertAdjacentHTML('afterbegin',content);
}


// 印 slide 的箭頭和圓點
function printSlides(n){
  const arrow = `
    <a class="prev" onclick="plusSlides(-1)">
      <img src="/static/images/icon/btn_leftArrow.svg" alt="prev">
    </a>
    <a class="next" onclick="plusSlides(1)">
      <img src="/static/images/icon/btn_rightArrow.svg" alt="next">
    </a>
  `
  slideBox.insertAdjacentHTML('beforeend',arrow);

 const dotDiv = document.createElement("div");
  dotDiv.className = "dots";
  for(let i=0;i<n;i++){
    const dotBtn = document.createElement("button");
    dotBtn.className = "dotBtn";
    dotBtn.onclick = function(){currentSlide(i)};
    dots.push(dotBtn);
    dotDiv.appendChild(dotBtn);
  }
  slideBox.appendChild(dotDiv);
}

// 照片切換 slides
function plusSlides(n) {
    showSlides(slideIndex += n);
}

function showSlides(n) {
  let i;
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}


// radio 切換價格
let tripPrice = 2000;
function changePrice(price){
    const text = "新台幣 " + price + " 元";
    document.getElementById("price").innerHTML = text;
    tripPrice = price;
}

// datepicker 的 min 設置
const date = document.getElementById("tripDate");
date.min = new Date().toISOString().split("T")[0];


// 開始預約行程
const tripForm = document.getElementById("right-form");
tripForm.addEventListener('submit', (e)=>{
    e.preventDefault();

    const tripTime = document.querySelector('[name=time]:checked');
    const tripDate = tripForm[0].value;
    // 判斷使用者是否登入以及表單是否空白 
    if(isUserLogin){
      if(tripDate ==''){
        openModal();
        switchModal(2,"請填寫日期");
      }else if(tripTime==null){
        openModal();
        switchModal(2,"請填寫時間");
      }else{
        startBooking(tripTime.value, tripDate);
      }
    }else{
      openModal();
    }
});



async function startBooking(tripTime, tripDate){
    try{
        const BookAPI = "/api/booking"
        const response = 
          await fetch(BookAPI,{
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                attractionId: attId,
                date: tripDate,
                time: tripTime,
                price: tripPrice  
            })
          });
        const data = await response.json();
        if(data.ok){
          openModal();
          switchModal(2,"預定成功");
          goBooking = true;
        }else{
          openModal();
          switchModal(2,"預定失敗");
        }

    } catch(error){
        console.log(error);
    }
}
