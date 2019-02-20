function arq_pesquisa_todos() {
	document.getElementById("pesquisa").innerHTML = "";
    document.getElementById('tipo').innerHTML = "";
}

function arq_pesquisa_disciplinae() {
    document.getElementById("pesquisa").innerHTML = document.getElementById("pesquisa_disciplina").innerHTML;
    document.getElementById('tipo').innerHTML = document.getElementById("pesquisa_tipo").innerHTML
}

function arq_pesquisa_professor() {
    document.getElementById("pesquisa").innerHTML = document.getElementById("pesquisa_professor").innerHTML;
    document.getElementById('tipo').innerHTML = document.getElementById("pesquisa_tipo").innerHTML
}

function arq_pesquisa_tipo() {
	document.getElementById("pesquisa").innerHTML = "";
    document.getElementById('tipo').innerHTML = document.getElementById("pesquisa_tipo").innerHTML
}

function submete(){
	switch(document.getElementById("filtro").selectedIndex){
	case 1:
		document.getElementById("pesquisa_disciplina").innerHTML = "";
		document.getElementById("pesquisa_tipo").innerHTML = "";
		break;  	
	case 2:
		document.getElementById("pesquisa_professor").innerHTML = "";
		document.getElementById("pesquisa_tipo").innerHTML = "";
		break;
	case 3:
		document.getElementById("pesquisa_tipo").innerHTML = "";
		break;  	
  }
}


function ao_mudar(){

  switch(document.getElementById("filtro").selectedIndex){
  	case 0:
  		arq_pesquisa_todos();
		break;  	
	case 1:
		arq_pesquisa_disciplinae();
		break;  	
	case 2:
		arq_pesquisa_professor();
		break;  	
	case 3:
		arq_pesquisa_tipo();
		break;  	
  }
}

function inicial(){

  switch(document.getElementById("filtro").selectedIndex){
  	case 0:
  		arq_pesquisa_todos();
		break;  	
	case 1:
		user_pesquisa_disciplina();
		break;  	
	case 2:
		user_pesquisa_professor();
		break;  	
	case 3:
		arq_pesquisa_tipo();
		break;  	
  }
}