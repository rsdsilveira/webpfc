drop table if exists devices;
drop table if exists events;

create table devices (
  db_id integer primary key autoincrement,
  name text,
  kind integer, 
  status text,
  mask text,
  micro_id integer,
  localization text
);

create table events (
  db_id integer primary key autoincrement,
  status text,
  operator integer,
  mic_id integer,
  occurred_at timestamp,
  foreign key(mic_id) references devices(micro_id)
); 
