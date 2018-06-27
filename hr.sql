BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `users` (
	`id`	INTEGER NOT NULL UNIQUE,
	`user_id`	TEXT UNIQUE,
	`user_name`	TEXT NOT NULL UNIQUE,
	`password`	INTEGER NOT NULL UNIQUE,
	`role`	INTEGER NOT NULL,
	`staff_bumen`	TEXT,
	PRIMARY KEY(`id`)
);
INSERT INTO `users` VALUES (1,'','admin',123,2,NULL);
INSERT INTO `users` VALUES (2,'001','hans','qaz',1,'管理部门');
INSERT INTO `users` VALUES (3,'101','Berk',233,1,'开发部门');
CREATE TABLE IF NOT EXISTS `clock_info` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`user_id`	INTEGER NOT NULL,
	`Clock_time`	TEXT NOT NULL,
	`Create_time`	TEXT NOT NULL,
	`Update_time`	TEXT
);
CREATE TABLE IF NOT EXISTS `banci_info` (
	`banci_id`	INTEGER NOT NULL UNIQUE,
	`star`	TEXT NOT NULL,
	`end`	TEXT NOT NULL,
	`interval`	INTEGER NOT NULL,
	`bumen`	TEXT NOT NULL,
	`creat_time`	TEXT NOT NULL,
	`update_time`	TEXT NOT NULL,
	PRIMARY KEY(`banci_id`)
);
COMMIT;
