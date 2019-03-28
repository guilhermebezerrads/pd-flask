function formulario_editar_comentario(elemento1){
    var display1 = document.getElementById(elemento1).style.display;
    if(display1 == "none"){
        document.getElementById(elemento1).style.display = 'block';
    }else{
        document.getElementById(elemento1).style.display = 'none';
    }  
}

function responder_comentario(elemento1){
    var display1 = document.getElementById(elemento1).style.display;

    if(display1 == "none"){
        document.getElementById(elemento1).style.display = 'block';
    }else{
        document.getElementById(elemento1).style.display = 'none';
    }

}

function editar_resposta(elemento1){
    var display1 = document.getElementById(elemento1).style.display;

    if(display1 == "none"){
        document.getElementById(elemento1).style.display = 'block';
    }else{
        document.getElementById(elemento1).style.display = 'none';
    }

}