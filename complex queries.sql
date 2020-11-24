# complex queries

# 1 แสดงรายชื่อลูกค้าที่จ่ายเงินมากสุด3อันดับแรกของแต่ละร้านอาหาร รวมถึงราคาที่จ่ายของคนนั้นๆในแต่ละร้าน (ให้สมมติว่าลูกค้าใช้โปรโมชั่นทั้งหมดที่เป็นไปได้)
select restaurant, customer, total_price
from
(select restaurant, customer, total_price,
row_number() over (partition by restaurant order by total_price desc) as restaurant_rank
from 
(select r.rname as restaurant, c.cname as customer, 
SUM((ohp.ohpdquantity * pd.pdprice)  * if(CURDATE() <= p.penddate, (100-p.pdiscount)/100, 1)) as total_price
from customer c
natural join ordert o 
natural join order_have_product ohp
natural join product pd 
right join restaurant r on pd.rid = r.rid
left join promotion p on r.rid = p.rid
group by r.rid, c.cid) as stepone) as ranked
where restaurant_rank <= 3;

# 2 แสดงรายชื่ออาหารที่ได้ avg rating มากที่สุดของแต่ละร้าน ที่มีการ review อย่างน้อย 2 ครั้งขึ้นไป และไม่มี rating ครั้งไหนเป็น 0 รวมถึงแสดง avg rating ด้วย
select restaurant, product, avg_rating
from
(select restaurant, product, avg_rating,
row_number() over (partition by restaurant order by avg_rating desc) as restaurant_rank
from 
(select r.rname as restaurant, pd.pdname as product, avg(rp.rprate) as avg_rating
from restaurant r 
left join product pd on r.rid = pd.rid
natural join review_product rp
where rp.rprate != 0
group by r.rid, pd.pdid
having COUNT(distinct rp.tid) >= 2) as stepone) as ranked
where restaurant_rank <= 1;

# 3 3. แสดงรายชื่อ delivery man ที่มีเบอร์โทรขึ้นต้นด้วยเลข 0 และจัดส่งจำนวนรายการมากสุด   (โดยนับเฉพาะออเดอร์ที่มีจำนวนรายการอาหารสูงสุดของลูกค้าแต่ละคน) มาทั้งหมด 2 อันดับแรก รวมถึงจำนวนรายการที่จัดส่งตามเงื่อนไขด้วย
select delivery_man, SUM(order_quantity) as total_maxquantityorder_of_each_customer
from
(select customer, delivery_man, order_quantity
from
(select customer, delivery_man, order_quantity,
row_number() over (partition by customer order by order_quantity desc) as customer_rank
from 
(select c.cname as customer, d.dname as delivery_man, SUM(ohp.ohpdquantity) as order_quantity
from customer c 
natural join ordert od
natural join order_have_product ohp
natural join product pd
natural join deliveryman d
where d.dphonenum like '0%'
group by od.odid) as stepone) as ranked
where customer_rank = 1) as steptwo
group by delivery_man
order by total_maxquantityorder_of_each_customer desc
limit 3;











