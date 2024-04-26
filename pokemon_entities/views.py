import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import PokemonEntity
from django.utils import timezone


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    current_time = timezone.localtime()
    active_pokemons_entities = PokemonEntity.objects.filter(
        appeared_at__lte=current_time,
        disappeared_at__gte=current_time
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in active_pokemons_entities:
        image_url = pokemon_entity.pokemon.image.url if pokemon_entity.pokemon.image else DEFAULT_IMAGE_URL
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(image_url)
        )

    pokemons_on_page = []
    for pokemon_entity in active_pokemons_entities:
        pokemons_on_page.append({
            'pokemon_id': pokemon_entity.pokemon.id,
            'img_url': request.build_absolute_uri(pokemon_entity.pokemon.image.url) if pokemon_entity.pokemon.image else DEFAULT_IMAGE_URL,
            'title_ru': pokemon_entity.pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon_entities = PokemonEntity.objects.filter(
            pokemon_id=pokemon_id,
            appeared_at__lte=timezone.localtime(),
            disappeared_at__gte=timezone.localtime()
        )
        pokemon = pokemon_entities.first().pokemon
    except (PokemonEntity.DoesNotExist, AttributeError):
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(pokemon.image.url) if pokemon.image else DEFAULT_IMAGE_URL
        )
    
    pokemon_data = {
        'img_url': request.build_absolute_uri(pokemon.image.url) if pokemon.image else DEFAULT_IMAGE_URL,
        'title_ru': pokemon.title,
        'description': pokemon.description,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
    }

    pokemon_data['previous_evolution'] = {
        'title_ru': pokemon.previous_evolution.title if pokemon.previous_evolution else "",
        'pokemon_id': pokemon.previous_evolution.id if pokemon.previous_evolution else None,
        'img_url': request.build_absolute_uri(pokemon.previous_evolution.image.url) if pokemon.previous_evolution and pokemon.previous_evolution.image else DEFAULT_IMAGE_URL,
    } if pokemon.previous_evolution else {}

    next_evolution = pokemon.next_evolutions.first()
    pokemon_data['next_evolution'] = {
        'title_ru': next_evolution.title if next_evolution else "",
        'pokemon_id': next_evolution.id if next_evolution else None,
        'img_url': request.build_absolute_uri(next_evolution.image.url) if next_evolution and next_evolution.image else DEFAULT_IMAGE_URL,
    } if next_evolution else {}

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_data
    })
