var pesq_username = document.getElementById("pesquisa_username");
var pesq_nome = document.getElementById("pesquisa_nome");
var pesq_email = document.getElementById("pesquisa_email");
var pesquisa = document.getElementById("pesquisa");


function user_pesquisa_todos() {
	pesquisa.innerHTML = "";
}

function user_pesquisa_username() {
    pesquisa.innerHTML = pesq_username.innerHTML;
}

function user_pesquisa_nome() {
    pesquisa.innerHTML = pesq_nome.innerHTML;
}

function user_pesquisa_email() {
    pesquisa.innerHTML = pesq_email.innerHTML;
}


document.getElementById("submit").onkeypress = function (){
	switch(this.selectedIndex){
	case 1:
		pesq_username.innerHTML = "";
		break;  	
	case 2:
		pesq_nome.innerHTML = "";
		break;  	
	case 3:
		pesq_email.innerHTML = "";
		break;  	
  }
}


document.getElementById("filtro").onchange = function(){

  switch(this.selectedIndex){
  	case 0:
  		user_pesquisa_todos();
		break;  	
	case 1:
		user_pesquisa_username();
		break;  	
	case 2:
		user_pesquisa_nome();
		break;  	
	case 3:
		user_pesquisa_email();
		break;  	
  }
}

function inicial(){

  switch(document.getElementById("filtro").selectedIndex){
  	case 0:
  		user_pesquisa_todos();
		break;  	
	case 1:
		user_pesquisa_username();
		break;  	
	case 2:
		user_pesquisa_nome();
		break;  	
	case 3:
		user_pesquisa_email();
		break;  	
  }
}