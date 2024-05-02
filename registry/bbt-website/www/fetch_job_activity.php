<?php

$servername = "10.200.1.91";
$username = "admin";
$password = "admin";
$dbname = "bbt";

$conn = new mysqli($servername, $username, $password, $dbname);

$sql = "SELECT LEFT(JOB_ID, 5) as JOB_ID, JOB_UPDATESTATUS, JOB_DATELASTUPDATED from tbl_jobstatus ORDER BY JOB_DATELASTUPDATED DESC";
$result = mysqli_query($conn, $sql);

if (mysqli_num_rows($result) > 0) {
    while ($row = mysqli_fetch_assoc($result)) {
        echo "<tr>
                <th>{$row['JOB_ID']}</th>
                <td>{$row['JOB_UPDATESTATUS']}</td>
                <td>{$row['JOB_DATELASTUPDATED']}</td>
              </tr>";
    }
} else {
    echo "0 results";
}

mysqli_close($conn);
?>
