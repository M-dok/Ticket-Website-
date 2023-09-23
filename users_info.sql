DROP TABLE IF EXISTS user_info;

CREATE TABLE user_info
(
    user_id INTEGER  PRIMARY KEY AUTOINCREMENT ,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);


DROP TABLE IF EXISTS gigs;
CREATE TABLE gigs
(
    gig_id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_name TEXT NOT NULL,
    gig_venue TEXT NOT NULL ,
    gig_date TEXT NOT NULL,
    genre TEXT NOT NULL,
    price INTEGER NOT NULL,
    num_of_tickets INTEGER NOT NULL
); 
INSERT INTO gigs(artist_name,gig_venue,gig_date,genre,price,num_of_tickets) 
VALUES('Metallica','Croke Park','2024-Jun-04','Rock',15,200),
       ('Drake','Aviva Stadium','2023-Mar-05','Rap',50,0),
       ('Pink Floyd','O2 Arena','2024-Nov-14','Rock',35,100),
       ('Calvin Harris','Radio City Music Hall ','2026-Aug-26','Pop',80,2),
       ('Bruno Mars','Páirc Uí Chaoimh','2023-Aug-15','Pop',45,0),
       ('Red Hot Chili Peppers','Button Factory','2023-Jan-01','Rock',25,0),
       ('Kendrick Lamar','The Gorge Amphitheatre','2024-Feb-09','Rap',65,1),
       ('Injury Reserve','Academy(Dublin)','2023-Nov-07','Rap',15,25),
       ('King Crimson','Hyde Park','2025-Jul-05','Rock',45,60),
       ('The Weekend','Festspielhaus Baden-Baden','2024-Oct-17','Pop',80,0),
       ('Daft Punk','3Areana','2024-Apr-18','EDM',65,10),
       ('MF Doom','Motion','2023-Apr-23','Rap',50,10),
       ('Black Country,New Road','Aviva Stadium','2023-Apr-23','Rock',45,0),
       ('Justice','Aviva Stadium','2023-Apr-25','EDM',45,0),
       ('Avicii ','Aviva Stadium','2023-Jun-23','EDM',45,0);


DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews 
(
    review_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    gig_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    artist_name TEXT NOT NULL,
    review TEXT NOT NULL, 
    score INTEGER NOT NULL

); 

DROP TABLE IF EXISTS purchases;

CREATE TABLE purchases
(
    purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    gig_id INTEGER NOT NULL,
    artist_name TEXT NOT NULL,
    gig_venue TEXT NOT NULL ,
    gig_date TEXT NOT NULL,
    price INTEGER NOT NULL
);

