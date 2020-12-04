<?php
//Autor: Miguel Angel Pérez López
//Le los valors de la petición y los graba en la base de datos
/*

Ejemplo de url para poner en browser y agregar un dato
http://localhost/IoT/insertar.php?fecha=17050145&hora=Perez&valor=Miguel&extension=xt1005&correo=mike@hotmail.com&oficina=5&reporta=1002&puesto=Ingeniero
*/
include 'conexion.php';
//Estos datos los vamos a recibir desde una página
//Hacer query que busque si el paciente es hombre o mujer
date_default_timezone_set('America/Mexico_City');
$fecha = date('Y-m-d');
$hora = date('h:i:s');
$idSensor = 2;



if($_GET){
    $idPaciente = $_GET["idPaciente"];
    $medicion = $_GET["medicion"];
    
    $sql_buscarSexo = "SELECT sexo FROM paciente WHERE idPaciente=".$idPaciente;
    echo $sql_buscarSexo;
    /*
    mysql_select_db("estacion_11");

    $datos=mysql_query($sql_buscarSexo);
    $fila=mysql_fetc_array($datos);
    echo $fila;
    */
    $sentencia_buscar = $pdo->prepare($sql_buscarSexo);
    $sentencia_buscar->execute();
    //$fila = $sentencia_buscar->fetch();
    $fila=$sentencia_buscar->fetch(PDO::FETCH_NUM,PDO::FETCH_ORI_PRIOR);
    $dato= $fila[0];
    /*
    do{
    $dato=$fila[0]."\n";
    echo $dato;
    }while($fila=$sentencia_buscar->fetch(PDO::FETCH_NUM,PDO::FETCH_ORI_PRIOR));
    */
    
    //$pdo=null;
    if($dato=="F"){
        if($medicion>=96){
            $estado="Inadecuado";
        }else if($medicion>=78&&$medicion<=95){
            $estado="Normal";
        }else if($medicio>=72&&$medicion<=75){
            $estado="Bueno";
        }else{
            $estado="Excelente";
        }
    }else{
        if($medicion>=86){
            $estado="Inadecuado";
        }else if($medicion>=70&&$medicion<=85){
            $estado="Normal";
        }else if($medicion>=62&&$medicion<=69){
            $estado="Bueno";
        }else{
            $estado="Excelente";
        }        
    }

    


    $sql_agregar = "INSERT INTO ritmocardiaco (idPaciente,idSensor,medicion,fecha,hora,estado) VALUES (?,?,?,?,?,?)";

    $sentencia_agregar = $pdo->prepare($sql_agregar);
    $resultado = $sentencia_agregar->execute(array($idPaciente,$idSensor,$medicion,$fecha,$hora,$estado));

    if($resultado == true){
        $sentencia_agregar = null;
        $pdo=null;
        echo "\nSe insertó el valor correctamente";
    } else{
        echo "Error al insertar en la BD";
    }

}else{
    echo "Faltan los datos";
}
?>