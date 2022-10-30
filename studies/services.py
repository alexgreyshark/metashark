import django_excel as excel
from .models import (
    AcademicGroup,
    StudyDirection,
)


class MakeReportTable:
    """Генерация xlsx отчета
    """
    def make_report(self):
        """Общий отчет
        """
        std_sheet = self.study_direction_sheet()
        group_sheet = self.study_group_sheet()
        per_group_sheet = self.study_students_per_group_sheet()
        result_sheet = std_sheet + group_sheet + per_group_sheet
        return result_sheet

    def study_direction_sheet(self):
        """Печать Учебных направлений
        """
        sheet = excel.pe.Sheet(
            [
                [
                    item.name,
                    item.code,
                    item.curator.username if item.curator else 'Нет куратора',
                    ', '.join(
                        item.subjects.values_list(
                            'name',
                            flat=True,
                        )
                    )
                ] for item in StudyDirection.objects.all()
            ],
            colnames=[
                'Наименование',
                'Код направления',
                'Куратор',
                'Учебные дисциплины'
            ],
            name='Учебные дисциплины',
        )
        return sheet

    def study_group_sheet(self):
        """Печать групп
        """
        sheet = excel.pe.Sheet(
            [
                [
                    item.short_name,
                    item.study_direction.name,
                    item.free_slots(),
                    item.get_female_count(),
                    item.get_male_count(),

                ] for item in AcademicGroup.objects.all()
            ],
            colnames=[
                'Наименование',
                'Учебное направление',
                'Кол-во свободных мест',
                'Кол-во женщин',
                'Кол-во мужчин',
            ],
            name='Группы',
        )
        return sheet

    def study_students_per_group_sheet(self):
        """Печать по группам
        """
        sheet = excel.pe.Sheet(
            [
                [
                    item.short_name,
                    student.last_name,
                    student.first_name,
                    student.birthday,
                ] for item in AcademicGroup.objects.all()
                for student in item.students.order_by('last_name', 'first_name')
            ],
            colnames=[
                'Наименование учебной группы',
                'Имя',
                'Фамилия',
                'Дата рождения',
            ],
            name='По группам',
        )
        return sheet
