<?php
//Autor: Miguel Angel Pérez López
//Abre la conexión a la base de datos
//variable e se declara asi $e
try {
    $pdo = new PDO('mysql:host=localhost;dbname=estacion_11','root','');
    echo "Conectado a la BD";
} catch(PDOException $e){
    echo "Error conectando a la BD ";
    print '\nError, '. $e->getMessage();
    die();
}

?>