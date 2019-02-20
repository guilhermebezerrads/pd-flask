var pesq_disciplina = document.getElementById("pesquisa_disciplina");
var pesq_professor = document.getElementById("pesquisa_professor");
var pesq_tipo = document.getElementById("pesquisa_tipo");
var tipo_display = document.getElementById('tipo');
var pesquisa_display = document.getElementById("pesquisa");


function arq_pesquisa_todos() {
	pesquisa_display.innerHTML = "";
    tipo_display.innerHTML = "";
}

function arq_pesquisa_disciplinae() {
    pesquisa_display.innerHTML = pesq_disciplina.innerHTML;
    tipo_display.innerHTML = pesq_tipo.innerHTML
}

function arq_pesquisa_professor() {
    pesquisa_display.innerHTML = pesq_professor.innerHTML;
    tipo_display.innerHTML = pesq_tipo.innerHTML
}

function arq_pesquisa_tipo() {
	pesquisa_display.innerHTML = "";
    tipo_display.innerHTML = pesq_tipo.innerHTML
}

document.getElementById("submit").onsubmit = function (){
	switch(this.selectedIndex){
	case 1:
		pesq_disciplina.innerHTML = "";
		pesq_tipo.innerHTML = "";
		break;  	
	case 2:
		pesq_professor.innerHTML = "";
		pesq_tipo.innerHTML = "";
		break;
	case 3:
		pesq_tipo.innerHTML = "";
		break;  	
  }
}


document.getElementById("filtro").onchange = function(){

  switch(this.selectedIndex){
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