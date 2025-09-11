from django.db import models

UNIT_TYPE_COUNTRY = 1
UNIT_TYPE_MIDDLE = 2
UNIT_TYPE_SETTLEMENT = 3
UNIT_TYPES = (
    (UNIT_TYPE_COUNTRY, 'Государство'),
    (UNIT_TYPE_MIDDLE, 'Промежуточная часть'),
    (UNIT_TYPE_SETTLEMENT, 'Населённый пункт'),
)

CALENDAR_GREGORIAN = 1
CALENDAR_JULIAN = 2
CALENDARS = (
    (CALENDAR_GREGORIAN, 'Григорианский календарь'),
    (CALENDAR_JULIAN, 'Юлианский календарь'),
)


class Date(models.Model):
    start_year = models.IntegerField(verbose_name='Год начала', null=True)
    start_month = models.PositiveIntegerField(verbose_name='Месяц начала', null=True)
    start_day = models.PositiveIntegerField(verbose_name='День начала', null=True)
    calendar_start = models.IntegerField(
        verbose_name='Календарь даты начала',
        choices=CALENDARS,
        default=CALENDAR_GREGORIAN,
    )
    end_year = models.IntegerField(verbose_name='Год окончания', null=True)
    end_month = models.PositiveIntegerField(verbose_name='Месяц окончания', null=True)
    end_day = models.PositiveIntegerField(verbose_name='День окончания', null=True)
    calendar_end = models.IntegerField(
        verbose_name='Календарь даты окончания',
        choices=CALENDARS,
        default=CALENDAR_GREGORIAN,
    )

    @staticmethod
    def glue_date(year, month, day):
        year_str = str(year).rjust(4, '0') if year else '????'
        month_str = str(month).rjust(2, '0') if month else '??'
        day_str = str(day).rjust(2, '0') if day else '??'
        if year and month and day:
            return f'{year_str}-{month_str}-{day_str}'
        elif year and month:
            return f'{year_str}-{month_str}'
        elif year:
            return year_str
        elif year or month or day:
            return f'{year_str}-{month_str}-{day_str}'
        
        return None

    @property
    def start_date(self):
        return self.glue_date(self.start_year, self.start_month, self.start_day)

    @property
    def end_date(self):
        return self.glue_date(self.end_year, self.end_month, self.end_day)

    class Meta:
        abstract = True


class Unit(Date, models.Model):
    type = models.IntegerField(verbose_name='Тип', choices=UNIT_TYPES)

    class Meta:
        verbose_name = 'Административно-территориальная единица'
        verbose_name_plural = 'Административно-территориальные единицы'


class UnitName(Date, models.Model):
    unit = models.ForeignKey(Unit, verbose_name='АТЕ', on_delete=models.CASCADE, related_name='names')
    name = models.CharField(verbose_name='Название АТЕ', max_length=200)

    class Meta:
        verbose_name = 'Наименование'
        verbose_name_plural = 'Наименования'


class Including(Date, models.Model):
    child = models.ForeignKey(Unit, verbose_name='АТЕ', on_delete=models.CASCADE, related_name='parent_includings')
    parent = models.ForeignKey(
        Unit,
        verbose_name='АТЕ уровнем выше',
        on_delete=models.CASCADE,
        related_name='children_includings',
    )

    class Meta:
        verbose_name = 'Включение'
        verbose_name_plural = 'Включения'
