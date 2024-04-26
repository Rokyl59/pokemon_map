from django.db import models  # noqa F401
from django.utils import timezone


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    title_jp = models.CharField(max_length=200, blank=True)
    image = models.ImageField(
        upload_to='pokemons_image',
        blank=True,
        null=True
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    appeared_at = models.DateTimeField(default=timezone.now)
    disappeared_at = models.DateTimeField(default=timezone.now)
    level = models.IntegerField(default=1)
    health = models.IntegerField(default=100)
    attack = models.IntegerField(default=50)
    defense = models.IntegerField(default=50)
    stamina = models.IntegerField(default=50)

    def __str__(self):
        return f"{self.pokemon.title} (Level {self.level}) at {self.latitude}, {self.longitude}"
