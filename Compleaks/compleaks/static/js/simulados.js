
function preenche_formulario(){

    var result_quests = document.getElementById("qtn_quests");
    var materias = document.getElementById("materia_possivel");
    
    if(document.getElementById("escolhe-disciplina").options.length <= 0){
        alert("Infelizmente não há materias elegiveis para simulados no momento!");
        return null;
    }


    var option = document.getElementById("escolhe-disciplina").value;
    console.log(option)

    $.ajax({url: "/simulados/materias-possiveis/"+option, success: function(result){
        materias.innerHTML = result;
        $("materia_possivel").html(result);
    }});

    $.ajax({url: "/simulados/numero-questao/"+option+"/-1%0%0", success: function(result){
        result_quests.innerHTML = result;
        $("qtn_quests").html(result);
    }});
}






function disponibiliza_materia(obj){
    

    var materias = document.getElementById("MateriasSimulado");

    var dois = $("#Materia_2").children().length;
    var tres = $("#Materia_3").children().length;

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

    var n2 = 0;
    var n3 = 0;

    var n1 = $("#Materia_1 option:selected").val();

    if((tres != 0) && ($("#materia-3").css('display') != 'none')){
        n3 = $("#Materia_3 option:selected").val();
    }

    if((dois != 0) && ($("#materia-2").css('display') != 'none')){
        n2 = $("#Materia_2 option:selected").val();
    }
    
    var result_quests = document.getElementById("qtn_quests");
    var option = $("#escolhe-disciplina").val()
    console.log("/simulados/numero-questao/"+option+"/"+n1+"%"+n2+"%"+n3);
    $.ajax({url: "/simulados/numero-questao/"+option+"/"+n1+"%"+n2+"%"+n3, success: function(result){
        result_quests.innerHTML = result;
        $("#qtn_quests").html(result);
    }});
}