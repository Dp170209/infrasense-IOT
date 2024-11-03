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
    
// Obtener todos los puentes
}elseif ($_SERVER['REQUEST_METHOD'] === 'GET' && empty($_GET['idPuente']) && empty($_GET['idDato'])) {
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
    
// Obtener un dato de lectura específico de la tabla 'datos_de_lectura'
} elseif ($_SERVER['REQUEST_METHOD'] === isset($_GET['idDato'])) {
    $idDato = $_GET['idDato'];
    $resultado = $conexion->query("SELECT valor FROM datos_de_lectura WHERE idDato = $idDato");
    $dato = $resultado->fetch_assoc();
    if ($resultado->num_rows > 0) {
        $datos = $resultado->fetch_assoc();
        echo json_encode(["valor" => $datos["valor"]]);
    } else {
        echo json_encode(["error" => "No se encontró el dato con el ID especificado."]);
    }

// Insertar nuevo registro en 'datos_de_lectura'
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Obtener los datos JSON de la solicitud
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);  // Decodificar el JSON a un array asociativo

    // Validar y asignar los datos
    $idGalga = isset($data['idGalga']) ? (int)$data['idGalga'] : 0;
    $valor = isset($data['Cos_Taylor']) ? (float)$data['Cos_Taylor'] : 0.0;
    $fecha = isset($data['Fecha']) ? $conexion->real_escape_string($data['Fecha']) : date('Y-m-d H:i:s');

    // Verificar y realizar la inserción si los datos son válidos
    if ($idGalga && $valor) {
        $stmt = $conexion->prepare("INSERT INTO datos_de_lectura (fecha_hora, valor, idGalga) VALUES (?, ?, ?)");
        $stmt->bind_param("sdi", $fecha, $valor, $idGalga);
        
        if ($stmt->execute()) {
            echo json_encode(["success" => "Datos insertados correctamente."]);
        } else {
            echo json_encode(["error" => "Error al insertar los datos."]);
        }
        $stmt->close();
    } else {
        echo json_encode(["error" => "Datos inválidos."]);
    }

// Modificar un registro existente en 'datos_de_lectura'
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['id_dato']) && !isset($_POST['accion'])) {
    $id_dato = $_POST['id_dato'];
    $nuevo_valor = $_POST['nuevo_valor'];

    $sql = "UPDATE datos_de_lectura SET valor = '$nuevo_valor' WHERE idDato = $id_dato";
    if ($conexion->query($sql) === TRUE) {
        echo json_encode(["success" => "Los datos se modificaron correctamente."]);
    } else {
        echo json_encode(["error" => "Error al modificar los datos: " . $conexion->error]);
    }
}
elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['id_dato']) && isset($_POST['accion']) && $_POST['accion'] === 'eliminar') {
    $id_dato = $_POST['id_dato'];

    $sql = "DELETE FROM puente WHERE idDato = $id_dato";
    if ($conexion->query($sql) === TRUE) {
        echo json_encode(["success" => "Dato eliminado correctamente."]);
    } else {
        echo json_encode(["error" => "Error al eliminar el puente: " . $conexion->error]);
    }
} else {
    echo json_encode(["error" => "Solicitud no válida."]);
}
$conexion->close();
?>

