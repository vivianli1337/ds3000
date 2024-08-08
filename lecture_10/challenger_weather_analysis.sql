-- show tables
SELECT name FROM sqlite_master WHERE type='table'

-- specific station columns stations near the cape
select station, lat, lon
from stations
where station <> '' 
and lat != '' and lat != 0 and lon != '' and lon != 0
and lat between 28.0 and 28.8
and lon between -80.8 and -80.4
order by lat


-- join with temperatures
select s.station, lat, lon, month, day, F
from stations s join temps t using (station)
where station <> '' 
and lat != '' and lat != 0 and lon != '' and lon != 0
and lat between 28.0 and 28.8
and lon between -80.8 and -80.4
and month = 1
order by day, F

-- Now perform the aggregation

-- Method 1: Using a view
create view jan_data as
select s.station, lat, lon, month, day, F
from stations s join temps t using (station)
where station <> '' 
and lat != '' and lat != 0 and lon != '' and lon != 0
and lat between 28.0 and 28.8
and lon between -80.8 and -80.4
and month = 1
order by day, F

select *
from jan_data

select day, avg(F)
from jan_data
group by day

-- Method 2: Using a subquery
select day, round(avg(F), 1)
from
(
select s.station, lat, lon, month, day, F
from stations s join temps t using (station)
where station <> '' 
and lat != '' and lat != 0 and lon != '' and lon != 0
and lat between 28.0 and 28.8
and lon between -80.8 and -80.4
and month = 1
order by day, F
)
group by day
order by day


-- Method 3: Avoid both a view and the subquery
select day, avg(F)
from stations s join temps t using (station)
where station <> '' 
and lat != '' and lat != 0 and lon != '' and lon != 0
and lat between 28.0 and 28.8
and lon between -80.8 and -80.4
and month = 1
group by day
order by day

