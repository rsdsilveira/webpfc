drop table if exists houseStates;

create table houseStates(
  db_id integer primary key autoincrement,
  userName integer,
  room integer,
  light boolean,
  temperature integer,
  curtain boolean,
  hourOfDay float
);