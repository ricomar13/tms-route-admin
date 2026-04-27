<?php
// 1. Leer datos sin importar cómo los mande el Front (JSON o Form)
$inputJSON = file_get_contents('php://input');
$input = json_decode($inputJSON, true);

$username = $_POST['username'] ?? $input['username'] ?? '';
$password = $_POST['password'] ?? $input['password'] ?? '';

if (empty($username) || empty($password)) {
    http_response_code(400);
    echo json_encode(["detail" => "Faltan datos"]);
    exit;
}

// 2. Buscar al usuario en la base de datos
$stmt = $pdo->prepare("SELECT * FROM user WHERE username = ?");
$stmt->execute([$username]);
$user = $stmt->fetch();

if ($user) {
    // TRUCO DE COMPATIBILIDAD: 
    // Python usa $2b$ y PHP prefiere $2y$. Los intercambiamos solo para la validación.
    $hash = str_replace('$2b$', '$2y$', $user['hashed_password']);

    if (password_verify($password, $hash)) {
        // Login exitoso: Generamos un token (base64 del username para este PoC real)
        echo json_encode([
            "access_token" => base64_encode($user['username']),
            "token_type" => "bearer"
        ]);
        exit;
    }
}

// 3. Si falla
http_response_code(401);
echo json_encode(["detail" => "Usuario o contraseña incorrectos (Validado en PHP)"]);