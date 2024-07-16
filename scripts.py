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


def find_scoolkid(name: str): #-> Schoolkid | None:
    """Возращает экземпляр класса Schoolkid или None'
     Args:
        name (str): имя школьника
    Returns:
        str или None
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
        except Schoolkid.DoesNotExist:
            raise Schoolkid.DoesNotExist(f'Schoolkid {name} doesn t found')
        except  Schoolkid.MultipleObjectsReturned:
            raise Schoolkid.MultipleObjectsReturned("More than one object was found")


def fix_marks(schoolkid: str) -> None:
    """Функция исправляет оценки ученика 5
    Args:
        name (str): имя школьника
    Returns:
        None
    Examples:
          >>> fix_marks('Фролов Иван')
    """
    schoolkid_card = find_scoolkid(schoolkid)
    schoolkid_bad_marks = Mark.objects.filter(schoolkid=schoolkid_card, points__in =[1, 2, 3])
    schoolkid_bad_marks.update(points=4)


def remove_chastisements(schoolkid: str) -> None:
    """Функция удаляет замечания на ученика
     Args:
        name (str): имя школьника
    Returns:
        None
    Examples:
          >>> remove_chastisements('Фролов Иван')
    """
    schoolkid_card = find_scoolkid(schoolkid)
    schoolkid_chastisements = Chastisement.objects.filter(schoolkid=schoolkid_card)
    schoolkid_chastisements.delete()


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
    schoolkid_card = find_scoolkid(schoolkid)
    lesson = Lesson.objects.filter(year_of_study=schoolkid_card.year_of_study,
                                        group_letter=schoolkid_card.group_letter,
                                        subject__title=subject).order_by('?').first()
    commendation = choice(COMMENDATIONS)
    Commendation.objects.create(text=commendation,
                                created=lesson.date,
                                schoolkid=schoolkid_card,
                                subject=lesson.subject,
                                teacher=lesson.teacher)
