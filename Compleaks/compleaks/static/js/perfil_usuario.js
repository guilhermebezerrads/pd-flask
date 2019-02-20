function formulario_email(elemento){
    var display = document.getElementById(elemento).style.display;
    if(display == "none"){
        document.getElementById(elemento).style.display = 'block';
    }else{
        document.getElementById(elemento).style.display = 'none';
    }  
}

function formulario_email_cancelar(elemento){
    var display = document.getElementById(elemento).style.display;
    document.getElementById(elemento).style.display = 'none';
}

function formulario_senha(elemento){
    var display = document.getElementById(elemento).style.display;
    if(display == "none"){
        document.getElementById(elemento).style.display = 'block';
    }else{
        document.getElementById(elemento).style.display = 'none';
    }  
}

function formulario_senha_cancelar(elemento){
    var display = document.getElementById(elemento).style.display;
    document.getElementById(elemento).style.display = 'none';
}