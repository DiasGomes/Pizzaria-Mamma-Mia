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

function removeFromCart(url, data){
    console.log(data)
    console.log(url)
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
