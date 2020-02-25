
\c pgdata

create table todos (
  id serial primary key,
  done boolean not null default false,
  task text not null,
  due timestamptz
);

insert into todos (task) values
  ('finish tutorial 0'), ('pat self on back');


