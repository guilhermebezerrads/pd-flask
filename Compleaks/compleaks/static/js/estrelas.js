function colorir(id, valor){
    id = parseInt(id);
    valor = parseInt(valor);

    stars = document.getElementsByClassName("star-"+id);
    
    if(stars[valor-1].name != "star"){
        for(i=0; i<=valor-1; i++){
            stars[i].name = "star";
        }
    }else{
        for(i=4; i>valor-1; i--){
            stars[i].name = "star-outline";
        }
    }

    pontua(id, valor);
    
}

function openAjax(){
var ajax = null;

try{
    ajax = new XMLHttpRequest;
}catch(erro){
    try{
        ajax = new ActiveXObject("Msxl2.XMLHTTP");
    }catch(er){
        try{
            ajax = new ActiveXObject("Microsoft.XMLHTTP");
        }catch(err){
            ajax = false;
        }
    }
}

return ajax;
}// Detecta dinamicamente o objeto XMLHttp (de acordo com o navegador)

function pontua(id, valor){
    if(document.getElementById){//Varifica se a funca ger funciona

        var ajax = openAjax();
        ajax.open("POST", "/arquivos/avaliar/"+id+"/"+valor, true);
        /*ajax.onreadystatechange = function(){
        
            if(ajax.readyState == 1){
               console.log('Carregando Resultados...');
            }

            if(ajax.readyState == 4){

            }else{
                alert("Erro ao carregar ---");
            }
        }*/

    }

    ajax.send(null);
}