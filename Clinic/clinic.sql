drop table if exists doctor, specialization, timetable, patient, appointment, prescription;

create table specialization(
    id serial primary key,
    spec_name varchar(30) not null
);

create table doctor(
    id serial primary key,
    last_name varchar(30) not null,
    first_name varchar(30) not null,
    middle_name varchar(30),
    id_specialization int not null,
    foreign key (id_specialization) references specialization(id)
);

create table timetable(
    id serial primary key,
    weekday varchar(30) not null,
    id_doctor int not null ,
    foreign key (id_doctor) references doctor(id)
);

create table patient(
    id serial primary key,
    last_name varchar(30) not null,
    first_name varchar(30) not null,
    middle_name varchar(30),
    email varchar(50),
    snils varchar(30) not null
);

create table appointment(
    id serial primary key,
    weekdate varchar(30) not null,
    type_app varchar(30) not null,
    id_patient int not null,
    id_doctor int not null,
    foreign key (id_patient) references patient(id),
    foreign key (id_doctor) references doctor(id)
);

create table prescription(
    id serial primary key,
    drugs varchar(50),
    id_patient int not null,
    id_doctor int not null,
    foreign key (id_patient) references patient(id),
    foreign key (id_doctor) references doctor(id)
);
--Заполнение таблиц--
insert into specialization(id, spec_name)
values (1, 'Стоматолог'),
       (2, 'Невролог'),
       (3, 'Гинеколог'),
       (4, 'Педиатр'),
       (5, 'Хирург'),
       (6, 'Проктолог'),
       (7, 'Терапевт'),
       (8, 'Диетолог'),
       (9, 'Психотерапевт');

insert into doctor(id, last_name, first_name, middle_name, id_specialization)
values (1, 'Волошина', 'Наталья', 'Анатольевна', 1),
       (2, 'Плетнёва', 'Наталья', 'Геннадьевна', 2),
       (3, 'Жорник', 'Татьяна', 'Михайловна', 3),
       (4, 'Васильченко', 'Надежда', 'Георгиевна', 4),
       (5, 'Окладной', 'Борис', 'Анатольевич', 5),
       (6, 'Шмаков', 'Владимир', 'Николаевич', 6),
       (7, 'Аманатова', 'Ирина', 'Сергеевна', 7),
       (8, 'Непомнящих', 'Ирина', 'Сергеевна', 8),
       (9, 'Арсеньева', 'Ольга', 'Геннадьевна', 9);

insert into timetable(weekday, id_doctor)
values ('2021-05-24', 3),
       ('2021-05-24', 8),
       ('2021-05-24', 4),
       ('2021-05-24', 2),
       ('2021-05-25', 8),
       ('2021-05-25', 9),
       ('2021-05-25', 6),
       ('2021-05-25', 5),
       ('2021-05-26', 2),
       ('2021-05-26', 8),
       ('2021-05-26', 7),
       ('2021-05-26', 4),
       ('2021-05-27', 6),
       ('2021-05-27', 1),
       ('2021-05-27', 2),
       ('2021-05-27', 9),
       ('2021-05-28', 4),
       ('2021-05-28', 6),
       ('2021-05-28', 7),
       ('2021-05-28', 2),
       ('2021-05-29', 4),
       ('2021-05-29', 1),
       ('2021-05-29', 3),
       ('2021-05-30', 5),
       ('2021-05-30', 6),
       ('2021-05-30', 9);

--ФУНКЦИИ--
--Показать расписание--
select timetable.weekday as work_time, doctor.last_name, doctor.first_name, doctor.middle_name, specialization.spec_name as doctor_specialization
from doctor
    inner join specialization on doctor.id_specialization = specialization.id
    inner join timetable on doctor.id = timetable.id_doctor;
--Добавить нового пациента--
drop function if exists add_patient(l_name varchar(30) , f_name varchar(30), m_name varchar(30), eemail varchar(50), ssnils varchar(30), doctor_id int);

create or replace function add_patient(l_name varchar(30) , f_name varchar(30), m_name varchar(30), eemail varchar(50), ssnils varchar(30), doctor_id int) returns varchar as
$$
declare
    pat_id int;
    doc_id int;
begin
    select id from doctor where id = doctor_id into doc_id;
    insert into patient(last_name, first_name, middle_name, email, snils)
    values (l_name, f_name, m_name, eemail, ssnils);
    select id from patient where last_name = l_name and first_name = f_name and middle_name = m_name and email = eemail and snils = ssnils into pat_id;
    insert into appointment(id_doctor, id_patient, weekdate, type_app)
    values (doc_id, pat_id, now(), 'Первичный');
    return 'Пациент зарегестрирован';
exception
    when others then return 'ERROR';
end$$
language plpgsql;
--Выписать пациента--
drop function if exists delete_patient(pat_id int);

create or replace function delete_patient(pat_id int) returns varchar as
$$
begin
    delete from appointment where id_patient = pat_id;
    delete from prescription where id_patient = pat_id;
    delete from patient where id = pat_id;
    return 'Пациент выписан';
exception
    when others then return 'ERROR22';
end$$
language plpgsql;
--Добавить новый рецепт--
drop function if exists prescription_patient(drug varchar(50), patient_id int, doctor_id int);

create or replace function prescription_patient(drug varchar(50), patient_id int, doctor_id int) returns varchar  as
$$
declare
    pat_id int;
    doc_id int;
begin
    select id from doctor where id = doctor_id into doc_id;
    select id from patient where id = patient_id into pat_id;
    insert into prescription(drugs, id_patient, id_doctor)
    values (drug, pat_id, doc_id);
    return 'Рецепт зарегестрирован';
exception
    when others then return 'ERROR';
end$$
language plpgsql;

