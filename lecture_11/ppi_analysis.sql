

select *
from ppi p 
limit 10


create view degree_distribution as
select num as degree, count(*) as frequency
from
(
select a, count(*) as num
from ppi p 
group by a 
order by num desc 
)
group by num 
order by frequency desc
