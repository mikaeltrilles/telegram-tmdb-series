import argparse
import requests
import subprocess
import os
from datetime import datetime

# Correspondance entre les ID de genre et les emojis
genre_mapping = {
    28: '💪 #Action',
    16: '🐵 #Animation',
    12: '🌋 #Aventure',
    35: '😂 #Comédie',
    80: '🔪 #Crime',
    18: '🎭 #Drame',
    99: '🌍 #Documentaire',
    10762: '👶🏻 #Enfant',
    10751: '👨‍👩‍👦‍👦 #Familial',
    14: '🦄 #Fantastique',
    10752: '💣 #Guerre',
    36: '👑 #Histoire',
    27: '😱 #Horreur',
    10402: '🎸 #Musique',
    9648: '🧙🏻‍♂️ #Mystère',
    10749: '💕 #Romance',
    878: '🤖 #SciFi',
    10770: '📺 #Telefilm',
    53: '🚓 #Thriller',
    37: '🌵 #Western',
    10764: '🎱 #Reality',
    10765: '🚀 #Science-Fiction_&_Fantastique',
    10759: '👊🏻 #Action_&_Adventure',
}

# Correspondance entre les noms de pays et les emojis
country_mapping = {
    'South Africa': '🇿🇦 #Afrique_du_Sud',
    'Germany': '🇩🇪 #Allemagne',
    'Algeria': '🇩🇿 #Algérie',
    'Saudi Arabia': '🇸🇦 #Arabie_Saoudite',
    'Argentina': '🇦🇷 #Argentine',
    'Australia': '🇦🇺 #Australie',
    'Austria': '🇦🇹 #Autriche',
    'Belgium': '🇧🇪 #Belgique',
    'Brazil': '🇧🇷 #Brésil',
    'Canada': '🇨🇦 #Canada',
    'Chile': '🇨🇱 #Chili',
    'China': '🇨🇳 #Chine',
    'Colombia': '🇨🇴 #Colombie',
    'South Korea': '🇰🇷 #Corée_du_sud',
    'Denmark': '🇩🇰 #Danemark',
    'Spain': '🇪🇸 #Espagne',
    'United States of America': '🇺🇸 #États_Unis',
    'Finland': '🇫🇮 #Finlande',
    'France': '🇫🇷 #France',
    'Hong Kong': '🇭🇰 #Hong_Kong',
    'Hungary': '🇭🇺 #Hongrie',
    'India': '🇮🇳 #Inde',
    'Italy': '🇮🇹 #Italie',
    'Iran': '🇮🇷 #Iran',
    'Ireland': '🇮🇪 #Irlande',
    'Iceland': '🇮🇸 #Islande',
    'Japan': '🇯🇵 #Japon',
    'Kenya': '🇰🇪 #Kenya',
    'Luxembourg': '🇱🇺 #Luxembourg',
    'Malta': '🇲🇹 #Malte',
    'Morocco': '🇲🇦 #Maroc',
    'Mexico': '🇲🇽 #Mexique',
    'New Zealand': '🇳🇿 #Nouvelle_Zelande',
    'Norway': '🇳🇴 #Norvège',
    'Pakistan': '🇵🇰 #Pakistan',
    'Netherlands': '🇳🇱 #Pays_Bas',
    'Poland': '🇵🇱 #Pologne',
    'Portugal': '🇵🇹 #Portugal',
    'Dominican Republic': '🇩🇴 #République_Dominicaine',
    'United Kingdom': '🇬🇧 #Royaume_Uni',
    'Russia': '🇷🇺 #Russie',
    'Senegal': '🇸🇳 #Sénégal',
    'Sweden': '🇸🇪 #Suède',
    'Switzerland': '🇨🇭 #Suisse',
    'Czech Republic': '🇨🇿 #Tchéquie',
    'Turkey': '🇹🇷 #Turquie',
    'Ukraine': '🇺🇦 #Ukraine',
    'Estonia': '🇪🇪 #Estonie',
}

# Statut de diffusion de la série
genre_statut = {
    'Ended': '<emoji id="5398001711786762757">✅</> Émission terminée',
    'Returning Series': '<emoji id="5440621591387980068">🔜</tg-emoji> Émission renouvelée',
    'Canceled': '❌ Émission annulée',
}

def get_series_details(api_key, series_id):
    base_url = f'https://api.themoviedb.org/3/tv/{series_id}?api_key={api_key}&language=fr-FR'
    response = requests.get(base_url)
    return response.json()

def get_credits_details(api_key, series_id):
    credits_url = f'https://api.themoviedb.org/3/tv/{series_id}/credits?api_key={api_key}&language=fr-FR'
    response = requests.get(credits_url)
    return response.json() if response.status_code == 200 else None

