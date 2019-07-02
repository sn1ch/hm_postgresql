import psycopg2
from datetime import datetime, timedelta
from pprint import pprint

authorization = "dbname=hm_postgressql_db user=sn1ch password=1234"


def create_db():  # создает таблицы
    with psycopg2.connect(authorization) as conn:
        with conn.cursor() as cur:
            cur.execute("""create table student (
                id serial primary key,
                name varchar(100),
                gpa numeric(10, 2),
                birth timestamp with time zone);
                """)
            cur.execute("""create table course (
                id serial primary key,
                name varchar(100));
                """)
            cur.execute("""create table student_course (
                id serial primary key,
                student_id integer references student(id),
                course_id integer references course(id));
                """)


def get_students(course_id):  # возвращает студентов определенного курса
    with psycopg2.connect(authorization) as conn:
        with conn.cursor() as cur:
            cur.execute(
                'select student.name, course_id from student_course '
                'join student on student_course.student_id = student.id')
            cur.execute('select student.name from student_course '
                        'join student on student_course.student_id = student.id where course_id=(%s)', (course_id,))
            return print(cur.fetchall())


def add_students(course_id, students):  # создает студентов и
    # записывает их на курс
    with psycopg2.connect(authorization) as conn:
        with conn.cursor() as cur:
            for student in students:
                cur.execute('insert into student (name, gpa, birth) values (%s, %s, %s)',
                            (list(student.values())[0], list(student.values())[1], list(student.values())[2]))
            cur.execute('select * from student')
            students_list = cur.fetchall()
            for student in students_list:
                for _ in range(len(students)):
                    if student[1] == students[_]['name']:
                        cur.execute('insert into student_course (student_id, course_id) values (%s, %s)',
                                    (student[0], course_id))


def add_student(**student):  # просто создает студента
    with psycopg2.connect(authorization) as conn:
        with conn.cursor() as cur:
            cur.execute('insert into student (name, gpa, birth) values (%s, %s, %s)',
                        (list(student.values())[0], list(student.values())[1], list(student.values())[2]))


def get_student(student_id):
    with psycopg2.connect(authorization) as conn:
        with conn.cursor() as cur:
            cur.execute('select * from student where id=(%s)', (student_id,))
            return print(cur.fetchall())


if __name__ == '__main__':
    now = datetime.now()
    long_ago = now - timedelta(days=365 * 30)
    long_ago2 = now - timedelta(days=365 * 10)
    long_ago3 = now - timedelta(days=365 * 5)

    students = [
        {'name': 'Mr Black2',
         'gpa': 3.4,
         'birth': long_ago},
        {'name': 'Mr Pink2',
         'gpa': 2,
         'birth': long_ago2},
        {'name': 'Mr Blue2',
         'gpa': 4.7,
         'birth': long_ago2}
    ]

    create_db()
    add_student(name='Jnon Pen', gpa=2, birth=long_ago3)
    get_student(22)
    get_students(1)
    add_students(1, students)
