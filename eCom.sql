DROP DATABASE IF EXISTS ecom;
CREATE DATABASE ecom;
\c ecom
create extension pgcrypto;

CREATE TABLE users (
  id serial NOT NULL,
  username varchar(12) NOT NULL,
  password varchar(100) NOT NULL,
  firstName varchar(50) NOT NULL,
  lastName varchar(50) NOT NULL,
  address varchar(100) NOT NULL,
  city varchar(100) NOT NULL,
  state varchar(50) NOT NULL,
  country varchar(50) NOT NULL,
  zip varchar(15) NOT NULL,
  
  PRIMARY KEY (username)
);

INSERT INTO users (username,password,firstName,lastName,Address,city, state,country,zip) values
('usman',crypt('usman',gen_salt('bf')),'Usman','Khalid','8 Woodland Ter','Fredericksburg','VA','USA','22401');