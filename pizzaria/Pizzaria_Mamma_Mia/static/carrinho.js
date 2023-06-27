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

function removeFromCart(url, data) {
    console.log(data);
    console.log(url);
    fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
        body: JSON.stringify(data)
    })
    .then(response => {
        // Avaliar a resposta do Django
        if (response.ok) {
            // Se a resposta estiver OK (código de status HTTP 200-299)
            location.reload(); // Recarregar a página
        } else {
            throw new Error("Erro na solicitação AJAX"); // Tratar erros, se necessário
        }
    })
    .then(data => {
        document.getElementById("num_of_items").innerHTML = data;
        console.log(data);
    })
    .catch(error => {
        console.log(error);
    });
}

// BOTÔES de romever item do carrinho
let removebtns = document.querySelectorAll(".btn-delete")

for(i=0;i < removebtns.length;i++){
    console.log(i + ': ' + removebtns[i].value)
}

removebtns.forEach(btn=>{
    btn.addEventListener("click", removeItemFromCart)
})

function removeItemFromCart(e){
    let product_content = e.target.value;
    content = product_content.split(";");
    let url = "remove_from_cart/"
    let data = {id:content[0], nome:content[1]};
    removeFromCart(url , data)
    
}
