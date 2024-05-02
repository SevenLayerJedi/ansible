


                <!-- Update Table Code -->
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                <script>
                    $(document).ready(function(){
                        function fetchJobActivity() {
                            $.ajax({
                                url: "fetch_job_activity.php",
                                type: "GET",
                                success: function(data){
                                    $("#dataTable tbody").html(data); // Replace the tbody contents
                                }
                            });
                        }

                        // Fetch job activity every 5 seconds
                        setInterval(fetchJobActivity, 5000); // Adjust time as needed

                        fetchJobActivity(); // Initial fetch
                    });
                </script>

                <!-- Job Activity Card-->
                <div class="col-xl-12 col-sm-6 mb-6">
                <div class="card">
                    <div class="card-header text-white bg-dark">
                        <i class="fa fa-table"></i> Job Activity</div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
                                    <thead>
                                        <tr>
                                            <th>JOB ID</th>
                                            <th>Job Status</th>
                                            <th>Last Update Date</th>
                                        </tr>
                                    </thead>
                                </table>
                            </div>
                        </div>
                        <div class="card-footer small text-muted">Updated yesterday at 11:59 PM</div>
                    </div>
                </div>
                </div>