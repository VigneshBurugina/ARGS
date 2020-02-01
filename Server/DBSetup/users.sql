use users;
create table users (username varchar(30) primary key,passhash varchar(500) unique not null,type char(3) not null);
create table user_admno (username varchar(30),admno int,foreign key (admno) references info.student(admno));