create database gohome;

use gohome;

create table MissingPeople(
id int unsigned primary key auto_increment,
userid varchar(64) not null,
userphone varchar(64) not null,
userloc varchar(64) not null,
photocnt int unsigned default 0,
missing_name varchar(64) not null,
missing_age int unsigned default 0,
missing_sex varchar(64) not null,
missing_city varchar(64) not null,
missing_date datetime default null,
missing_desc text,
reserve1 varchar(64),
reserve2 varchar(64),
reserve3 varchar(64),
reserve4 varchar(64),
reserve5 varchar(64)
);

create table User(
id int unsigned primary key auto_increment,
userid varchar(64) not null,
userloc varchar(64) not null,
useruploadtime datetime default null,
photocnt int unsigned default 0,
reserve1 varchar(64),
reserve2 varchar(64),
reserve3 varchar(64),
reserve4 varchar(64),
reserve5 varchar(64)
);

create table DetectResult (
    id INT primary key NOT NULL AUTO_INCREMENT,
    userid VARCHAR(1024),
    photourl VARCHAR(1024),
    score int unsigned default 0
);
