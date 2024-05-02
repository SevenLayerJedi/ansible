

                <!-- Icon Cards-->
                <?php
                $servername = "10.200.1.91";
                $username = "admin";
                $password = "admin";
                $dbname = "bbt";
                // Create connection
                $conn = new mysqli($servername, $username, $password, $dbname);
                $sqll = "SELECT  * from sales_stats";
                if (mysqli_query($conn, $sqll)) {
                    echo "";
                } else {
                    echo "Error: " . $sqll . "<br>" . mysqli_error($conn);
                }
                $result = mysqli_query($conn, $sqll);
                if (mysqli_num_rows($result) > 0) {
                    // output data of each row
                    while ($row = mysqli_fetch_assoc($result)) { ?>

                <!--  Total Jobs Completed -->
                <div class="row">
                <div class="col-xl-4 col-sm-6 mb-4">
                <div class="card text-white bg-dark o-hidden h-100">
                <div class="card-body">
                <div class="card-body-icon">
                <i class="fa fa-fw fa-comments"></i>
                </div>
                <div class="mr-5"><?php echo $row["Vistors"]; ?> Total Jobs Completed</div>
                </div>
                <a class="card-footer text-white clearfix small z-1" href="#">
                <span class="float-left">View Details</span>
                <span class="float-right">
                <i class="fa fa-angle-right"></i>
                </span>
                </a>
                </div>
                </div>
                
                <!-- Jobs in Queue -->
                <div class="col-xl-4 col-sm-6 mb-4">
                <div class="card text-white bg-dark o-hidden h-100">
                <div class="card-body">
                <div class="card-body-icon">
                <i class="fa fa-fw fa-list"></i>
                </div>
                <div class="mr-5"><?php echo $row["revenue"]; ?>  Jobs in Queue</div>
                </div>
                <?php }
                } else {
                    echo "0 results";
                }
                ?>
                <a class="card-footer text-white clearfix small z-1" href="#">
                <span class="float-left">View Details</span>
                <span class="float-right">
                <i class="fa fa-angle-right"></i>
                </span>
                </a>
                </div>
                </div>

                <!-- Active Jobs -->
                <div class="col-xl-4 col-sm-6 mb-4">
                <div class="card text-white bg-dark o-hidden h-100">
                <div class="card-body">
                <div class="card-body-icon">
                <i class="fa fa-fw fa-shopping-cart"></i>
                </div>
                <div class="mr-5">4 Active Jobs</div>
                </div>
                <a class="card-footer text-white clearfix small z-1" href="#">
                <span class="float-left">View Details</span>
                <span class="float-right">
                <i class="fa fa-angle-right"></i>
                </span>
                </a>
                </div>
                </div>
