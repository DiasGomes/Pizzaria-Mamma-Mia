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

// BOTÃO da pizza
let pizzasbtns = document.querySelector(".btn_pedido")

pizzasbtns.addEventListener("click", addPizzaToCart)

function addPizzaToCart(e){
    let url = "add_to_cart/";
    let tamanho = document.getElementById("tamanho-montar");
    let sabor1 = document.getElementById("primeiro-sabor-montar");
    let sabor2 = document.getElementById("segundo-sabor-montar");
    // coloca como default
    if(tamanho.value === ''){
        tamanho.value = 2;
    }
    if(sabor1.value === ''){
        sabor1.value = 4;
    }
    if(sabor2.value === ''){
        sabor2.value = 9;
    }
    let data = {nome:"pizza2sabores", sabor1:sabor1.value, sabor2:sabor2.value, tamanho: tamanho.value};
    addToCart(url , data);
}
