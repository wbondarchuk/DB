import psycopg2 as lib
import datetime


def Greeting():
    print('        ===========        ')
    print('        ===========        ')
    print('        ===========        ')
    print('        ===========        ')
    print('===========================')
    print('Программа УмНаЯ Поликлиника')
    print('===========================')
    print('        ===========        ')
    print('        ===========        ')
    print('        ===========        ')
    print('        ===========        ')
    print('Вот что я умею:\n')
    print('0. Посмотреть расписание специалистов\n'
          '1. Добавить пациента\n'
          '2. Посмотреть и выписать пациента\n'
          '3. Назначить лекарства\n')
    print('Введите номер функции')
    print('Вы ввели:\n')
    num = int(input())
    if num < 0 or num > 3:
        print('Что-то не так, введите число от 0 до 3!')
        return -2
    return num


def View_doctors():
    db1 = lib.connect(dbname="postgres", user="postgres", password="tv1cssdh", host="127.0.0.1", port="5433")
    mycursor1 = db1.cursor()
    try:
        print('Дата приема     Фамилия    Имя     Отчество      Специализация')
        mycursor1.execute(
            'select timetable.weekday as work_time, doctor.last_name, doctor.first_name, doctor.middle_name, '
            'specialization.spec_name as doctor_specialization from doctor inner join specialization on '
            'doctor.id_specialization = specialization.id inner join timetable on doctor.id = timetable.id_doctor;')
        for row in mycursor1:
            print(row)
        db1.commit()
    except (Exception, lib.DatabaseError) as error:
        print(error)
    finally:
        mycursor1.close()
        if db1 is not None:
            db1.close()


def Patient_data(l_name, f_name, m_name, eemail, ssnils, doctor_id):
    db2 = lib.connect(dbname="postgres", user="postgres", password="tv1cssdh", host="127.0.0.1", port="5433")
    mycursor2 = db2.cursor()
    try:
        mycursor2.execute('select * from add_patient(%(p1)s,%(p2)s,%(p3)s,%(p4)s,%(p5)s,%(p6)s);',
                          {"p1": l_name, "p2": f_name, "p3": m_name, "p4": eemail, "p5": ssnils, "p6": doctor_id})
        for row in mycursor2:
            print(row)
        db2.commit()
    except (Exception, lib.DatabaseError) as error:
        print(error)
    finally:
        mycursor2.close()
        if db2 is not None:
            db2.close()


def Add_Patient():
    db2 = lib.connect(dbname="postgres", user="postgres", password="tv1cssdh", host="127.0.0.1", port="5433")
    mycursor2 = db2.cursor()
    try:
        print('ID   Фамилия     Имя       Отчество')
        mycursor2.execute('select id, last_name, first_name, middle_name from doctor')
        for row in mycursor2:
            print(row)
        db2.commit()
    except (Exception, lib.DatabaseError) as error:
        print(error)
    finally:
        mycursor2.close()
        if db2 is not None:
            db2.close()
    print('Введите свой ID:')
    doctor_id = int(input())
    print('\nВведите фамилию пациента:')
    l_name = str(input())
    print('\nВведите имя пациента:')
    f_name = str(input())
    print('\nВведите отчество пациента:')
    m_name = str(input())
    print('\nВведите email пациента:')
    eemail = str(input())
    print('\nВведите СНИЛС пациента:')
    ssnils = str(input())
    Patient_data(f_name, l_name, m_name, eemail, ssnils, doctor_id)


def Patient_cured(pat_id):
    db3 = lib.connect(dbname="postgres", user="postgres", password="tv1cssdh", host="127.0.0.1", port="5433")
    mycursor3 = db3.cursor()
    try:
        mycursor3.execute('select * from delete_patient(%(h)s);',
                          {"h": pat_id})
        for row in mycursor3:
            print(row)
        db3.commit()
    except (Exception, lib.DatabaseError) as error:
        print(error)
    finally:
        mycursor3.close()
        if db3 is not None:
            db3.close()


def Delete_Patient():
    db3 = lib.connect(dbname="postgres", user="postgres", password="tv1cssdh", host="127.0.0.1", port="5433")
    mycursor3 = db3.cursor()
    try:
        print('ID  Имя   Фамилия   Отчество    email   СНИЛС ')
        mycursor3.execute('select * from patient;')
        for row in mycursor3:
            print(row)
        db3.commit()
    except (Exception, lib.DatabaseError) as error:
        print(error)
    finally:
        mycursor3.close()
        if db3 is not None:
            db3.close()
    print('Введите ID выписываемого пациента или если хотите выйти введите 0:')
    pat_id = int(input())
    Patient_cured(pat_id)


def drugdiller(drug, patient_id, doctor_id):
    db4 = lib.connect(dbname="postgres", user="postgres", password="tv1cssdh", host="127.0.0.1", port="5433")
    mycursor4 = db4.cursor()
    try:
        mycursor4.execute('select * from prescription_patient(%(f1)s,%(f2)s,%(f3)s);',
                         {"f1": drug, "f2": patient_id, "f3": doctor_id})
        for row in mycursor4:
            print(row)
        db4.commit()
    except (Exception, lib.DatabaseError) as error:
        print(error)
    finally:
        mycursor4.close()
        if db4 is not None:
            db4.close()


def Give_Drugs():
    db4 = lib.connect(dbname="postgres", user="postgres", password="tv1cssdh", host="127.0.0.1", port="5433")
    mycursor4 = db4.cursor()
    try:
        print('ID  Имя   Фамилия   Отчество    email   СНИЛС ')
        mycursor4.execute('select * from patient;')
        for row in mycursor4:
            print(row)
        db4.commit()
        print('ID   Рецепт      ID_пациента        ID_врача')
        mycursor4.execute('select * from prescription;')
        for row in mycursor4:
            print(row)
        db4.commit()
    except (Exception, lib.DatabaseError) as error:
        print(error)
    finally:
        mycursor4.close()
        if db4 is not None:
            db4.close()
    print('Введите свой ID:')
    doctor_id = int(input())
    print('Введите ID пациента:')
    patient_id = int(input())
    print('\nВведите рецепт на лекарства:')
    drug = str(input())
    drugdiller(drug, patient_id, doctor_id)


operations = [View_doctors, Add_Patient, Delete_Patient, Give_Drugs]


def main():
    ACK = 1
    while ACK != 0:
        i = Greeting()
        if i == -2:
            print('Повторите попытку')
        else:
            action = operations[i]
            action()
            print('Продолжить?')
            print('Введите Да(1) или Нет(0):\n')
            ACK = int(input())
            if ACK == 0:
                print('До свидания!')


main()
