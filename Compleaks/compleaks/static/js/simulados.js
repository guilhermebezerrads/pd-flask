
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
        materias.innerHTML = result;
        $("materia_possivel").html(result);
    }});
}






function disponibiliza_materia(obj){
    

    var materias = document.getElementById("MateriasSimulado");
    /*
    var materia_1 = $("#Materia_1");
    var materia_2 = $("#Materia_2");
    var materia_3 = $("#Materia_3");
    */
    //var materia_1.options = document.getElementById("materia-1").childNodes;
    //var materia_2.options = document.getElementById("materia-2").childNodes;
    //var materia_3.options = document.getElementById("materia-3").childNodes;
    var dois = $("#Materia_2").children().length;
    var tres = $("#Materia_3").children().length;
    /*$("#materia_1 option").map(function() {return $(this).val();}).get();
    console.log($("select#example option").map(function() {return $(this).val();}).get());
    console.log(tres);
    console.log(dois);
    var opt2 = $("#Materia_1 option").map(function() {return $(this).val();}).get();
    console.log($("#Materia_1 option[value='" + opt2[0] + "']", this));
    console.log(opt2[0]);
    */
    var opt2 = $("#Materia_2 option").map(function() {return $(this).val();}).get();
    console.log($("#Materia_2 option[value='"+opt2[0]+"']"));
    
    
    if(obj.id == "Materia_1"){

        if(dois != 0){

            if($("#materia-2").css('display') == 'none'){
                $("#materia-2").show();
            }
        }

    }

    if(obj.id == "Materia_2"){

        if($("#materia-2").css('display') == 'none'){
            $("#materia-2").show();
        }
        if(tres != 0){

            if($("#materia-3").css('display') == 'none'){
                $("#materia-3").show();
            }

        }
    }    

    if(obj.id == "Materia_3"){

        if($("#materia-2").css('display') == 'none'){
            $("#materia-2").show();
        }

        if($("#materia-3").css('display') == 'none'){
            $("#materia-3").show();
        }

    }

    if( $("#Materia_1" ).val() == 'a'){
        $("#materia-3").hide();
        $("#materia-2").hide();
    }

    /*

    if( $("#Materia_1" ).val() == $( "#Materia_2" ).val()){
        ordena_options();
    }

    if( $("#Materia_3" ).val() == $( "#Materia_2" ).val()){
         ordena_options();
    }

    if( $("#Materia_1" ).val() == $( "#Materia_3" ).val()){
         ordena_options();
    }
    */

    if(dois != 0){

        var opt2 = $("#Materia_2 option").map(function() {return $(this).val();}).get();

        for (var i = 0; i < opt2.length; i++) {
            console.log(opt2[i]);
            var option = $("#Materia_2 option[value='" + opt2[i] + "']");
            option.attr("disabled",false);
        }

        for (var i = 0; i < opt2.length; i++) {
            if($("#Materia_2 option[value='" + opt2[i] + "']").val() == $("#Materia_1 option:selected").val() ){
                var option = $("#Materia_2 option[value='" + opt2[i] + "']");
                console.log(option);
                option.attr("disabled","disabled");
            }
        }
    }


    if(tres != 0){

        var opt3 = $("#Materia_3 option").map(function() {return $(this).val();}).get();
        
        for (var i = 0; i < opt3.length; i++) {
            var option = $("#Materia_3 option[value='" + opt3[i] + "']");
            option.attr("disabled",false);
        }

        for (var i = 0; i < opt3.length; i++) {
            if($("#Materia_2 option:selected").val() == $("#Materia_3 option[value='" + opt2[i] + "']").val() ){
                var option = $("#Materia_3 option[value='" + opt3[i] + "']");
                console.log(option);
                option.attr("disabled","disabled");
            }
        }

        for (var i = 0; i < opt3.length; i++) {
            if($("#Materia_1 option:selected").val() == $("#Materia_3 option[value='" + opt2[i] + "']").val() ){
                var option = $("#Materia_3 option[value='" + opt3[i] + "']");
                console.log(option);
                option.attr("disabled","disabled");
            }
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