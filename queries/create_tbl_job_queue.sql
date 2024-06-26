CREATE TABLE `tbl_job_config` (
  `id` enum('1') NOT NULL,
  `max_job_queue_size` int NOT NULL
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci	

INSERT INTO `tbl_job_config` (`id`, `max_job_queue_size`) VALUES ('1', '20');


CREATE TABLE `tbl_worker_config` (
  `id` enum('1') NOT NULL,
  `max_worker_count` int NOT NULL
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci	

INSERT INTO `tbl_worker_config` (`id`, `max_worker_count`) VALUES ('1', '5');


CREATE TABLE `tbl_job_category` (
  `job_type` varchar(256) NOT NULL
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci	

INSERT INTO `tbl_job_category` (`job_type`) VALUES ('nmap');
INSERT INTO `tbl_job_category` (`job_type`) VALUES ('masscan');
INSERT INTO `tbl_job_category` (`job_type`) VALUES ('nikto');
INSERT INTO `tbl_job_category` (`job_type`) VALUES ('dirbuster');
INSERT INTO `tbl_job_category` (`job_type`) VALUES ('gobuster');
INSERT INTO `tbl_job_category` (`job_type`) VALUES ('ffuf');



CREATE TABLE `tbl_job_status` (
  `job_id` varchar(256) NOT NULL,
  `job_update_status` varchar(256) NOT NULL,
  `job_date_last_updated` datetime NOT NULL
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci	




CREATE TABLE `tbl_job_queue` (
  `job_id` VARCHAR(256) NOT NULL,
  `job_type` VARCHAR(256) NOT NULL,
  `job_category` VARCHAR(256) NOT NULL,
  `geoname_id` VARCHAR(256) NOT NULL,
  `job_target` VARCHAR(256) NOT NULL,
  `job_created_date` DATETIME NOT NULL,
  UNIQUE KEY `job_id` (`job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



CREATE TABLE `tbl_outputfile_path` (
  `outputfile_name` VARCHAR(256) NOT NULL,
  `outputfile_path` VARCHAR(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `tbl_outputfile_path` (`outputfile_name`, `outputfile_path`) VALUES ('nmap', '/opt/bbt/nmap');



CREATE TABLE `tbl_job_type` (
  `job_type_name` VARCHAR(256) NOT NULL,
  `job_binary_path` VARCHAR(256) NOT NULL,
  `job_switches` VARCHAR(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `tbl_job_type` (`job_type_name`, `job_binary_path`, `job_switches`) VALUES ('nmap_full_tcp', '/usr/bin/nmap', '-sC -sV -oA {outputfile} -p- {target}');

CREATE TABLE `tbl_job_status_categories` (
  `job_status_category` VARCHAR(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `tbl_job_status_categories` (`job_status_category`) VALUES ('New');
INSERT INTO `tbl_job_status_categories` (`job_status_category`) VALUES ('In Progress');
INSERT INTO `tbl_job_status_categories` (`job_status_category`) VALUES ('Paused');
INSERT INTO `tbl_job_status_categories` (`job_status_category`) VALUES ('Completed');



CREATE TABLE `tbl_jobs` (
  `job_id` VARCHAR(256) NOT NULL,
  `job_type` VARCHAR(256) NOT NULL,
  `job_category` VARCHAR(256) NOT NULL,
  `geoname_id` VARCHAR(256) NOT NULL,
  `job_target` VARCHAR(256) NOT NULL,
  `job_status` VARCHAR(256) NOT NULL,
  `job_owner` VARCHAR(256) DEFAULT NULL,
  `job_percent_complete` INT DEFAULT NULL,
  `job_created_date` DATETIME NOT NULL,
  `job_start_date` DATETIME NOT NULL,
  `job_end_date` DATETIME DEFAULT NULL,
  `job_date_last_updated` DATETIME NOT NULL,
  UNIQUE KEY `job_id` (`job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

