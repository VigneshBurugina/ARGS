use info;
create table teacher (empid int primary key,name varchar(30),class varchar(5),phone char(10),email varchar(30));
create table student (admno int,name varchar(30),class varchar(5),DOB date,fathername varchar(30),mothername varchar(30),phone char(10),address varchar(100), email varchar(30),primary key (admno,name));
