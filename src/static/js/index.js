var BASE_URL_API = "http://127.0.0.1:5000/"
var xhr = new XMLHttpRequest()
var xhr2 = new XMLHttpRequest()
var xhr3 = new XMLHttpRequest()

var whenUserOut1 = document.getElementById('whenUserOut1')
var whenUserOut2 = document.getElementById('whenUserOut2')
var whenUserIn = document.getElementById('whenUserIn')
var container_main = document.getElementById('container_main')
var btnBuscar=document.getElementById("btnBuscar");
//btnBuscar.addEventListener("click",buscar);

window.onload = function () {
    xhr.onload=function(){
        text = xhr.responseText
        result = JSON.parse(text)
        //console.log(result.value)
        // existe un usuario en la sesion ???
        if (result.value == true) {
            console.log("TRUE")
            whenUserOut1.classList.add("hidden")
            whenUserOut2.classList.add("hidden")
            whenUserIn.classList.remove("hidden")
        } else {
            console.log("FALSE")
            whenUserOut1.classList.remove("hidden")
            whenUserOut2.classList.remove("hidden")
            whenUserIn.classList.add("hidden")
        }
    }
    url = BASE_URL_API+'ifUser'
    xhr.open('GET', url, true)
    xhr.send()

    xhr2.onload=function(){
        var preg = xhr2.responseText
        var result_preg = JSON.parse(preg)
        result_preg.reverse()
        //console.log(result_preg)
        if (result_preg.length > 0) {
            for(let i=0; i<result_preg.length;i++){
                var espacio = document.createElement("div")
                var titulo = document.createElement("h1")
                var detalle = document.createElement("p")
                var titulo_resp = document.createElement("h3")
                var lista_resp = document.createElement("ul")
                var btn_resp = document.createElement("a")
                
                xhr3.onload=function(){
                    resp = xhr3.responseText
                    result_resp = JSON.parse(resp)
                    //console.log(result_resp)
                    let respuestas = result_resp.filter(resp => resp.id_qn == result_preg[i].id); // return implicito
                    //console.log(respuestas);
    
                    for (let j = 0; j < respuestas.length; j++) {
                        var lista_item = document.createElement("li")
                        lista_item.textContent = respuestas[j].ans_detail
                        lista_item.classList.add('lead')

                        lista_resp.appendChild(lista_item)

                        if (respuestas[j].correct == 1) {
                            var btnCorrect = document.createElement("button")
                            btnCorrect.textContent = 'Correcto'
                            btnCorrect.classList.add("w-10", "mb-2", "btn", "btn-md", "btn-success")
                            lista_resp.appendChild(btnCorrect)
                        } else {
                            var form = document.createElement("form")
                            var btnWaiting = document.createElement("button")
                            form.setAttribute("method","POST")
                            form.setAttribute("action","/checkAnswer/"+respuestas[j].id)
                            btnWaiting.textContent = 'Necesita calificación'
                            btnWaiting.classList.add("w-10", "mb-2", "btn", "btn-md", "btn-outline-secondary")
                            form.appendChild(btnWaiting)
                            lista_resp.appendChild(form)
                        }

                        
                    }
                }
                url_resp = BASE_URL_API+'showAnswers'
                xhr3.open('GET', url_resp, false);
                xhr3.send();
    
                titulo.textContent = result_preg[i].qn_title
                detalle.textContent = result_preg[i].qn_detail
                titulo_resp.textContent = 'Respuestas'
                btn_resp.textContent = 'Responder'
    
                espacio.classList.add("mb-4", "bg-light", "p-5", "rounded")
                detalle.classList.add("lead")
                btn_resp.classList.add("btn","btn-lg","btn-primary")
                btn_resp.setAttribute("href","answer/"+result_preg[i].id)
    
                espacio.appendChild(titulo)
                espacio.appendChild(detalle)
                espacio.appendChild(titulo_resp)
                espacio.appendChild(lista_resp)
                espacio.appendChild(btn_resp)
    
                container_main.appendChild(espacio)
            }
        } else {
            var caja = document.createElement("div")
            var contenido = document.createElement("h1")
            contenido.textContent = 'No se han realizado preguntas todavía'
            caja.classList.add("mb-4", "bg-light", "p-5", "rounded")
            caja.appendChild(contenido)
            container_main.appendChild(caja)
        }
        
    }
    url_preg = BASE_URL_API+'showQuestions'
    xhr2.open('GET', url_preg, true)
    xhr2.send()
}

function buscar() {
    
    
    
}
