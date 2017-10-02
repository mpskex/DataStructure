drop table if exists files;
create table FILES (
  ID        integer primary key,
  TITLE     text not null,
  FILEPATH  text not null
); 