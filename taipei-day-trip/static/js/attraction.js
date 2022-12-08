// fetch 載入頁面
const id = location.href.split("attraction/")[1];
let slideIndex = 1;
let slides = [];
let dots = [];

const getData =() => {
  let url = "/api/attraction/"+id;
  fetch(url)
      .then(function(response){
          return response.json();
      })
      .then(function(data){
        const section = document.querySelector("section");
        if(data.error){
          section.innerHTML = "請重新輸入編號";
          section.classList.add("section-empty");
        }else{
          document.title = data.data.name;
          printHtml(data.data);
          if(data.data.images.length != 1){
            printSlides(data.data.images.length);
            showSlides(slideIndex);
          }
        }
      })
      .catch(function(error){
          console.log(error);
      });
}
window.addEventListener("load", getData, false);

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
    slideImg.src = images[i];
    slides.push(slideImg);
    slideDiv.appendChild(slideImg);
  }

  slideBox.appendChild(slideDiv);
}

// print right-box
const rightBox = document.getElementById("right-box");
function printForm(name, cat, mrt){
  let content = `
    <h3 class="fz-24 fw-700" style="text-align: left;">${name}</h3>
    <div class="intro">${cat} at ${mrt}</div>
  `
  rightBox.insertAdjacentHTML('afterbegin',content);
}

// print bottom
const bottom = document.getElementById("bottom");
function printBottom(description, address, transport){
  let content = `
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
  let arrow = `
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
function changePrice(price){
    let text = "新台幣 " + price + " 元";
    document.getElementById("price").innerHTML = text;
}

// datepicker 的 min 設置
const date = document.getElementById("tripDate");
date.min = new Date().toISOString().split("T")[0];