# def minutes_to_hours(minutes):
#     hours = minutes // 60
#     remaining_minutes = minutes % 60
#     return f"{hours:02d}h{remaining_minutes:02d}"

def generate_html(series_details, credits_details):
    try:
        html_content = ""

        genres_with_emojis = [genre_mapping.get(
            genre['id'], '') for genre in series_details['genres']]
        genres_html = ' • '.join(genres_with_emojis)

        # Vérifier si la balise tagline existe et n'est pas vide
        if 'tagline' in series_details and series_details['tagline']:
            tagline_html = f"\n<i>{series_details['tagline']}</>\n"
        else:
            tagline_html = ' '

        # Formater la date de sortie en format européen
        release_date = datetime.strptime(
            series_details['first_air_date'], '%Y-%m-%d').strftime('%d/%m/%Y')

        # Convertir les pays en emojis
        countries_emoji = [country_mapping.get(
            country['name'], '') for country in series_details.get('production_countries', [])]
        countries_html = ' • '.join(countries_emoji)

        # Ajouter les liens TMDB et TVDB
        tmdb_link = f"<a href='https://www.themoviedb.org/tv/{series_details['id']}'>📺 TMDB</>"

        # Vérifier si le titre original existe, sinon utiliser le titre en français
        title = series_details['name']
        original_title = series_details.get('original_name', '')
        release_year = datetime.strptime(
            series_details['first_air_date'], '%Y-%m-%d').strftime('%Y')
        title_html = f"<b> • {title} ({release_year})</>"
        if original_title and original_title != title:
            title_html += f"<br><b>Titre Original:</> {original_title}"

            # Ajoutez cette ligne pour obtenir le statut de diffusion
        raw_status = series_details.get('status', 'Non spécifié')
        status = genre_statut.get(raw_status, 'Non spécifié')  # Mapping du statut

        # Arrondir vote_average à deux chiffres après la virgule s'il y a une note, sinon "NC" (Non Classé)
        vote_average_rounded = round(series_details.get(
            'vote_average', 'NC'), 2) if 'vote_average' in series_details else 'nc'

        # Convertir la durée en format "hh:mm"
        runtime_formatted = f"{series_details['episode_run_time'][0]} min" if series_details.get('episode_run_time') else 'nc'

        # Extraire tous les noms des membres de l'équipe de réalisation ayant le job "Creator"
        creators = [member['name'] for member in series_details['created_by']]

        # Si des créateurs sont disponibles, les utiliser, sinon "NC"
        creators_html = ', '.join(creators) if creators else 'nc'

        # Vérifier si les détails du casting sont disponibles
        if 'cast' in credits_details:
            # Obtenez la liste des membres de la distribution
            cast_members = credits_details['cast']

            # Si la liste des membres de la distribution est disponible, l'utiliser, sinon "NC"
            if cast_members:
                # Limiter aux 10 premiers acteurs
                cast_html = ', '.join(
                    [f"{member['name']}" for member in cast_members[:10]])
            else:
                cast_html = 'nc'
        else:
            cast_html = 'nc'

        html_content = f"""{title_html}
<b>Statut:</> {status}
<emoji id="5082592692391641768">🖼️</>

<b>Origines:</> {countries_html}
<b>Date de Première Diffusion:</> {release_date}
<b>Durée d'un épisode:</> {runtime_formatted} ⭐️ <b>{vote_average_rounded}</>/10
<b>Créateurs:</b> {creators_html}
<b>Acteurs :</b> {cast_html}
<b>Genres:</> {genres_html}
{tagline_html}
<b>Synopsis:</>
<m>{series_details['overview']}</>

{tmdb_link}

<b>Affiche:</><img src="https://image.tmdb.org/t/p/w500/{series_details['poster_path']}">
"""

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    return html_content

