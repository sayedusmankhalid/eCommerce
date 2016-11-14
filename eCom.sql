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
  id varchar(100) NOT NULL,
  name text NOT NULL,
  description text NOT NULL,
  price decimal NOT NULL,
  quantity int NOT NULL,
  image text,
  date_posted date NOT NULL,
  seller_name text NOT NULL,
  catagory_name text NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY (seller_name) REFERENCES users(username)
);

CREATE TABLE sellerproducts (
  username varchar(12) NOT NULL,
  product_id text NOT NULL,
  PRIMARY KEY(username, product_id),
  FOREIGN KEY(username) REFERENCES users(username),
  FOREIGN KEY(product_id) REFERENCES products(id)
);

INSERT INTO users (username,password,firstName,lastName,Address,city, state,zip,country,email) values
('usman',crypt('usman',gen_salt('bf')),'Usman','Khalid','8 Woodland Ter','Fredericksburg','VA','22401','USA','test1@gmail.com');
INSERT INTO users (username,password,firstName,lastName,Address,city, state,zip,country,email) values
('koy',crypt('koy',gen_salt('bf')),'Koy','Voss','14 Whitestone Dr','Stafford','VA','22556','USA','test2@gmail.com');

insert into products(id,name, description, price, quantity, date_posted, seller_name, catagory_name)values('1','iphone','best iphone ever',110,3,'2016-01-13','usman','electronics');
insert into products(id, name, description, price, quantity, date_posted, seller_name, catagory_name)values('2','iphone','best iphone ever',110,3,'2016-01-13','koy','electronics');

INSERT INTO sellerproducts(username, product_id) VALUES ('koy', 2), ('usman', 1);

Grant ALL on users to usman;
Grant ALL on products to usman;
Grant All on sellerproducts to usman;

