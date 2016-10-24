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
  catagory_name text NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY (seller_name) REFERENCES users(username)
);

INSERT INTO users (username,password,firstName,lastName,Address,city, state,zip,country,email) values
('usman',crypt('usman',gen_salt('bf')),'Usman','Khalid','8 Woodland Ter','Fredericksburg','VA','22401','USA','test1@gmail.com');
INSERT INTO users (username,password,firstName,lastName,Address,city, state,zip,country,email) values
('koy',crypt('koy',gen_salt('bf')),'Koy','Voss','14 Whitestone Dr','Stafford','VA','22556','USA','test2@gmail.com');

insert into products(name, description, price, quantity, date_posted, seller_name, catagory_name)values('iphone','best iphone ever',110,3,'2016-01-13','usman','electronics');

--select users.username, products.name, products.description from users join products on products.seller_name ='usman';--
--select products.name from cart join products on cart.product_id = products.id; --