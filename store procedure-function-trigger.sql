# if get [Error Code: 1417 This function has none of DETERMINISTIC...] run this command
# SET GLOBAL log_bin_trust_function_creators = 1;
DELIMITER $$
CREATE FUNCTION DeliveryStatus(odstatus VARCHAR(15))
	RETURNS BOOL
	DETERMINISTIC
BEGIN
	DECLARE status BOOL;
	IF odstatus = 'deliver' THEN
		SET status = 0;
	ELSE
		SET status = 1;
	END IF;
	RETURN (status);
END $$
DELIMITER ;

DELIMITER $$
CREATE FUNCTION InsertNewOrder(cid INT(5), did INT(5))
	RETURNS INT(5)
BEGIN
	DECLARE new_odid INT(5);
    INSERT INTO ordert (cid,did) VALUES (cid,did);
    SET new_odid = LAST_INSERT_ID();-- 
    RETURN new_odid;
END $$
DELIMITER ;

DELIMITER $$
CREATE FUNCTION calculateTotalPrice(target_odid INT(5))
	RETURNS DOUBLE
	DETERMINISTIC
BEGIN
	DECLARE totalPrice DOUBLE;
    DECLARE discount DOUBLE;
    SET discount = 0;
    SELECT SUM(ohpdquantity*pdprice) INTO totalPrice
    FROM ordert NATURAL JOIN order_have_product NATURAL JOIN product 
    WHERE odid = target_odid GROUP BY odid;
    SELECT sum(pdiscount) INTO discount 
    FROM order_use_promotion NATURAL JOIN ordert NATURAL JOIN promotion 
    WHERE odid=target_odid GROUP BY odid;
    SET totalPrice = totalPrice - discount;
    RETURN (totalPrice);
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE UpdateOrderStatus(IN target_odid INT(5),IN new_status VARCHAR(15))
BEGIN
	SET autocommit=0;
	START TRANSACTION;
	UPDATE ordert SET odstatus=new_status WHERE odid=target_odid;
	UPDATE deliveryman SET dstatus=DeliveryStatus(new_status) WHERE did=( SELECT did FROM ordert O WHERE O.odid=target_odid );
    COMMIT;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE searchCustomerID(IN target_cid INT(5))
BEGIN
    DECLARE c INT;
    DECLARE i INT;
    DECLARE od_id INT;
    SET i = 0;
    SELECT count(distinct(odid)) INTO c FROM ordert NATURAL JOIN order_have_product NATURAL JOIN product WHERE cid = target_cid;
    loop1: LOOP
		IF i<c THEN
			SELECT odid INTO od_id 
			FROM ordert NATURAL JOIN order_have_product NATURAL JOIN product 
			WHERE cid=target_cid GROUP BY odid LIMIT 1 OFFSET i;
			SELECT cid,odid,pdid,did,pdname,ohpdquantity,calculateTotalPrice(od_id) AS totalprice,odstatus,pdprice
			FROM ordert NATURAL JOIN order_have_product NATURAL JOIN product 
			WHERE cid=target_cid AND odid = od_id;
            SET i = i+1;
        ELSE
			LEAVE loop1;
        END IF;
	END LOOP loop1;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER orderLog
AFTER UPDATE ON ordert
FOR EACH ROW
BEGIN
	INSERT INTO orderUpdateTime VALUES (NEW.odid,NEW.odstatus,now());
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER transactionLog
AFTER INSERT ON transaction
FOR EACH ROW
BEGIN
	INSERT INTO transactionUpdateTime VALUES (NEW.tid,NEW.tbalance,now());
END $$
DELIMITER ;

CREATE INDEX productName ON product(pdname);