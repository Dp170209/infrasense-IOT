<?php
$conexion = new mysqli("localhost", "root", "", "puentesDB");

if ($conexion->connect_error) {
    die("Conexión fallida: " . $conexion->connect_error);
}

header('Content-Type: application/json');

// Obtener todos los puentes
if ($_SERVER['REQUEST_METHOD'] === 'GET' && empty($_GET)) {
    $resultado = $conexion->query("SELECT * FROM datos_de_lectura");
    $datos_lectura = [];
    while ($fila = $resultado->fetch_assoc()) {
        $datos_lectura[] = $fila;
    }
    echo json_encode($datos_lectura);
} elseif ($_SERVER['REQUEST_METHOD'] === 'GET' && empty($_GET['idPuente']) && empty($_GET['idDato'])) {
    $resultado = $conexion->query("SELECT * FROM puente");
    $puentes = [];
    while ($fila = $resultado->fetch_assoc()) {
        $puentes[] = $fila;
    }
    echo json_encode($puentes);
} elseif ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['idPuente'])) {
    $idPuente = (int)$_GET['idPuente'];
    $resultado = $conexion->query("SELECT * FROM galga WHERE idPuente = $idPuente");
    $galgas = [];
    while ($fila = $resultado->fetch_assoc()) {
        $galgas[] = $fila;
    }
    echo json_encode($galgas);
} elseif ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['idDato'])) {
    $idDato = $_GET['idDato'];
    $resultado = $conexion->query("SELECT valor FROM datos_de_lectura WHERE idDato = $idDato");
    if ($resultado->num_rows > 0) {
        echo json_encode($resultado->fetch_assoc());
    } else {
        echo json_encode(["error" => "No se encontró el dato con el ID especificado."]);
    }
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['id_dato']) && !isset($_POST['accion'])) {
    // Modificación de un registro
    $id_dato = $_POST['id_dato'];
    $nuevo_taylor = $_POST['nuevo_taylor'];
    $nuevo_trig = $_POST['nuevo_trig'];
    $nuevo_error = $_POST['nuevo_error'];

    $sql = "UPDATE datos_de_lectura SET Cos_Taylor = '$nuevo_taylor', Cos_Trig = '$nuevo_trig',Error='$nuevo_error' WHERE idDato = $id_dato";
    if ($conexion->query($sql) === TRUE) {
        echo json_encode(["success" => "Los datos se modificaron correctamente."]);
    } else {
        echo json_encode(["error" => "Error al modificar los datos: " . $conexion->error]);
    }
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['id_dato']) && isset($_POST['accion']) && $_POST['accion'] === 'eliminar') {
    $id_dato = $_POST['id_dato'];

    $sql = "DELETE FROM datos_de_lectura WHERE idDato = $id_dato";
    if ($conexion->query($sql) === TRUE) {
        echo json_encode(["success" => "Dato eliminado correctamente."]);
    } else {
        echo json_encode(["error" => "Error al eliminar el dato: " . $conexion->error]);
    }
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && empty($_POST)) {
    // Nuevo manejador para datos JSON
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);

    // Validar y asignar los datos necesarios
    $idGalga = isset($data['idGalga']) ? (int)$data['idGalga'] : 0;
    $cosTaylor = isset($data['Cos_Taylor']) ? (float)$data['Cos_Taylor'] : 0.0;
    $cosTrig = isset($data['Cos_Trig']) ? (float)$data['Cos_Trig'] : 0.0;
    $error = isset($data['Error']) ? (float)$data['Error'] : 0.0;
    $fecha = isset($data['Fecha']) ? $conexion->real_escape_string($data['Fecha']) : date('Y-m-d H:i:s');

    // Realizar la inserción en caso de tener un ID de galga válido
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
        echo json_encode(["error" => "ID de galga no válido."]);
    }
} else {
    echo json_encode(["error" => "Solicitud no válida."]);
}

$conexion->close();
?>
