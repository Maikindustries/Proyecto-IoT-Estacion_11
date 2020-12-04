<?php
//Autor: Miguel Angel Pérez López
//Le los valors de la petición y los graba en la base de datos
/*

Ejemplo de url para poner en browser y agregar un dato
http://localhost/IoT/insertar.php?fecha=17050145&hora=Perez&valor=Miguel&extension=xt1005&correo=mike@hotmail.com&oficina=5&reporta=1002&puesto=Ingeniero
*/
include 'conexion.php';
//Estos datos los vamos a recibir desde una página
date_default_timezone_set('America/Mexico_City');
$fecha = date('Y-m-d');
$hora = date("h:i:s");
$idSensor = 1;
//Agregar a los ifs que considere humedad
if($_GET){
    $idPaciente = $_GET["idPaciente"];
    $medicionTemperatura = $_GET["medicionTemperatura"];
    $medicionHumedad = $_GET["medicionHumedad"];
    //Designar estado
    if($medicionTemperatura>=20&&$medicionTemperatura<26){
        $estado="Cálido";
    }else if($medicionTemperatura>=26){
        $estado="Alta";
    }else if($medicionTemperatura<20&&$medicionTemperatura>10){
        $estado="Baja";
    }else{
        $estado="Muy baja";
    }
    $sql_agregar = "INSERT INTO humedadhabitacion (idPaciente,idSensor,medicionTemperatura,medicionHumedad,fecha,hora,estado) VALUES (?,?,?,?,?,?,?)";

    $sentencia_agregar = $pdo->prepare($sql_agregar);
    $resultado = $sentencia_agregar->execute(array($idPaciente,$idSensor,$medicionTemperatura,$medicionHumedad,$fecha,$hora,$estado));

    if($resultado == true){
        $sentencia_agregar = null;
        $pdo=null;
        echo "\nSe insertó el valor correctamente";
        if($estado=="Cálido"){
            echo "La habitación tiene una buena temperatura para que se recupere.";
        }else if($estado=="Alta"){
            echo "La habitación tiene una temperatura alta pero buena para que se recupere.";
        }else if($estado=="Baja"){
           echo "La habitación tiene una temperatura baja, se recomienda que repose en una habitacion más cálida.";
        }else{
            echo "La habitación tiene una temperatura muy baja, se recomienda que repose en una habitación más cálida.";
        }
    } else{
        echo "Error al insertar en la BD";
    }
}else{
    echo "Faltan los datos";
}
?>