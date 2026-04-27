<?php
// 1. Configuración de CORS
header("Access-Control-Allow-Origin: http://localhost:5173");
header("Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With");
header("Access-Control-Allow-Credentials: true");
header("Content-Type: application/json");

if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    http_response_code(200);
    exit();
}

// 2. Importar conexión a DB 
require_once __DIR__ . '/config/db.php';

// 3. Enrutamiento manual (Como FastAPI)
$request_uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

// --- RUTA: /users/token (Login) ---
if ($request_uri === '/users/token' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    include __DIR__ . '/users/token.php';
    exit();
}

// --- RUTA: /users/me (Perfil/Home) ---
if ($request_uri === '/users/me' && $_SERVER['REQUEST_METHOD'] === 'GET') {
    include __DIR__ . '/users/me.php';
    exit();
}

// Si llega aquí, es que la ruta no existe
http_response_code(404);
echo json_encode(["detail" => "Not Found en PHP"]);