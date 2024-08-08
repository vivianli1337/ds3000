select *
from sqlite_master
where name like 'vsx'

CREATE TABLE "vsx" (
"index" INTEGER,
  "iod" INTEGER,
  "name" TEXT,
  "code" INTEGER,
  "type" TEXT,
  "min" REAL,
  "max" REAL,
  "period" REAL,
  "ra" REAL,
  "dec" REAL
)

select count(*) from vsx v 

-- Database Transformations
-- Sometimes the maximum is really the amplitude

drop view if exists vsx_corrected

create view vsx_corrected as 
select
    name,
    type as vartype,
    min, max,
    case when max - min < 0 then min + max else max end as maxadj,
    period
from vsx

select *
from vsx_corrected
where vartype = 'CEP'


select count(*) from miras

-- Observable
select
    name,
    vartype,
    min,
    maxadj as max,
    maxadj - min as amplitude,
    period
from vsx_corrected
where period is not null
and vartype = 'M'
--and min <= 4
--and amplitude > 2
order by period


--
