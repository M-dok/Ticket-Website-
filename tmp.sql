SELECT * FROM gigs;
SELECT price FROM gigs;
SELECT * FROM reviews;
SELECT * FROM user_info;
SELECT * FROM purchases;

SELECT * FROM gigs WHERE genre='EDM' AND NOT gig_id  = 5;
SELECT * FROM gigs 
WHERE NOT gig_id = 5 ORDER BY RANDOM() LIMIT 3;