from random import choice
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation


COMMENDATIONS = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!'
    ]


def find_scoolkid(name: str) -> Schoolkid | None:
    """Возращает экземпляр класса 'datacenter.models.Schoolkid или None'
     Args:
        name (str): имя школьника
    Returns:
        class 'datacenter.models.Schoolkid'или None
    Examples:
          >>> find_scoolkid('Фролов Иван')
        /Фролов Иван Григорьевич 6А
        /Either the entry or blog doesn't exist.
        /More than one object was found
    """
    if not name:
        print('Введите фамилию и имя ученика')
    else:
        try:
            return Schoolkid.objects.get(full_name__contains=name)
        except ObjectDoesNotExist:
            print("Either the entry or blog doesn't exist.")
            return
        except MultipleObjectsReturned:
            print("More than one object was found")
            return


def fix_marks(schoolkid: str) -> None:
    """Функция исправляет оценки ученика на 4 или 5
    Args:
        name (str): имя школьника
    Returns:
        None
    Examples:
          >>> fix_marks('Фролов Иван')
    """
    schoolkid_doc = find_scoolkid(schoolkid)
    schoolkid_bad_marks = Mark.objects.filter(schoolkid=schoolkid_doc, points__in =[1, 2, 3])
    schoolkid_bad_marks.update(points=choice(4,5))


def remove_chastisements(schoolkid: str) -> None:
    """Функция удаляет замечания на ученика
     Args:
        name (str): имя школьника
    Returns:
        None
    Examples:
          >>> remove_chastisements('Фролов Иван')
    """
    schoolkid_doc = find_scoolkid(schoolkid)
    schoolkid_Chastisements = Chastisement.objects.filter(schoolkid=schoolkid_doc)
    schoolkid_Chastisements.delete()


def create_commendation(schoolkid: str, subject: str) -> None:
    """Функция создаст запись, в которой хвалят ученика
     Args:
        name (str): имя школьника
        subject (str): название предмета
    Returns:
        None
    Examples:
          >>> create_commendation('Фролов Иван', 'Математика')
    """
    schoolkid_doc = find_scoolkid(schoolkid)
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid_doc.year_of_study,
        group_letter=schoolkid_doc.group_letter,
        ubject__title=subject
        ).order_by('?').first()

    commendation = choice(COMMENDATIONS)
    Commendation.objects.create(text=commendation,
                                created=lesson.date,
                                schoolkid=schoolkid_doc,
                                subject=lesson.subject,
                                teacher=lesson.teacher)
