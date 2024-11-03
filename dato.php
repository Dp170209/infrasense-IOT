<?php
$conexion = new mysqli("localhost", "root", "", "puentesDB");

if ($conexion->connect_error) {
    die("Conexión fallida: " . $conexion->connect_error);
}

header('Content-Type: application/json'); // Asegura que el contenido sea JSON

// Operación para insertar un nuevo dato de lectura
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['fecha_hora']) && isset($_POST['valor']) && isset($_POST['id_galga']) && !isset($_POST['id_dato'])) {
    $fecha_hora = $_POST['fecha_hora'];
    $valor = $_POST['valor'];
    $id_galga = $_POST['id_galga'];

    $sql = "INSERT INTO datos_de_lectura (fecha_hora, valor, idGalga) VALUES ('$fecha_hora', $valor, $id_galga)";

    if ($conexion->query($sql) === TRUE) {
        echo json_encode(["success" => "Dato de lectura insertado correctamente"]);
    } else {
        echo json_encode(["error" => "Error al insertar el dato de lectura: " . $conexion->error]);
    }
}

// Operación para obtener todos los datos de lectura
elseif ($_SERVER['REQUEST_METHOD'] === 'GET' && empty($_GET)) {
    $resultado = $conexion->query("SELECT * FROM datos_de_lectura");

    $datos_de_lectura = [];
    while ($fila = $resultado->fetch_assoc()) {
        $datos_de_lectura[] = $fila;
    }
    echo json_encode($datos_de_lectura);
}

// Operación para obtener los datos de lectura específicos por ID de galga
elseif ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['id_galga_lectura'])) {
    $id_galga = $_GET['id_galga_lectura'];
    $resultado = $conexion->query("SELECT fecha_hora, valor FROM datos_de_lectura WHERE idGalga = $id_galga");

    $lecturas = [];
    while ($fila = $resultado->fetch_assoc()) {
        $lecturas[] = $fila;
    }
    echo json_encode($lecturas);
}

// Operación para eliminar un dato de lectura específico
elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['id_dato']) && isset($_POST['accion']) && $_POST['accion'] === 'eliminar') {
    $id_dato = $_POST['id_dato'];

    $sql = "DELETE FROM datos_de_lectura WHERE idDato = $id_dato";
    if ($conexion->query($sql) === TRUE) {
        echo json_encode(["success" => "Dato de lectura eliminado correctamente."]);
    } else {
        echo json_encode(["error" => "Error al eliminar el dato de lectura: " . $conexion->error]);
    }
} else {
    echo json_encode(["error" => "Solicitud no válida."]);
}

$conexion->close();
?>