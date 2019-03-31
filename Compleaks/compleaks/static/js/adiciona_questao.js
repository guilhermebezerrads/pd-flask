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

	var ajax = openAjax();

	console.log(select.value)

	ajax.open("GET", '/questoes/materias/'+select.value, true);			


	ajax.onreadystatechange = function(){
	
		if(ajax.readyState == 1){
			exibeResult.innerHTML = '<p><img src="/static/images/Preloader_5.gif" alt="Carregando" /></p>';
		}

		if(ajax.readyState == 4){
			if(ajax.status == 200){
				var result = ajax.responseText;
				result = result.replace(/\+/g, " ");
				result = unescape(result);
				exibeResult.innerHTML = result;
			}else{
				exibeResult.innerHTML ="<p>Erro ao carregar pesquisa ---</p>";
			}
		}

	}

	ajax.send(null);


}