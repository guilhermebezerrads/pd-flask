function colorir(id, valor){
    id = parseInt(id);
    valor = parseInt(valor);

    var stars = document.getElementsByClassName("star-"+id);

    for(i=4; i>=0; i--){
        stars[i].name = "star-outline";
    }
    

    for(i=0; i<=valor-1; i++){
        stars[i].name = "star";
    } 
}

function colorir2(id, valor){
    id = parseInt(id);
    valor = parseInt(valor);

    var stars2 = document.getElementsByClassName("star2-"+id);

    for(i=4; i>=0; i--){
        stars2[i].name = "star-outline";
    }
    

    for(i=0; i<=valor-1; i++){
        stars2[i].name = "star";
    } 
}

function pontua(id, valor){

    id = parseInt(id);
    valor = parseInt(valor);

    var stars = document.getElementsByClassName("star-"+id);
    var stars2 = document.getElementsByClassName("star2-"+id);

    $.ajax({type : 'post', 
        url: "/arquivos/avaliar/"+id+"/"+valor,
        success: function(result){

            result = result.split(".")
            let num = parseInt(result[1]);
            if(result[0]=="Apagado"){


                for(i=4; i>=0; i--){
                    stars[i].name = "star-outline";
                    stars[i].style.color = " rgb(243, 38, 54)"
                    stars[i].setAttribute("onmouseout","colorir("+id+", "+num+");");

                    stars2[i].name = "star-outline";
                    stars2[i].style.color = " rgb(243, 38, 54)"
                    stars2[i].setAttribute("onmouseout","colorir2("+id+", "+num+");");
                }

                for(i=0; i<=num-1; i++){
                    stars[i].name = "star";
                    stars2[i].name = "star";
                }

            }else{
                console.log("Aloha");

                for(i=4; i>=0; i--){
                    stars[i].name = "star-outline";
                    stars[i].style.color = " rgb(255, 217, 0)"
                    stars[i].setAttribute("onmouseout","colorir("+id+", "+num+");");

                    stars2[i].name = "star-outline";
                    stars2[i].style.color = " rgb(255, 217, 0)"
                    stars2[i].setAttribute("onmouseout","colorir2s("+id+", "+num+");"); 
                }
                
                for(i=0; i<=num-1; i++){
                    stars[i].name = "star";
                    stars2[i].name = "star";
                }

            }

            
        }
    });

}
