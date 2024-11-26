<?php
// Configuración de conexión a la base de datos
$conexion = new mysqli("localhost", "root", "", "puentesDB");

if ($conexion->connect_error) {
    die(json_encode(["error" => "Conexión fallida: " . $conexion->connect_error]));
}

header('Content-Type: application/json');

// Leer el contenido JSON de la solicitud
$input = json_decode(file_get_contents("php://input"), true);

// Obtener todos los datos de lectura
if ($_SERVER['REQUEST_METHOD'] === 'GET' && empty($_GET)) {
    $resultado = $conexion->query("SELECT * FROM datos_de_lectura");
    if ($resultado) {
        $datos_lectura = $resultado->fetch_all(MYSQLI_ASSOC);
        echo json_encode($datos_lectura);
    } else {
        echo json_encode(["error" => "Error al obtener los datos de lectura: " . $conexion->error]);
    }
}

// Obtener todos los puentes
elseif ($_SERVER['REQUEST_METHOD'] === 'GET' && empty($_GET['idPuente']) && empty($_GET['idDato'])) {
    $resultado = $conexion->query("SELECT * FROM puente");
    if ($resultado) {
        $puentes = $resultado->fetch_all(MYSQLI_ASSOC);
        echo json_encode($puentes);
    } else {
        echo json_encode(["error" => "Error al obtener los puentes: " . $conexion->error]);
    }
}

// Obtener todas las galgas de un puente específico
elseif ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['idPuente'])) {
    $idPuente = (int)$_GET['idPuente'];
    $stmt = $conexion->prepare("SELECT * FROM galga WHERE idPuente = ?");
    $stmt->bind_param("i", $idPuente);
    $stmt->execute();
    $resultado = $stmt->get_result();
    $galgas = $resultado->fetch_all(MYSQLI_ASSOC);
    echo json_encode($galgas);
    $stmt->close();
}

// Obtener un dato específico de lectura
elseif ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['idDato'])) {
    $idDato = (int)$_GET['idDato'];
    $stmt = $conexion->prepare("SELECT * FROM datos_de_lectura WHERE idDato = ?");
    $stmt->bind_param("i", $idDato);
    $stmt->execute();
    $resultado = $stmt->get_result();
    if ($resultado->num_rows > 0) {
        echo json_encode($resultado->fetch_assoc());
    } else {
        echo json_encode(["error" => "No se encontró el dato con el ID especificado."]);
    }
    $stmt->close();
}

// Actualizar un registro en la tabla de datos de lectura
elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($input['id_dato'], $input['nuevo_peso'], $input['iothing'])) {
    $id_dato = (int)$input['id_dato'];
    $nuevo_peso = (float)$input['nuevo_peso'];
    $iothing = (String)$input['iothing'];

    $stmt = $conexion->prepare("UPDATE datos_de_lectura SET peso = ?, iothing = ? WHERE idDato = ?");
    $stmt->bind_param("dsi", $nuevo_peso, $iothing, $id_dato);

    if ($stmt->execute()) {
        echo json_encode(["success" => "Los datos se modificaron correctamente."]);
    } else {
        echo json_encode(["error" => "Error al modificar los datos: " . $stmt->error]);
    }
    $stmt->close();
}

// Eliminar un registro de la tabla de datos de lectura
elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($input['id_dato'], $input['accion']) && $input['accion'] === 'eliminar') {
    $id_dato = (int)$input['id_dato'];

    $stmt = $conexion->prepare("DELETE FROM datos_de_lectura WHERE idDato = ?");
    $stmt->bind_param("i", $id_dato);

    if ($stmt->execute()) {
        echo json_encode(["success" => "Dato eliminado correctamente."]);
    } else {
        echo json_encode(["error" => "Error al eliminar el dato: " . $stmt->error]);
    }
    $stmt->close();
}

else {
    echo json_encode(["error" => "Solicitud no válida."]);
}

$conexion->close();
?>
