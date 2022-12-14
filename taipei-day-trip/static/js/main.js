let isLoading = false;

// 輸入框與景點列表
const searchList = document.getElementById("search-list");
const searchInput = document.getElementById("search-input");
const searchUl = searchList.getElementsByTagName('ul')[0];

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
            const content = `
                <li onclick="printCat(this)">${data.data[i]}</li>
            `
            searchUl.insertAdjacentHTML('beforeend',content);
        }
    })
    .catch(function(error){
        console.log(error);
    });

// 搜尋框串接 /api/attractions 搜尋關鍵字
const searchBtn = document.getElementById("search-btn");
const gridBox = document.getElementById("grid-box");
let keyword = searchInput.value;
let nextPage = 0;

searchBtn.addEventListener('click',function(){
    keyword = document.getElementById("search-input").value;
    nextPage = 0;
    observer.unobserve(target);
    gridBox.innerHTML = '';
    if(!isLoading){
        isLoading = true;
        getMoreData();
    }
    observer.observe(target);
});

// fetch 載入頁面
const loading = document.getElementById("loading");
const getMoreData =() => {
    loading.style.display = "flex";
    let url = "/api/attractions?page="+nextPage;
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
                const content = `
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
            loading.style.display = "none";
            isLoading = false;
        })
        .catch(function(error){
            console.log(error);
        });
}

// 呼叫後印出一張 card
async function printCard(data, i){
    if(data[i].mrt == null){
        data[i].mrt = data[i].name;
    }
    const content = `
        <div class="pre-card">
            <a class="clear" href="/attraction/${data[i].id}">
                <figure>
                    <img src=${data[i].images[0]} class="pre-img" alt="">
                    <figcaption>
                        ${data[i].name}
                    </figcaption>
                </figure>
                <div class="pre-intro">
                    <div>${data[i].mrt}</div>
                    <div>${data[i].category}</div>
                </div>
            </a>
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
        if(!isLoading){
            isLoading = true;
            getMoreData();
        }
    }
}
const observer = new IntersectionObserver(callback, options);
const target = document.querySelector('#footer');
observer.observe(target);
