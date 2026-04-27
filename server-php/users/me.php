<?php
$headers = getallheaders();
$auth = $headers['Authorization'] ?? $headers['authorization'] ?? '';

if (strpos($auth, 'Bearer ') === 0) {
    $token = substr($auth, 7);
    $username = base64_decode($token);

    // CONSULTA REAL
    $stmt = $pdo->prepare("SELECT id, username, email, first_name, last_name, role FROM user WHERE username = ?");
    $stmt->execute([$username]);
    $user = $stmt->fetch();

    if ($user) {
        echo json_encode($user);
    } else {
        http_response_code(401);
        echo json_encode(["detail" => "Sesión inválida"]);
    }
} else {
    http_response_code(401);
    echo json_encode(["detail" => "No autorizado por PHP"]);
}