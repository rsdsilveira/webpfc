drop table if exists houseStates;

create table houseStates(
  db_id integer primary key autoincrement,
  [user] integer,
  room integer,
  light boolean,
  temperature integer,
  curtain boolean,
  hourOfDay float
);