def generate_markdown(series_details, credits_details):
    try:
        markdown_content = ""

        genres_with_emojis = [genre_mapping.get(
            genre['id'], '') for genre in series_details['genres']]
        genres_markdown = ' • '.join(genres_with_emojis)

        # Vérifier si la balise tagline existe et n'est pas vide
        if 'tagline' in series_details and series_details['tagline']:
            tagline_markdown = f"\n__{series_details['tagline']}__\n"
        else:
            tagline_markdown = ' '

        # Formater la date de sortie en format européen
        release_date = datetime.strptime(
            series_details['first_air_date'], '%Y-%m-%d').strftime('%d/%m/%Y')

        # Convertir les pays en emojis
        countries_emoji = [country_mapping.get(
            country['name'], '') for country in series_details.get('production_countries', [])]
        countries_markdown = ' • '.join(countries_emoji)

        # Ajouter les liens TMDB et TVDB
        tmdb_link = f"[📺 TMDB](https://www.themoviedb.org/tv/{series_details['id']})"

        # Vérifier si le titre original existe, sinon utiliser le titre en français
        title = series_details['name']
        original_title = series_details.get('original_name', '')
        release_year = datetime.strptime(
            series_details['first_air_date'], '%Y-%m-%d').strftime('%Y')
        title_markdown = f"**{title} ({release_year})**"
        if original_title and original_title != title:
            title_markdown += f"\n**Titre Original:** {original_title}"

        # Ajoutez cette ligne pour obtenir le statut de diffusion
        raw_status = series_details.get('status', 'Non spécifié')
        status = genre_statut.get(raw_status, 'Non spécifié')  # Mapping du statut

        # Arrondir vote_average à deux chiffres après la virgule s'il y a une note, sinon "NC" (Non Classé)
        vote_average_rounded = round(series_details.get(
            'vote_average', 'NC'), 2) if 'vote_average' in series_details else 'nc'

        # Convertir la durée en format "hh:mm"
        runtime_formatted = f"{series_details['episode_run_time'][0]} min" if series_details.get('episode_run_time') else 'nc'

        # Extraire tous les noms des membres de l'équipe de réalisation ayant le job "Creator"
        creators = [member['name']
                     for member in credits_details['crew'] if member['job'] == 'Creator']

        # Si des créateurs sont disponibles, les utiliser, sinon "NC"
        creators_markdown = ', '.join(creators) if creators else 'nc'

        # Vérifier si les détails du casting sont disponibles
        if 'cast' in credits_details:
            # Obtenez la liste des membres de la distribution
            cast_members = credits_details['cast']

            # Si la liste des membres de la distribution est disponible, l'utiliser, sinon "NC"
            if cast_members:
                # Limiter aux 10 premiers acteurs
                cast_markdown = ', '.join(
                    [f"{member['name']}" for member in cast_members[:10]])
            else:
                cast_markdown = 'nc'
        else:
            cast_markdown = 'nc'

        markdown_content = f"""{title_markdown}
**Statut:** {status}
**Origines:** {countries_markdown}
**Date de Première Diffusion:** {release_date}
**Durée d'un épisode:** {runtime_formatted} ⭐️ **{vote_average_rounded}**/10
**Créateurs:** {creators_markdown}
**Acteurs :** {cast_markdown}
**Genres:** {genres_markdown}
{tagline_markdown}
**Synopsis:**
{series_details['overview']}

{tmdb_link}

**Affiche:** ![Affiche](https://image.tmdb.org/t/p/w500/{series_details['poster_path']})
"""

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    return markdown_content

if __name__ == "__main__":
    # Remplacez 'VOTRE_CLE_API' par votre clé API réelle
    api_key = '09a87b0b9f15b8b28f3a6927593ad6b0'

    # Configurer les arguments en ligne de commande
    parser = argparse.ArgumentParser(
        description="Générer une fiche de présentation de série à partir de l'API TMDb.")
    parser.add_argument("series_id", type=str, help="L'ID de la série sur TMDb")

    # Analyser les arguments
    args = parser.parse_args()

    # Obtenir les détails de la série
    series_details = get_series_details(api_key, args.series_id)

    # Obtenir les détails du casting
    credits_details = get_credits_details(api_key, args.series_id)

    if credits_details is not None:
        # Génère la fiche HTML
        html_content = generate_html(series_details, credits_details)

        # Ajouter les liens TMDB et TVDB à la fiche HTML
        tmdb_link = f"<a href='https://www.themoviedb.org/tv/{series_details['id']}'>📺 TMDB</>"

        # Génère la fiche Markdown
        markdown_content = generate_markdown(series_details, credits_details)

        # Ajoute le contenu Markdown à la fiche HTML
        html_content += f"\n\n---\n\n{markdown_content}"

        # Spécifiez le chemin du dossier où vous souhaitez enregistrer le fichier HTML
        # folder_path = "~/tmkprojectlist/series/"

        # Enregistre la fiche HTML dans un fichier
        html_file_path = f"tmkprojectlist/series/{args.series_id}.html"
        with open(html_file_path, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)

        # # Vérifie si le fichier HTML existe
        if os.path.exists(html_file_path):
            # Ouvre le fichier HTML dans Visual Studio Code avec la prévisualisation
            subprocess.run(
                ["code", "--file-uri", f"file://{os.path.abspath(html_file_path)}"])
        else:
            print(f"Le fichier HTML {html_file_path} n'existe pas.")
    else:
        print(f"Les détails du casting ne sont pas disponibles.")
