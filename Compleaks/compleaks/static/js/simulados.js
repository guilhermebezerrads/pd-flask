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
}

function preenche_formulario(){

    var result_quests = document.getElementById("qtn_quests");
    var materias = document.getElementById("materia_possivel");
    
    if(document.getElementById("escolhe-disciplina").options.length <= 0){
        alert("Infelizmente não há materias elegiveis para simulados no momento!");
        return null;
    }


    var option = document.getElementById("escolhe-disciplina").value;
    console.log(option)

    $.ajax({url: "/simulados/numero-questao/"+option, success: function(result){
        result_quests.innerHTML = result;
        $("qtn_quests").html(result);
    }});

    $.ajax({url: "/simulados/materias-possiveis/"+option, success: function(result){
        result_quests.innerHTML = result;
        $("materia_possivel").html(result);
    }});
}






function disponibiliza_materia(obj){
    
    console.lof(obj);

    var materias = document.getElementById("MateriasSimulado");

    var materia_1 = document.getElementById("materia-1");
    var materia_2 = document.getElementById("materia-2");
    var materia_3 = document.getElementById("materia-3");

    //var materia_1.options = document.getElementById("materia-1").childNodes;
    //var materia_2.options = document.getElementById("materia-2").childNodes;
    //var materia_3.options = document.getElementById("materia-3").childNodes;

    if(obj.nome == "Materia-1"){

        if(materia_2.style.display == "none"){
            materia_2.style.display = "block"
        }

    }

    if(obj.nome == "Materia-2"){

        if(materia_2.style.display == "none"){
            materia_2.style.display = "block"
        }
        
        if(materia_3.style.display == "none"){
            materia_3.style.display = "block"
        }

    }    

    if(obj.nome == "Materia-3"){

        if(materia_2.style.display == "none"){
            materia_2.style.display = "block"
        }
        
        if(materia_3.style.display == "none"){
            materia_3.style.display = "block"
        }

    }

    if(materia_2.value == materia_1.value){
        materia_2.selectedIndex = 0;
    }

    if(materia_2.value == materia_3.value){
        materia_3.selectedIndex= 0;
    }

    if(materia_1.value == materia_3.value){
        materia_3.selectedIndex = 0;
    }

    for (var i = 0; i < materia_2.options.length; i++) {
        materia_2.options[i].disabled = false;
    }

    for (var i = 0; i < materia_3.options.length; i++) {
         materia_3.options[i].disabled = false;
    }

    for (var i = 0; i < materia_2.options.length; i++) {
        if(materia_1.selectedIndex == (parseInt(materia_2.options[i].value) - 1) ){
            materia_2.options[i].disabled = true;
        }
    }

    for (var i = 0; i < materia_3.options.length; i++) {
        if(materia_1.selectedIndex == (parseInt(materia_3.options[i].value) - 1) ){
            materia_3.options[i].disabled = true;
        }
    }

    for (var i = 0; i < materia_3.options.length; i++) {
        if(materia_2.selectedIndex == parseInt(materia_3.options[i].value) ){
            materia_3.options[i].disabled = true;
        }
    }

    
}


/*var aux = 0;
    var changes = repositorio.childNodes;

    if(childs_materia.length <= 3){
        aux = 3;
    }else{
        var last = childs_materia[childs_materia.length - 1];
        var str = last.id;
        str = str.split("-");
        aux = parseInt(str[1]);
        aux++;
    }
    

    repositorio.id = "materia-"+aux;
    repositorio.style.display = "";
    changes[3].id = "inputIconEx"+aux;
    changes[3].name = "materia-"+aux;
    //changes[5].for = changes[3].id;
    changes[7].setAttribute("onclick","Remover_Materia(\'materia-"+aux+"\');");

    materias.appendChild(repositorio);*/

    //console.log(childs_materia.length );

    /*console.log(childs_materia[childs_materia.length - 1]);
    var last = childs_materia[childs_materia.length - 1];

    var gambiarra = document.getElementById("gambiarra");
    var node_gambiarra = document.createElement("br");

    gambiarra.appendChild(node_gambiarra);*/