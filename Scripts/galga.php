<?php
$conexion = new mysqli("localhost", "iot", "", "puentesDB");

if ($conexion->connect_error) {
    die("Conexión fallida: " . $conexion->connect_error);
}

header('Content-Type: application/json');

// Capturar el contenido JSON de php://input y decodificarlo
$input = json_decode(file_get_contents("php://input"), true);

// Operación para insertar una nueva galga
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($input['ubicacion_galga']) && isset($input['fecha_instalacion']) && isset($input['id_puente']) && !isset($input['id_galga'])) {
    $ubicacion_galga = $conexion->real_escape_string($input['ubicacion_galga']);
    $fecha_instalacion = $conexion->real_escape_string($input['fecha_instalacion']);
    $id_puente = $conexion->real_escape_string($input['id_puente']);

    $sql = "INSERT INTO galga (ubicacion, fecha_instalacion, idPuente) VALUES ('$ubicacion_galga', '$fecha_instalacion', $id_puente)";

    if ($conexion->query($sql) === TRUE) {
        echo json_encode(["success" => "Galga insertada correctamente"]);
    } else {
        echo json_encode(["error" => "Error al insertar la galga: " . $conexion->error]);
    }
}

// Operación para obtener todas las galgas
elseif ($_SERVER['REQUEST_METHOD'] === 'GET' && empty($_GET)) {
    $resultado = $conexion->query("SELECT * FROM galga");

    $galgas = [];
    while ($fila = $resultado->fetch_assoc()) {
        $galgas[] = $fila;
    }
    echo json_encode($galgas);
}

// Operación para obtener los datos de una galga específica por ID
elseif ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['id_galga'])) {
    $id_galga = $conexion->real_escape_string($_GET['id_galga']);
    $resultado = $conexion->query("SELECT ubicacion, fecha_instalacion, idPuente FROM galga WHERE idGalga = $id_galga");

    if ($resultado->num_rows > 0) {
        $datos = $resultado->fetch_assoc();
        echo json_encode(["ubicacion_galga" => $datos["ubicacion"], "fecha_instalacion" => $datos["fecha_instalacion"], "id_puente" => $datos["idPuente"]]);
    } else {
        echo json_encode(["error" => "No se encontró la galga con el ID especificado."]);
    }
}

// Operación para modificar los datos de una galga específica
elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($input['id_galga']) && isset($input['accion']) && $input['accion'] === 'modificar') {
    if (isset($input['ubicacion_galga']) && isset($input['fecha_instalacion'])) {
        $id_galga = $conexion->real_escape_string($input['id_galga']);
        $ubicacion_galga = $conexion->real_escape_string($input['ubicacion_galga']);
        $fecha_instalacion = $conexion->real_escape_string($input['fecha_instalacion']);

        $sql = "UPDATE galga SET ubicacion = '$ubicacion_galga', fecha_instalacion = '$fecha_instalacion' WHERE idGalga = $id_galga";
        
        if ($conexion->query($sql) === TRUE) {
            echo json_encode(["success" => "Galga modificada correctamente."]);
        } else {
            echo json_encode(["error" => "Error al modificar la galga: " . $conexion->error]);
        }
    } else {
        echo json_encode(["error" => "Datos incompletos para la modificación."]);
    }
}

// Operación para eliminar una galga específica
elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($input['id_galga']) && isset($input['accion']) && $input['accion'] === 'eliminar') {
    $id_galga = $conexion->real_escape_string($input['id_galga']);

    $sql = "DELETE FROM galga WHERE idGalga = $id_galga";
    if ($conexion->query($sql) === TRUE) {
        echo json_encode(["success" => "Galga eliminada correctamente."]);
    } else {
        echo json_encode(["error" => "Error al eliminar la galga: " . $conexion->error]);
    }
} else {
    echo json_encode(["error" => "Solicitud no válida."]);
}

$conexion->close();
?>
