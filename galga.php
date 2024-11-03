<?php
$conexion = new mysqli("localhost", "root", "", "puentesDB");

if ($conexion->connect_error) {
    die("Conexión fallida: " . $conexion->connect_error);
}

header('Content-Type: application/json'); // Asegura que el contenido sea JSON

// Operación para insertar una nueva galga
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['ubicacion_galga']) && isset($_POST['fecha_instalacion']) && isset($_POST['id_puente']) && !isset($_POST['id_galga'])) {
    $ubicacion_galga = $_POST['ubicacion_galga'];
    $fecha_instalacion = $_POST['fecha_instalacion'];
    $id_puente = $_POST['id_puente'];

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
    $id_galga = $_GET['id_galga'];
    $resultado = $conexion->query("SELECT ubicacion, fecha_instalacion, idPuente FROM galga WHERE idGalga = $id_galga");

    if ($resultado->num_rows > 0) {
        $datos = $resultado->fetch_assoc();
        echo json_encode(["ubicacion_galga" => $datos["ubicacion"], "fecha_instalacion" => $datos["fecha_instalacion"], "id_puente" => $datos["idPuente"]]);
    } else {
        echo json_encode(["error" => "No se encontró la galga con el ID especificado."]);
    }
}

// Operación para modificar los datos de una galga específica
elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['id_galga']) && !isset($_POST['accion'])) {
    $id_galga = $_POST['id_galga'];
    $ubicacion_galga = $_POST['ubicacion_galga'];
    $fecha_instalacion = $_POST['fecha_instalacion'];
    $id_puente = $_POST['id_puente'];

    $sql = "UPDATE galga SET ubicacion = '$ubicacion_galga', fecha_instalacion = '$fecha_instalacion', idPuente = $id_puente WHERE idGalga = $id_galga";
    if ($conexion->query($sql) === TRUE) {
        echo json_encode(["success" => "Galga modificada correctamente."]);
    } else {
        echo json_encode(["error" => "Error al modificar la galga: " . $conexion->error]);
    }
}

// Operación para eliminar una galga específica
elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['id_galga']) && isset($_POST['accion']) && $_POST['accion'] === 'eliminar') {
    $id_galga = $_POST['id_galga'];

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
