import json
import os
import random
from django.core.management.base import BaseCommand

from studies.models import (
    AcademicGroup,
    Student,
    StudyDirection,
    Subject,
    SexStudent,
)

FILEPATH = os.path.abspath(os.path.dirname(__file__))


def generate_studydirection():
    """Заполнение направление подготовки
    """
    file = open(f'{FILEPATH}/studydirection.json', 'r')
    data = json.load(file)
    for sd in data:
        check_exists = StudyDirection.objects.filter(name=sd['name'])
        if check_exists:
            print(f"{sd['name']} уже есть")
        else:
            StudyDirection.objects.create(
                **sd,
            )
    file.close()


def generate_academicgroups():
    """Заполнение учебных групп
    """
    file = open(f'{FILEPATH}/academicgroups.json', 'r')
    data = json.load(file)
    for sd in data:
        check_exists = AcademicGroup.objects.filter(short_name=sd['short_name'])
        if check_exists:
            print(f"{sd['short_name']} уже есть")
        else:
            AcademicGroup.objects.create(
                **sd,
            )
    file.close()


def generate_subject():
    """Заполнение направление подготовки
    """
    file = open(f'{FILEPATH}/subject.json', 'r')
    data = json.load(file)
    for sd in data:
        check_exists = Subject.objects.filter(name=sd['name'])
        if check_exists:
            print(f"{sd['name']} уже есть")
        else:
            subject = Subject(
                name=sd['name'],
            )
            subject.save()
            subject.study_direction.set(sd['study_direction'])
            subject.save()
    file.close()


def generate_students():
    """Заполнение направление подготовки
    """
    file = open(f'{FILEPATH}/students.json', 'r')
    data = json.load(file)
    available_groups = AcademicGroup.objects.all()
    sex_tuple = (
        SexStudent.female,
        SexStudent.male,
    )
    for group in available_groups:
        for s in sex_tuple:
            sex = s
            f_names = data['male_names'] if sex == '2' else data['female_names']
            l_names = data['last_names'] if sex == '2' else [f"{x}а" for x in data['last_names']]
            bdays = data['birthdays']
            for i in range(random.randint(3, 10)):
                if AcademicGroup.objects.get(pk=group.pk).students.count() <= 20:
                    f_name = random.sample(f_names, k=1)[0]
                    l_name = random.sample(l_names, k=1)[0]
                    bday = random.sample(bdays, k=1)[0]
                    Student.objects.create(
                        first_name=f_name,
                        last_name=l_name,
                        sex=sex,
                        academic_group=group,
                        birthday=bday,
                    )
    file.close()


class Command(BaseCommand):

    def handle(self, *args, **options):
        generate_studydirection()
        generate_academicgroups()
        generate_subject()
        generate_students()
