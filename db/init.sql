create user postgres_test_user password 'any_password_you_know';

create database postgres_test_db encoding 'utf-8';
grant all privileges on database postgres_test_db to postgres_test_user;
alter database postgres_test_db owner to postgres_test_user;

