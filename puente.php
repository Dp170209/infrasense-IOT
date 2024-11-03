<?php
$conexion = new mysqli("localhost", "root", "", "puentesDB");

if ($conexion->connect_error) {
    die("Conexión fallida: " . $conexion->connect_error);
}

header('Content-Type: application/json'); // Asegura que el contenido sea JSON

// Operación para insertar un nuevo puente
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['nombre_puente']) && isset($_POST['ubicacion']) && !isset($_POST['id_puente'])) {
    $nombre_puente = $_POST['nombre_puente'];
    $ubicacion = $_POST['ubicacion'];

    $sql = "INSERT INTO Puente (nombre, ubicacion) VALUES ('$nombre_puente', '$ubicacion')";

    if ($conexion->query($sql) === TRUE) {
        echo json_encode(["success" => "Registro insertado correctamente"]);
    } else {
        echo json_encode(["error" => "Error al insertar el registro: " . $conexion->error]);
    }
}

// Operación para obtener todos los puentes con todos sus datos
elseif ($_SERVER['REQUEST_METHOD'] === 'GET' && empty($_GET)) {
    $resultado = $conexion->query("SELECT * FROM puente");

    $puentes = [];
    while ($fila = $resultado->fetch_assoc()) {
        $puentes[] = $fila;
    }
    echo json_encode($puentes);
}

// Operación para obtener los datos de un puente específico por ID
elseif ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['id_puente'])) {
    $id_puente = $_GET['id_puente'];
    $resultado = $conexion->query("SELECT nombre, ubicacion FROM puente WHERE idPuente = $id_puente");

    if ($resultado->num_rows > 0) {
        $datos = $resultado->fetch_assoc();
        echo json_encode(["nombre_puente" => $datos["nombre"], "ubicacion" => $datos["ubicacion"]]);
    } else {
        echo json_encode(["error" => "No se encontró el puente con el ID especificado."]);
    }
}

// Operación para modificar los datos de un puente específico
elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['id_puente']) && !isset($_POST['accion'])) {
    $id_puente = $_POST['id_puente'];
    $nombre_puente = $_POST['nombre_puente'];
    $ubicacion = $_POST['ubicacion'];

    $sql = "UPDATE puente SET nombre = '$nombre_puente', ubicacion = '$ubicacion' WHERE idPuente = $id_puente";
    if ($conexion->query($sql) === TRUE) {
        echo json_encode(["success" => "Los datos se modificaron correctamente."]);
    } else {
        echo json_encode(["error" => "Error al modificar los datos: " . $conexion->error]);
    }
}

// Operación para eliminar un puente específico (eliminación completa del registro)
elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['id_puente']) && isset($_POST['accion']) && $_POST['accion'] === 'eliminar') {
    $id_puente = $_POST['id_puente'];

    $sql = "DELETE FROM puente WHERE idPuente = $id_puente";
    if ($conexion->query($sql) === TRUE) {
        echo json_encode(["success" => "Puente eliminado correctamente."]);
    } else {
        echo json_encode(["error" => "Error al eliminar el puente: " . $conexion->error]);
    }
} else {
    echo json_encode(["error" => "Solicitud no válida."]);
}

$conexion->close();
?>
