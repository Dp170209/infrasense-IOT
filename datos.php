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
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['id_dato']) && isset($_POST['nuevo_valor'])) {
    // Modificación de un registro
    $id_dato = $_POST['id_dato'];
    $nuevo_valor = $_POST['nuevo_valor'];

    $sql = "UPDATE datos_de_lectura SET valor = '$nuevo_valor' WHERE idDato = $id_dato";
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
} else {
    echo json_encode(["error" => "Solicitud no válida."]);
}
$conexion->close();
?>
