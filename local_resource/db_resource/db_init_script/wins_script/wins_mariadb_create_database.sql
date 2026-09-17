

DROP TABLE IF EXISTS app.system_integrity_files;

CREATE TABLE IF NOT EXISTS app.system_integrity_files  (

	`created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `id` varchar(36) NOT NULL,
  `file_path` varchar(512) NOT NULL,
  `original_hash` varchar(128) DEFAULT NULL,
  `update_hash` varchar(128) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `status` varchar(16) NOT NULL DEFAULT 'INTACT',
  `last_error` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS smtp_mail_client_setting  (

	`updated_at` datetime NOT NULL DEFAULT current_timestamp(),
  `mail_url` varchar(128) NOT NULL,
  `mail_port` int NOT NULL,
  `from_mail` varchar(128) NOT NULL ,
  `use_auth` TINYINT(1) DEFAULT 1,
  `login_id` varchar(128) DEFAULT '',
	`login_password` varchar(128) DEFAULT '',
  `use_tls` TINYINT(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

