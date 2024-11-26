<?php
$conexion = new mysqli("localhost", "root", "", "puentesDB");

if ($conexion->connect_error) {
    die("Conexión fallida: " . $conexion->connect_error);
}

header('Content-Type: application/json');

// Lee el contenido JSON para las solicitudes que no usan `$_POST` directamente
$inputData = json_decode(file_get_contents("php://input"), true);

// Operación para insertar un nuevo puente
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($inputData['nombre_puente']) && isset($inputData['ubicacion']) && !isset($inputData['id_puente'])) {
    $nombre_puente = $inputData['nombre_puente'];
    $ubicacion = $inputData['ubicacion'];

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
elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($inputData['accion']) && $inputData['accion'] === 'modificar') {
    $id_puente = $inputData['id_puente'];
    $nombre_puente = $inputData['nombre_puente'];
    $ubicacion = $inputData['ubicacion'];

    $sql = "UPDATE puente SET nombre = '$nombre_puente', ubicacion = '$ubicacion' WHERE idPuente = $id_puente";
    if ($conexion->query($sql) === TRUE) {
        echo json_encode(["success" => "Los datos se modificaron correctamente."]);
    } else {
        echo json_encode(["error" => "Error al modificar los datos: " . $conexion->error]);
    }
}

// Operación para eliminar un puente específico
elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($inputData['id_puente']) && isset($inputData['accion']) && $inputData['accion'] === 'eliminar') {
    $id_puente = $inputData['id_puente'];

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
