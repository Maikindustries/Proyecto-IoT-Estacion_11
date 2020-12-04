<?php
//Autor: Miguel Angel Pérez López
//Le los valors de la petición y los graba en la base de datos
/*

Ejemplo de url para poner en browser y agregar un dato
http://localhost/IoT/insertar.php?fecha=17050145&hora=Perez&valor=Miguel&extension=xt1005&correo=mike@hotmail.com&oficina=5&reporta=1002&puesto=Ingeniero
*/
include 'conexion.php';
date_default_timezone_set('America/Mexico_City');
//$script_tz = date_default_timezone_get();
//Estos datos los vamos a recibir desde una página
$fecha = date('Y-m-d');
$hora = date('h:i:s');
$idSensor = 2;
if($_GET){
    $idPaciente = $_GET["idPaciente"];
    $medicion = $_GET["medicion"];
    //Designar estado
    if($medicion>=90){
        $estado="Excelente";
    }else{
        $estado="Deficiente";
    }

    $sql_agregar = "INSERT INTO niveldeoxigenacion (idPaciente,idSensor,medicion,fecha,hora,estado) VALUES (?,?,?,?,?,?)";

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