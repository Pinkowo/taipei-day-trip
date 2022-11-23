// 輸入框與景點列表
let searchList = document.getElementById("search-list");
let searchInput = document.getElementById("search-input");
let searchUl = searchList.getElementsByTagName('ul')[0];

function showList(){
    searchList.classList.remove("hide");
}
function hideList(){
    searchList.classList.add("hide");
}

window.addEventListener('click', function (e) {
    if(e.target==searchUl){
        showList();
    }else if(e.target==searchInput){
        showList();
    }else{
        hideList();
    }
}, true);

function printCat(cat){
    document.getElementById("search-input").value = cat.innerHTML;
    hideList();
}

// 用/api/categories 載入所有景點分類
fetch("/api/categories")
    .then(function(response){
        return response.json();
    })
    .then(function(data){
        for(let i=0;i<data.data.length;i++){
            let content = `
                <li onclick="printCat(this)">${data.data[i]}</li>
            `
            searchUl.insertAdjacentHTML('beforeend',content);
        }
    })
    .catch(function(error){
        console.log(error);
    });

// 搜尋框串接 /api/attractions 搜尋關鍵字
let searchBtn = document.getElementById("search-btn");
let keyword = searchInput.value;
let nextPage = 0;
let gridBox = document.getElementById("grid-box");

searchBtn.addEventListener('click',function(){
    keyword = document.getElementById("search-input").value;
    nextPage = 0;
    observer.unobserve(target);
    gridBox.innerHTML = '';
    debounceGet();
    observer.observe(target);
});

// fetch 載入頁面
const getMoreData =() => {
    url = "/api/attractions?page="+nextPage;
    if(keyword != ''){
        url = "/api/attractions?page="+nextPage+"&keyword="+keyword;
    }
    fetch(url)
        .then(function(response){
            return response.json();
        })
        .then(function(data){
            if(data.data.length == 0){
                observer.unobserve(target);
                let content = `
                    <div class="centerText">
                        查無相關景點
                    </div>
                    `
                gridBox.insertAdjacentHTML('beforeend',content);
            }
            else{
                nextPage = data.nextPage; 
                if(nextPage == null){
                    observer.unobserve(target);
                }
                for(let i=0;i<data.data.length;i++){
                    printCard(data.data,i);
                }
            }
        })
        .catch(function(error){
            console.log(error);
        });
}

// 呼叫後印出一張 card
function printCard(data, i){
    if(data[i].mrt == null){
        data[i].mrt = data[i].name;
    }
    let content = `
        <div class="pre-card">
            <figure>
                <img src=${data[i].images[0]} alt="">
                <figcaption>
                    ${data[i].name}
                </figcaption>
            </figure>
            <div class="pre-intro">
                <div>${data[i].mrt}</div>
                <div>${data[i].category}</div>
            </div>
        </div>
        `
    gridBox.insertAdjacentHTML('beforeend',content);
}

// IntersectionObserver ⾃動載入後續⾴⾯
const options = {
    root: null,
    rootMargin: '104px',
    threshold: 1
};
function callback(entries, observer){
    if(entries[0].intersectionRatio == 1){
        debounceGet();
    }
}
const observer = new IntersectionObserver(callback, options);
const target = document.querySelector('#footer');
observer.observe(target);

// 防抖
function debounce(fun, delay) {
    return function (args) {
        let that = this;
        let _args = args;
        clearTimeout(fun.time);
        fun.time = setTimeout(function () {
            fun.call(that, _args);
        }, delay);
    }
}
let debounceGet = debounce(getMoreData, 500);