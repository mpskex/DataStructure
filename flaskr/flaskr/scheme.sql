drop table if exists USERS;
CREATE TABLE USERS(
  UserID  text  primary key,
  UserName  text,
  Passwd text not null,
  sessionID text not null
);