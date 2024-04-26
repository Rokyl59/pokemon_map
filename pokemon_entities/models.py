from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='pokemons_image',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
    )
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f'{self.pokemon.title} at {self.latitude}, {self.longitude}'
