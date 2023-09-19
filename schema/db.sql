-- Create syntax for TABLE 'job'
CREATE TABLE `job` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `cron_expression` varchar(20) DEFAULT NULL,
  `api_path` varchar(200) DEFAULT NULL,
  `api_method` varchar(20) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `state` enum('run','stop') DEFAULT NULL,
  `update_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `state` (`state`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

-- Create syntax for TABLE 'job_log'
CREATE TABLE `job_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `job_id` int(11) DEFAULT NULL,
  `msg` text,
  `execute_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `job_id` (`job_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;


INSERT INTO `job` ( `cron_expression`, `api_path`, `api_method`, `description`, `state`, `update_date`)
VALUES
  ('30 0 * * *', 'RunTest()', 'LOCAL', '執行本機測試', 'run', '2023-08-16 07:00:05'),
  ('*/10 * * * *', 'https://xxxx.com/api/v1/notify/send', 'PATCH', '發送推播通知', 'run', '2023-08-04 18:00:29');
