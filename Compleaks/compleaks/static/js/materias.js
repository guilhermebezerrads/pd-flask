function Nova_Materia(){
	var childs_materia = document.getElementById("Materias").childNodes;

	if(childs_materia.length >= 17){
		return null;
	}

	var materias = document.getElementById("Materias");

	var repositorio = document.getElementById("repositorio").cloneNode(true); 

	var aux = 0;
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

	materias.appendChild(repositorio);

	//console.log(childs_materia.length );

	/*console.log(childs_materia[childs_materia.length - 1]);
	var last = childs_materia[childs_materia.length - 1];*/

	var gambiarra = document.getElementById("gambiarra");
	var node_gambiarra = document.createElement("br");

	gambiarra.appendChild(node_gambiarra);

	
}


function Remover_Materia(id){

	var parent = document.getElementById("Materias");
	var child = document.getElementById(id);

	console.log(child);	
	parent.removeChild(child);

	var gambiarra = document.getElementById("gambiarra");
	var gambiarra_sons = document.getElementById("gambiarra").childNodes;

	console.log(gambiarra);

	try{
		gambiarra.removeChild(gambiarra_sons[0]);
	}finally{
		console.log("Voce ativou um ester-egg de uma execessão bem inútil");
	}

}