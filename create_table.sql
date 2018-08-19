

create table j_stocks(
id int not null primary key auto_increment,
indexs varchar(11),
stock varchar(11),
spread varchar(11)
) engine=InnoDB  charset=utf8;

select * from j_stocks;


create table a_stocks(
id int not null primary key auto_increment,
indexs varchar(11),
stock varchar(11),
spread varchar(11)
) engine=InnoDB  charset=utf8;


create table hk_stocks(
id int not null primary key auto_increment,
indexs varchar(11),
stock varchar(11),
spread varchar(11)
) engine=InnoDB  charset=utf8;



create table us_stocks(
id int not null primary key auto_increment,
indexs varchar(11),
stock varchar(11),
spread varchar(11)
) engine=InnoDB  charset=utf8;