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

function  preenche_materia(){
	var select = document.getElementById("escolhe-disciplina");
	var exibeResult = document.getElementById("materia");

	console.log(select.value)

	$.ajax({url: '/questoes/materias/'+select.value, success: function(result){
        exibeResult.innerHTML = result;
        $("qtn_quests").html(result);
    }});



}