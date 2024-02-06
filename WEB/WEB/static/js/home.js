
function Obteniendo_Registro_Respuestas_Automaticas(){
    $.ajax({
        url: url_respuestas_automaticas ,
        type:'get',
        dataType:'JSON',
        success: function( request ){
        	dibujando_registros_respuestas_automaticas( request['respuesta'] )
        },
        error: function( request ){
            console.log("Error Error Error")
        },
    })

}

function dibujando_registros_respuestas_automaticas( list_registros ){

    lista_tr_row_respuestas_automaticas.forEach( tr_ingresado => {
		tr_ingresado.remove()
    });
    
    lista_tr_row_respuestas_automaticas = []
    
    list_registros.forEach( data_row => {
    	
    	console.log( data_row )

        let tr_row = $("#row_table_respuesta_automatica").clone()

        $(tr_row).attr("hidden",false)

        $(tr_row).find("#id_file").text( String( data_row["id"] ) )
        $(tr_row).find("#name_file").text( String( data_row["name_file"] ) )
        $(tr_row).find("#date_file").text( String( data_row["fecha_creacion"].substring(0, 16) ) )

        $( tr_row ).insertBefore("#row_table_respuesta_automatica")
        
        lista_tr_row_respuestas_automaticas.push( tr_row )

    }); 
}

function download_files_registros_respuestas_automaticas( button ){
	let tr_row = button.parentNode.parentNode;
	let id_row = $(tr_row).find("#id_file").text()
    window.location.replace( url_respuestas_automaticas_files + "?id=" + id_row );
}

function Obteniendo_CronoJobs(){
    $.ajax({
        url: url_cronojobs ,
        type:'get',
        dataType:'JSON',
        success: function( request ){
            console.log( request )
            console.log( request )
            console.log( request )
            console.log( request )
            dibujando_registros_CronoJobs( request['respuesta'] )
        },
        error: function( request ){
            console.log("Error Error Error")
        },
    })

}

function dibujando_registros_CronoJobs( list_registros ){
    console.log( list_registros )
    lista_tr_row_cronojobs.forEach( tr_ingresado => {
        tr_ingresado.remove()
    });
    console.log(11111)
    lista_tr_row_cronojobs = []
    console.log(22222)
    list_registros.forEach( data_row => {
        
        console.log( data_row )

        let tr_row = $("#row_table_cronojob").clone()

        $(tr_row).attr("hidden",false)

        $(tr_row).find("#id_file").text( String( data_row["id"] ) )
        $(tr_row).find("#name_file").text( String( data_row["name_file"] ) )
        $(tr_row).find("#date_ejecucion_file").text( String( data_row["fecha_ejecusion"].substring(0, 16) ) )
        $(tr_row).find("#state_file").text( String( data_row["estado"] ) )
        $(tr_row).find("#date_creacion_file").text( String( data_row["fecha_creacion"].substring(0, 16) ) )
        $( tr_row ).insertBefore("#row_table_cronojob")
        
        lista_tr_row_cronojobs.push( tr_row )

    }); 
}

console.log('Conexion Realizada')

Obteniendo_Registro_Respuestas_Automaticas()

Obteniendo_CronoJobs()