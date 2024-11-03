<?php
$conexion = new mysqli("localhost", "root", "", "puentesDB");

if ($conexion->connect_error) {
    die("Conexión fallida: " . $conexion->connect_error);
}

header('Content-Type: application/json');

// Obtener el contenido JSON de la solicitud
$input = json_decode(file_get_contents("php://input"), true);

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
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($input['id_dato']) && isset($input['nuevo_taylor']) && isset($input['nuevo_trig']) && isset($input['nuevo_error'])) {
    // Modificación de un registro
    $id_dato = (int)$input['id_dato'];
    $nuevo_taylor = (float)$input['nuevo_taylor'];
    $nuevo_trig = (float)$input['nuevo_trig'];
    $nuevo_error = (float)$input['nuevo_error'];

    $sql = "UPDATE datos_de_lectura SET Cos_Taylor = '$nuevo_taylor', Cos_Trig = '$nuevo_trig', Error = '$nuevo_error' WHERE idDato = $id_dato";
    if ($conexion->query($sql) === TRUE) {
        echo json_encode(["success" => "Los datos se modificaron correctamente."]);
    } else {
        echo json_encode(["error" => "Error al modificar los datos: " . $conexion->error]);
    }
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($input['id_dato']) && isset($input['accion']) && $input['accion'] === 'eliminar') {
    $id_dato = (int)$input['id_dato'];

    $sql = "DELETE FROM datos_de_lectura WHERE idDato = $id_dato";
    if ($conexion->query($sql) === TRUE) {
        echo json_encode(["success" => "Dato eliminado correctamente."]);
    } else {
        echo json_encode(["error" => "Error al eliminar el dato: " . $conexion->error]);
    }
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($input['idGalga'], $input['Cos_Taylor'], $input['Cos_Trig'], $input['Error'], $input['Fecha'])) {
    // Inserción de nuevos datos
    $idGalga = (int)$input['idGalga'];
    $cosTaylor = (float)$input['Cos_Taylor'];
    $cosTrig = (float)$input['Cos_Trig'];
    $error = (float)$input['Error'];
    $fecha = $conexion->real_escape_string($input['Fecha']);

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
