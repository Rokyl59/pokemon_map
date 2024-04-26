from django.db import models  # noqa F401
from django.utils import timezone


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    title_en = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Название на английском"
    )
    title_jp = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Название на японском"
    )
    image = models.ImageField(
        upload_to='pokemons_image',
        blank=True,
        null=True,
        verbose_name="Изображение"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание"
    )
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions',
        verbose_name="Из кого эволюционировал"
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name="Покемон",
    )
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(default=timezone.now, verbose_name="Время появления")
    disappeared_at = models.DateTimeField(default=timezone.now, verbose_name="Время исчезновения")
    level = models.IntegerField(default=1, verbose_name="Уровень")
    health = models.IntegerField(default=100, verbose_name="Здоровье")
    attack = models.IntegerField(default=50, verbose_name="Атака")
    defense = models.IntegerField(default=50, verbose_name="Защита")
    stamina = models.IntegerField(default=50, verbose_name="Выносливость")

    def __str__(self):
        return f"{self.pokemon.title} (Level {self.level}) at {self.latitude}, {self.longitude}"
