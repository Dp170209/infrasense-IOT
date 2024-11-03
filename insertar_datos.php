<?php
$conexion = new mysqli("192.168.0.13", "Dp", "", "puentesDB");

if ($conexion->connect_error) {
    die("Conexión fallida: " . $conexion->connect_error);
}

header('Content-Type: application/json');

// Obtener todos los puentes
if ($_SERVER['REQUEST_METHOD'] === 'GET' && empty($_GET['idPuente'])) {
    $resultado = $conexion->query("SELECT * FROM puente");
    $puentes = [];
    while ($fila = $resultado->fetch_assoc()) {
        $puentes[] = $fila;
    }
    echo json_encode($puentes);

// Obtener galgas para un puente específico
} elseif ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['idPuente'])) {
    $idPuente = (int)$_GET['idPuente'];
    $resultado = $conexion->query("SELECT * FROM galga WHERE idPuente = $idPuente");
    $galgas = [];
    while ($fila = $resultado->fetch_assoc()) {
        $galgas[] = $fila;
    }
    echo json_encode($galgas);

// Insertar datos de lectura
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Obtener los datos JSON de la solicitud
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);  // Decodificar el JSON a un array asociativo

    // Validar y asignar los datos
    $idGalga = isset($data['idGalga']) ? (int)$data['idGalga'] : 0;
    $cosTaylor = isset($data['Cos_Taylor']) ? (float)$data['Cos_Taylor'] : 0.0;
    $cosTrig = isset($data['Cos_Trig']) ? (float)$data['Cos_Trig'] : 0.0;
    $error = isset($data['Error']) ? (float)$data['Error'] : 0.0;
    $fecha = isset($data['Fecha']) ? $conexion->real_escape_string($data['Fecha']) : date('Y-m-d H:i:s');

    // Verificar y realizar la inserción si los datos son válidos
    if ($idGalga) {
        $stmt = $conexion->prepare("INSERT INTO datos_de_lectura (Cos_Taylor, Cos_Trig, Error, fecha_hora, idGalga) VALUES (?, ?, ?, ?, ?)");
        $stmt->bind_param("dddsd", $cosTaylor, $cosTrig, $error, $fecha, $idGalga);
        
        if ($stmt->execute()) {
            echo json_encode(["success" => "Datos insertados correctamente."]);
        } else {
            echo json_encode(["error" => "Error al insertar los datos: " . $stmt->error]);
        }
        $stmt->close();
    } else {
        echo json_encode(["error" => "Datos inválidos."]);
    }
} else {
    echo json_encode(["error" => "Solicitud no válida."]);
}

$conexion->close();
?>
