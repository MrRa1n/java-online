drop table if exists users;
drop table if exists roles;
drop table if exists challenges;
drop table if exists user_roles;
drop table if exists code;
drop table if exists resources;
drop table if exists code;
drop table if exists users_challenges;

create table users (
    user_id serial primary key,
    username text unique not null,
    password text not null,
    email text unique not null,
    avatar_url text,
    experience_points integer default 0 not null,
    created_on timestamp not null,
    last_login timestamp
);

create table roles (
    role_id serial primary key,
    role_name text unique not null
);

create table challenges (
    challenge_id serial primary key,
    title text not null,
    instructions text not null
);

create table user_roles (
    user_id int references users(user_id) on delete cascade,
    role_id int references roles(role_id) on delete cascade,
    grant_date timestamp
);

create type code_t as enum('template','submission','test');

create table code (
    code_id serial primary key,
    code_url text,
    type code_t not null,
    user_id int references users(user_id),
    challenge_id int references challenges(challenge_id) on delete cascade
);

create table resources (
    resource_id serial primary key,
    resource_url text,
    challenge_id int references challenges(challenge_id) on delete cascade
);

create table users_challenges (
    user_id int references users (user_id),
    challenge_id int references challenges(challenge_id) on update cascade on delete cascade
);
