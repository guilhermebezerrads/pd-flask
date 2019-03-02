function formulario_editar_comentario(elemento1){
    var display1 = document.getElementById(elemento1).style.display;
    var display2 = document.getElementById('ver_comentario').style.display;
    if(display1 == "none"){
        document.getElementById(elemento1).style.display = 'block';
    }else{
        document.getElementById(elemento1).style.display = 'none';
    }  
    if(display2){
        document.getElementById('ver_comentario').style.display = 'none';
    }  
}