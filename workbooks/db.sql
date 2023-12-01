drop table if exists sessions;

create table sessions (
id INT NOT NULL AUTO_INCREMENT,
session_name varchar(150),
is_active bool,
dt_start varchar(50),
dt_end varchar(50),
PRIMARY KEY (id)
)
AUTO_INCREMENT = 1;


drop table if exists transactions;
create table transactions (
id INT NOT NULL AUTO_INCREMENT,
session_id int,
name varchar(50),
dt varchar(50),
money double,
reason varchar(1000),
PRIMARY KEY (id)
)
AUTO_INCREMENT = 1;
