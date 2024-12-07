drop database if exists iclr2025;
create database iclr2025;
use iclr2025;
drop table if exists rating;
drop table if exists article;
create table article (
    year int not null,
    id int primary key auto_increment,
    serial int not null,
    title varchar(512) not null,
    author varchar(255),
    keywords varchar(2048) not null,
    abstract_file_link varchar(255) not null,
    tl_dr text,
    primary_area varchar(512) not null,
    download_link varchar(255) not null
);
create table rating (
    id int primary key auto_increment,
    article_id int not null,
    rating int not null,
    foreign key (article_id) references article(id)
);
