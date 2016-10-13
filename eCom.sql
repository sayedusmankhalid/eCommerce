DROP DATABASE IF EXISTS ecom;
CREATE DATABASE ecom;
\c ecom
create extension pgcrypto;

CREATE TABLE users (
  username varchar(12) NOT NULL,
  password varchar(100) NOT NULL,
  firstName varchar(50) NOT NULL,
  lastName varchar(50) NOT NULL,
  address varchar(100) NOT NULL,
  city varchar(100) NOT NULL,
  state varchar(50) NOT NULL,
  zip varchar(15) NOT NULL,
  country varchar(50) NOT NULL,
  email varchar(100)NOT NULL,
  
  PRIMARY KEY (username)
);

CREATE TABLE products (
  id serial NOT NULL,
  name text NOT NULL,
  description text NOT NULL,
  price decimal NOT NULL,
  quantity int NOT NULL,
  image text,
  date_posted date NOT NULL,
  seller_name text NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY (seller_name) REFERENCES users(username)
);

CREATE TABLE cart (
  username text NOT NULL,
  product_id int NOT NULL,
  quantity int NOT NULL,
  PRIMARY KEY(username, product_id),
  FOREIGN KEY(username) REFERENCES users(username),
  FOREIGN KEY(product_id) REFERENCES products(id)
);

INSERT INTO users (username,password,firstName,lastName,Address,city, state,zip,country,email) values
('usman',crypt('usman',gen_salt('bf')),'Usman','Khalid','8 Woodland Ter','Fredericksburg','VA','22401','USA','test@gmail.com');
