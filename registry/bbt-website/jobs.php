<?php

require_once __DIR__ . '/vendor/autoload.php'; // Include Composer's autoloader

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

// RabbitMQ server credentials
$server = '10.200.1.91';
$port = 5672;
$username = 'admin';
$password = 'admin';

// Job data
$jobId = $_POST['job_id'] ?? null;
$cmd = $_POST['cmd'] ?? null;

if (!$jobId || !$cmd) {
    die('Missing job_id or cmd parameters');
}

// Connect to RabbitMQ server
$connection = new AMQPStreamConnection($server, $port, $username, $password);
$channel = $connection->channel();

// Declare the queue
$queueName = 'bugbounty-jobs';
$channel->queue_declare($queueName, false, true, false, false);

// Create job payload
$jobData = [
    'job_id' => $jobId,
    'cmd' => $cmd,
];

// Convert job data to JSON
$messageBody = json_encode($jobData);

// Create AMQP message
$message = new AMQPMessage($messageBody, ['delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT]);

// Publish message to queue
$channel->basic_publish($message, '', $queueName);

// Close the channel and the connection
$channel->close();
$connection->close();

echo 'Job sent to RabbitMQ server.';