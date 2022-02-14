from random import choice

from datacenter.models import *
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.management.base import BaseCommand


def find_schoolkid(full_name: str):
    """Поиск ученика в базе данных по ФИО.

    Args:
        full_name (str): ФИО ученика

    Returns:
        Schoolkid: Найденная запись ученика
    """
    try:
        return Schoolkid.objects.get(full_name__contains=full_name)
    except ObjectDoesNotExist:
        print('Ученик не найден.')
    except MultipleObjectsReturned:
        print('Найдено слишком много учеников.')


def fix_marks(schoolkid):
    """Исправляет плохие оценки ученика на 5.

    Args:
        schoolkid (Schoolkid): Ученик
    """
    for mark in Mark.objects.filter(schoolkid=schoolkid, points__lte=3):
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
    """Удаляет замечание по ученику.

    Args:
        schoolkid (Schoolkid): Ученик
    """
    for chastisement in Chastisement.objects.filter(schoolkid=schoolkid):
        chastisement.delete()


def create_commendation(schoolkid, subject_title):
    """Создание благодарности по ученику.

    Args:
        schoolkid (Schoolkid): Ученик
        subject_title (str): Название предмета
    """
    with open('./commendations.txt', 'r') as commendations_file:
        commendation_phrase = choice(commendations_file.readlines()).strip()

        lesson = Lesson.objects.filter(
            subject__title=subject_title,
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter
        ).order_by('-date').first()

        Commendation.objects.create(text=commendation_phrase,
                                    created=lesson.date,
                                    schoolkid=schoolkid,
                                    subject=lesson.subject,
                                    teacher=lesson.teacher)


class Command(BaseCommand):
    """Start the bot."""

    help = 'Hack DB'

    def handle(self, *args, **options):
        schoolkid = find_schoolkid('Фролов Иван')
        if schoolkid:
            create_commendation(schoolkid, 'Математика')
        # print(find_schoolkid('Фролов Иван'))
        #
