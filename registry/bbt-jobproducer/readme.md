# Build Docker Image
docker build -t bbt-jobproducer .

# Start Docker Image
docker run -d --name bbt-jobproducer -v /mnt/nvme/jobs/bugbounty:/mnt/nvme/jobs/bugbounty bbt-jobproducer
