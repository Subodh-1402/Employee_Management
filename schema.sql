create table users( id integer primary key AUTOINCREMENT, name text not null, password text not null, admin boolean not null DEFAULT '0');

create table emp (empid integer primary key AUTOINCREMENT, name text not null, email text, phone integer, address text, joining_date default CURRENT_DATE);