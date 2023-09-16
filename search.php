<?php

if (isset($_POST)) {
    $params = json_decode(file_get_contents('php://input'), TRUE);

    $token = base64_decode($params['token']);
    $splitedToken = str_split($token, 3);
    $findTasiahKey = array_map(function ($item) {
        return substr($item, -1);
    }, $splitedToken);
    $tasiahKey = implode($findTasiahKey);

    if ($tasiahKey != 'tasiah') {
        echo json_encode([
            'code' => 400,
            'message' => 'token tidak valid'
        ]);
    }

    $message = $params['message'];
    $enginePath = dirname(__FILE__) . '/' . 'search.py';

    $command = escapeshellcmd('python ' . $enginePath . ' "' . $message . '"');
    $output = shell_exec($command);

    if ($output == 'error') {
        echo json_encode([
            'code' => 500,
            'message' => 'ups, ada error pada engine'
        ]);
    }

    $respon = explode('<respon>', $output)[1] ?? '';
    echo json_encode([
        'code' => 200,
        'message' => $respon
    ]);
}

?>