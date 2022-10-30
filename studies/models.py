from dataclasses import dataclass
from django.db import models

from users.models import (
    User,
)

MAX_STUDENTS_COUNT = 20


class StudyDirection(models.Model):
    """Направление подготовки
    """
    name = models.CharField(
        max_length=255,
        verbose_name='Наименование',
    )
    code = models.CharField(
        max_length=15,
        verbose_name='Код направления',
    )
    curator = models.OneToOneField(
        User,
        null=True,
        blank=True,
        verbose_name='Куратор',
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Направление подготовки'
        verbose_name_plural = 'Направления подготовки'


class Subject(models.Model):
    """Учебная дисциплина
    """
    name = models.CharField(
        max_length=255,
        verbose_name='Наименование',
    )
    study_direction = models.ManyToManyField(
        'StudyDirection',
        related_name='subjects',
    )

    def __str__(self) -> str:
        return self.name

    def study_direction_repr(self) -> str:
        """Репрезентация направлений подготовки
        Returns: str
        """
        return ', '.join(
            self.study_direction.values_list(
                'name',
                flat=True,
            )
        )

    class Meta:
        verbose_name = 'Учебная дисциплина'
        verbose_name_plural = 'Учебные дисциплины'


class AcademicGroup(models.Model):
    """Учебная группа
    """
    short_name = models.CharField(
        max_length=25,
    )
    study_direction = models.ForeignKey(
        'StudyDirection',
        on_delete=models.CASCADE,
        related_name='academic_group',
    )

    def __str__(self) -> str:
        return self.short_name

    def free_slots(self):
        """Возвращает количество свободных мест в группе
        """
        return MAX_STUDENTS_COUNT - self.students.count()

    def get_female_count(self):
        """Возвращает количество студентов женщин
        """
        return self.students.filter(
            sex=SexStudent.female,
        ).count()

    def get_male_count(self):
        """Возвращает количество студентов мужчин
        """
        return self.students.filter(
            sex=SexStudent.male,
        ).count()

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'


@dataclass
class SexStudent:
    """Пол студента
    """
    female: str = '1'
    male: str = '2'


class Student(models.Model):
    """Студент
    """
    first_name = models.CharField(
        max_length=30,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=30,
        verbose_name='Фамилия',
    )
    SEX_CHOICES = (
        (SexStudent.female, 'Женский'),
        (SexStudent.male, 'Мужской'),
    )
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        verbose_name='Пол',
    )
    birthday = models.DateField(
        verbose_name='Дата рождения',
    )
    academic_group = models.ForeignKey(
        'AcademicGroup',
        on_delete=models.CASCADE,
        verbose_name='Учебная группа',
        related_name='students',
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


@dataclass
class ReportStatus:
    ready: str = '1'
    pending: str = '2'


class Report(models.Model):
    """Отчет
    """
    REPORT_STATUS = (
        (ReportStatus.ready, 'Готов'),
        (ReportStatus.pending, 'Ожидайте...'),
    )
    status = models.CharField(
        max_length=1,
        choices=REPORT_STATUS,
        default=ReportStatus.pending,
        verbose_name='Статус отчета',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Запрошен в: ',
    )
    file = models.FileField(
        verbose_name='Отчет',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'
