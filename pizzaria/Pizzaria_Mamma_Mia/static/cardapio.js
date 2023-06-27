function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function addToCart(url, data){
    fetch(url, {
        method: "POST",
        headers: {"Content-Type":"application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(data=>{
        document.getElementById("num_of_items").innerHTML = data
        console.log(data)
    })
    .catch(error=>{
        console.log(error)
    })
}

// BOTÔES da pizza
let pizzasbtns = document.querySelectorAll(".pizzas-cardapio button")

pizzasbtns.forEach(btn=>{
    btn.addEventListener("click", addPizzaToCart)
})

function addPizzaToCart(e){
    let product_id = e.target.value
    let url = "add_to_cart/"
    let tamanho = document.getElementById("tamanho-pizza"+ product_id)
    if(tamanho.value === ''){
        tamanho.value = 2
    }
    let data = {id:product_id, nome:"pizza", tamanho: tamanho.value}
    addToCart(url , data)
    
}

// BOTÔES das bebidas
let bebidasbtns = document.querySelectorAll(".bebidas-cardapio button")

bebidasbtns.forEach(btn=>{
    btn.addEventListener("click", addBebidaToCart)
})

function addBebidaToCart(e){
    let product_id = e.target.value
    let url = "add_to_cart/"
    let data = {id:product_id, nome:"bebida"}
    
    addToCart(url , data)
    
}

// BOTÔES de combos
let combosbtns = document.querySelectorAll(".combos-cardapio button")

combosbtns.forEach(btn=>{
    btn.addEventListener("click", addComboToCart)
})

function addComboToCart(e){
    let product_id = e.target.value
    let url = "add_to_cart/"
    let data = {id:product_id, nome:"combo"}
    addToCart(url , data)
    
}

// ABAS
function openTab(tabId, abaId) {
    // Esconder todo o conteúdo das abas
    var tabContents = document.getElementsByClassName('tab-content');
    for (var i = 0; i < tabContents.length; i++) {
      tabContents[i].classList.remove('active');
    }
    
    // Mostrar o conteúdo da aba selecionada
    var selectedTab = document.getElementById(tabId);
    selectedTab.classList.add('active');

    // Esconder todo o conteúdo das abas
    var tabContents = document.getElementsByClassName('aba-option');
    for (var i = 0; i < tabContents.length; i++) {
      tabContents[i].classList.remove('active');
    }
    
    // Mostrar o conteúdo da aba selecionada
    var selectedTab = document.getElementById(abaId);
    selectedTab.classList.add('active');

  }