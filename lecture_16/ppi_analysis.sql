

-- PPI network analysis
-- DS3000 / DS5110

-- count how many times a protein in the 'a' column
-- occurs

select * from ppi

drop view if exists degree_distribution

create view degree_distribution as
select num_interactions, count(*) as frequency
from
(
select a, count(*) as num_interactions
from ppi
group by a
order by num_interactions desc
)
group by num_interactions
order by frequency desc

select *
from degree_distribution


drop view if exists degcount

create view degcount as
select a, count(*) adjacent
from ppi
group by a 
order by adjacent desc

select * from degcount



select *
from ppi
where a in (select a from degcount where adjacent > 100)
and b in (select a from degcount where adjacent > 100)




