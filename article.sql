drop database if exists iclr;
create database iclr;
use iclr;
drop table if exists rating;
drop table if exists article;
create table article (
    year int not null,
    id int primary key auto_increment,
    serial int not null,
    title varchar(255) not null,
    author varchar(255),
    keywords varchar(255) not null,
    abstract text not null,
    tl_dr text,
    primary_area varchar(255) not null,
    download_link varchar(255) not null
);
create table rating (
    id int primary key auto_increment,
    article_id int not null,
    rating int not null,
    foreign key (article_id) references article(id)
);
