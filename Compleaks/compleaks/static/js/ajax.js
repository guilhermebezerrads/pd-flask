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

function busca(exibi ,endereco, pagina){
	if(document.getElementById){//Varifica se a funca ger funciona
		var exibeResult = document.getElementById(exibi);
		var ajax = openAjax();
		ajax.open("GET", endereco+"?page="+pagina, true);
		ajax.onreadystatechange = function(){
		
			if(ajax.readyState == 1){
				exibeResult.innerHTML = '<p>Carregando Resultados...</p>';
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
}