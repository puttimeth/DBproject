CREATE TABLE deliveryman(
	did INT(5) AUTO_INCREMENT,
	dname VARCHAR(45) NOT NULL,
	dphonenum VARCHAR(10) NOT NULL,
	dlicense VARCHAR(10) NOT NULL,
	dstatus BOOL NOT NULL DEFAULT 1,
	PRIMARY KEY (did)
);

CREATE TABLE customer(
	cid INT(5) AUTO_INCREMENT,
	cname VARCHAR(45) NOT NULL,
	caddress VARCHAR(125) NOT NULL,
    cphonenum VARCHAR(10) NOT NULL,
    cbankacc VARCHAR(25),
	cstatus BOOL NOT NULL DEFAULT 0,
	PRIMARY KEY (cid)
);
CREATE TABLE owner(
	oid INT(5) AUTO_INCREMENT,
    oname VARCHAR(45) NOT NULL,
    oaddress VARCHAR(125),
    ophonenum VARCHAR(10) NOT NULL,
    obankacc VARCHAR(25),
    ostatus BOOL NOT NULL DEFAULT 0,
    overified BOOL NOT NULL DEFAULT 0,
    PRIMARY KEY (oid)
);
CREATE TABLE restaurant(
	rid INT(5) AUTO_INCREMENT,
    rname VARCHAR(45) NOT NULL,
    raddress VARCHAR(125) NOT NULL,
    rphonenum VARCHAR(10) NOT NULL,
    rstatus BOOL NOT NULL DEFAULT 0,
    oid INT(5) NOT NULL,
    PRIMARY KEY (rid),
    FOREIGN KEY (oid) REFERENCES owner(oid) ON DELETE CASCADE
);
CREATE TABLE ordert(
	odid INT(5) AUTO_INCREMENT,
	cid INT(5) NOT NULL,
	did INT(5) NOT NULL,
	odstatus VARCHAR(15) NOT NULL DEFAULT 'in process',
	PRIMARY KEY (odid),
	FOREIGN KEY (cid) REFERENCES customer(cid) ON DELETE CASCADE,
	FOREIGN KEY (did) REFERENCES deliveryman(did) ON DELETE CASCADE
);
CREATE TABLE promotion(
	pid INT(5) AUTO_INCREMENT,
    pdes VARCHAR(300) NOT NULL,
    pdiscount DOUBLE(5,2) NOT NULL,
    penddate DATETIME NOT NULL,
    rid INT(5) NOT NULL,
    PRIMARY KEY (pid),
    FOREIGN KEY (rid) REFERENCES restaurant(rid) ON DELETE CASCADE,
    CHECK (pdiscount>0)
);
CREATE TABLE advertisement(
	aid INT(5) AUTO_INCREMENT,
    ades VARCHAR(100) NOT NULL,
    rid INT(5) NOT NULL,
    PRIMARY KEY (aid),
    FOREIGN KEY (rid) REFERENCES restaurant(rid) ON DELETE CASCADE
);
CREATE TABLE product(
	pdid INT(5) AUTO_INCREMENT,
    pdname VARCHAR(45) NOT NULL,
    rid INT(5) NOT NULL,
    pdprice DOUBLE(5,2) NOT NULL,
    PRIMARY KEY (pdid),
    FOREIGN KEY (rid) REFERENCES restaurant(rid) ON DELETE CASCADE,
    CHECK (pdprice>0)
);
CREATE TABLE order_have_product(
	odid INT(5),
    pdid INT(5),
    ohpdquantity INT(5),
    PRIMARY KEY (odid,pdid),
    FOREIGN KEY (odid) REFERENCES ordert(odid) ON DELETE CASCADE,
    FOREIGN KEY (pdid) REFERENCES product(pdid) ON DELETE CASCADE,
    CHECK (ohpdquantity>0)
);
CREATE TABLE receive_order(
	rid INT(5),
    odid INT(5),
    PRIMARY KEY (rid,odid),
    FOREIGN KEY (rid) REFERENCES restaurant(rid) ON DELETE CASCADE,
    FOREIGN KEY (odid) REFERENCES ordert(odid) ON DELETE CASCADE
);
CREATE TABLE order_use_promotion(
	odid INT(5),
    pid INT(5),
    PRIMARY KEY (odid,pid),
    FOREIGN KEY (odid) REFERENCES ordert(odid) ON DELETE CASCADE,
    FOREIGN KEY (pid) REFERENCES promotion(pid) ON DELETE CASCADE
);
CREATE TABLE restaurant_tag(
	rid INT(5),
    rtag VARCHAR(45) NOT NULL,
    PRIMARY KEY (rid,rtag),
    FOREIGN KEY (rid) REFERENCES restaurant(rid) ON DELETE CASCADE
);
CREATE TABLE product_tag(
	pdid INT(5),
    pdtag VARCHAR(45) NOT NULL,
    PRIMARY KEY (pdid,pdtag),
    FOREIGN KEY (pdid) REFERENCES product(pdid) ON DELETE CASCADE
);
CREATE TABLE promotion_condition(
	pid INt(5),
    pcondition VARCHAR(300) NOT NULL,
    PRIMARY KEY (pid,pcondition),
    FOREIGN KEY (pid) REFERENCES promotion(pid) ON DELETE CASCADE
);
CREATE TABLE transaction(
	tid INT(5) AUTO_INCREMENT,
    tbalance INT(5) NOT NULL,
    odid INT(5) NOT NULL,
    PRIMARY KEY (tid),
    FOREIGN KEY (odid) REFERENCES ordert(odid) ON DELETE CASCADE,
    CHECK (tbalance>0)
);
CREATE TABLE review_restaurant(
    rid INT(5),
    tid INT(5),
    rrdes VARCHAR(100) NOT NULL,
    rrrate DOUBLE(5,2) NOT NULL,
    PRIMARY KEY (rid,tid),
    FOREIGN KEY (rid) REFERENCES restaurant(rid) ON DELETE CASCADE,
    FOREIGN KEY (tid) REFERENCES transaction(tid) ON DELETE CASCADE,
    CHECK (rrrate>=0 AND rrrate<=5)
);
CREATE TABLE review_product(
    pdid INT(5),
    tid INT(5),
    rpdes VARCHAR(100) NOT NULL,
    rprate DOUBLE(5,2) NOT NULL,
    PRIMARY KEY (pdid,tid),
    FOREIGN KEY (pdid) REFERENCES product(pdid) ON DELETE CASCADE,
    FOREIGN KEY (tid) REFERENCES transaction(tid) ON DELETE CASCADE,
    CHECK (rprate>=0 AND rprate<=5)
);
# trigger table
CREATE TABLE orderUpdateTime(
	odid INT(5),
	new_status VARCHAR(15) NOT NULL,
	time DATETIME NOT NULL,
    FOREIGN KEY (odid) REFERENCES ordert(odid) ON DELETE CASCADE
);
CREATE TABLE transactionUpdateTime(
	tid INT(5),
	tbalance int(5),
	time DATETIME NOT NULL,
    FOREIGN KEY (tid) REFERENCES transaction(tid) ON DELETE CASCADE
);