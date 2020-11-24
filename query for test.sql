SELECT * FROM customer;
SELECT * FROM ordert;
SELECT * FROM deliveryman;
SELECT * FROM owner;
SELECT * FROM restaurant;
SELECT * FROM promotion;
SELECT * FROM advertisement;
SELECT * FROM product;
SELECT * FROM transaction;
SELECT * FROM order_have_product;
SELECT * FROM receive_order;
SELECT * FROM order_use_promotion;
SELECT * FROM review_restaurant;
SELECT * FROM review_product;
SELECT * FROM restaurant_tag;
SELECT * FROM product_tag;
SELECT * FROM orderUpdateTime;
SELECT * FROM transactionUpdateTime;

SELECT odid, calculateTotalPrice(odid) as total_price from ordert order by odid;

SELECT rname, pdname, pdtag FROM product NATURAL JOIN product_tag NATURAL JOIN restaurant WHERE pdtag IN ('salad','pizza');

SELECT R.rname, P.pdname, PT2.pdtag FROM restaurant R, product P, (SELECT * FROM product_tag PT WHERE PT.pdtag IN ('salad','pizza') ) AS PT2 WHERE PT2.pdid = P.pdid AND P.rid = R.rid;