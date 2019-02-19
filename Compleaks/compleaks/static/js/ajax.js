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

function busca_assincrona(exibi , adm, filtrar, pesquisar, t_arquiv){
	if(document.getElementById){//Varifica se a funca ger funciona
		var exibeResult = document.getElementById(exibi);
		var ajax = openAjax();

		filtro = parseInt(document.getElementById(filtrar).value);
		pesquisa = document.getElementById(pesquisar).childNodes;
		tipo_arquivo = document.getElementById(t_arquiv).childNodes;

		pesquisa = pesquisa[3].value;
		tipo_arquivo = tipo_arquivo[3].value;

		if (pesquisa == ''){
			ajax.open("GET", '/arquivos/busca_asn/'+adm+'/'+3+'/'+tipo_arquivo, true);			
		}else{
			ajax.open("GET", '/arquivos/busca_asn/'+adm+'/'+filtro+'/'+pesquisa+'/'+tipo_arquivo, true);			
		}
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
}