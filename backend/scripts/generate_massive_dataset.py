"""
Generate a massive movie dataset (50,000+ movies) for RAG testing.
Optimized for batch processing and parallel embedding generation.
"""

import sys
import os
import random
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import execute_query, get_cursor
from config import config

# Expanded data for more variety
DIRECTORS = [
    # American Directors
    "Steven Spielberg", "Martin Scorsese", "Christopher Nolan", "Quentin Tarantino",
    "David Fincher", "Ridley Scott", "James Cameron", "Wes Anderson",
    "Coen Brothers", "Paul Thomas Anderson", "Darren Aronofsky", "Michael Mann",
    "Kathryn Bigelow", "Greta Gerwig", "Sofia Coppola", "Ava DuVernay",
    "Barry Jenkins", "Jordan Peele", "Ryan Coogler", "Spike Lee",
    "Sam Raimi", "Tim Burton", "Terry Gilliam", "Clint Eastwood",
    "Oliver Stone", "Ron Howard", "Robert Zemeckis", "M. Night Shyamalan",
    "John Hughes", "Rob Reiner", "Cameron Crowe", "Kevin Smith",
    "Richard Linklater", "Todd Phillips", "Adam McKay", "Judd Apatow",
    # International Directors
    "Denis Villeneuve", "Guillermo del Toro", "Alfonso Cuarón", "Alejandro González Iñárritu",
    "Bong Joon-ho", "Park Chan-wook", "Wong Kar-wai", "Akira Kurosawa",
    "Hayao Miyazaki", "Satoshi Kon", "Makoto Shinkai", "Hirokazu Kore-eda",
    "Pedro Almodóvar", "Fernando Meirelles", "Luc Besson", "Jean-Pierre Jeunet",
    "Lars von Trier", "Nicolas Winding Refn", "Thomas Vinterberg", "Florian Henckel von Donnersmarck",
    "Giuseppe Tornatore", "Paolo Sorrentino", "Yorgos Lanthimos", "Andrei Tarkovsky",
    "Ingmar Bergman", "Federico Fellini", "Sergio Leone", "Werner Herzog",
    "Michael Haneke", "Roman Polanski", "Andrzej Wajda", "Krzysztof Kieślowski",
    "Ken Loach", "Danny Boyle", "Guy Ritchie", "Matthew Vaughn",
    "Edgar Wright", "Taika Waititi", "Peter Jackson", "George Miller",
    # Classic Directors
    "Stanley Kubrick", "Francis Ford Coppola", "Alfred Hitchcock", "Billy Wilder",
    "John Ford", "Howard Hawks", "Orson Welles", "Frank Capra",
    "Cecil B. DeMille", "George Cukor", "William Wyler", "Michael Curtiz",
    # Horror Specialists
    "Robert Eggers", "Ari Aster", "Mike Flanagan", "James Wan",
    "John Carpenter", "Wes Craven", "George Romero", "Tobe Hooper",
    "David Cronenberg", "Dario Argento", "Eli Roth", "Ti West",
    # Modern Directors
    "Denis Villeneuve", "Damien Chazelle", "Chloe Zhao", "Emerald Fennell",
    "Lulu Wang", "Dee Rees", "Boots Riley", "Bo Burnham",
    "Olivia Wilde", "Marielle Heller", "Lorene Scafaria", "Karyn Kusama",
]

GENRES = [
    "Sci-Fi", "Drama", "Action", "Thriller", "Horror", "Comedy", "Romance",
    "Animation", "War", "Mystery", "Crime", "Fantasy", "Adventure", "Western",
    "Documentary", "Musical", "Biography", "Sport", "Family", "Noir",
    "Psychological Thriller", "Dark Comedy", "Romantic Comedy", "Action Comedy",
    "Sci-Fi Horror", "Historical Drama", "Political Thriller", "Legal Drama",
    "Medical Drama", "Disaster", "Superhero", "Martial Arts", "Heist"
]

# More title patterns for variety
TITLE_PATTERNS = [
    ["The", ["Last", "Final", "First", "Lost", "Dark", "Silent", "Forgotten", "Eternal", "Hidden", "Secret", "Endless", "Dying", "Living", "Burning", "Frozen"],
     ["Night", "Day", "Hour", "Dawn", "Storm", "Dream", "Shadow", "Light", "Truth", "Promise", "Wish", "Hope", "Fear", "Empire", "Kingdom"]],
    [["Dark", "Bright", "Cold", "Deep", "High", "Long", "Short", "Hard", "Soft", "Sharp", "Thin", "Wide", "Narrow", "Bitter", "Sweet"],
     ["Water", "Fire", "Earth", "Sky", "Road", "Path", "Line", "Edge", "Point", "Corner", "End", "Start", "Heart", "Mind", "Soul"]],
    ["The", ["Man", "Woman", "Girl", "Boy", "King", "Queen", "Stranger", "Ghost", "Hunter", "Witness", "Killer", "Lover", "Fool", "Hero", "Villain"],
     ["Who", "in", "from", "of", "with", "without", "against", "beyond", "beneath"],
     ["Knew", "the", "Too Much", "Everything", "Nothing", "Shadows", "Time", "Fear", "Love", "Death", "Secrets"]],
    [["Blood", "Iron", "Steel", "Gold", "Silver", "Stone", "Glass", "Paper", "Silk", "Ice", "Bone", "Ash", "Dust", "Salt", "Smoke"],
     ["and", "&"],
     ["Honor", "Fire", "Thunder", "Lightning", "Tears", "Dreams", "Bones", "Roses", "Thorns", "Mirrors", "Chains", "Wings"]],
    [["Running", "Falling", "Rising", "Burning", "Breaking", "Chasing", "Hunting", "Finding", "Losing", "Seeking", "Hiding", "Fighting", "Dancing", "Dying", "Living"],
     ["Down", "Up", "Away", "Home", "Free", "Wild", "Alone", "Together", "Forward", "Backward", "Nowhere", "Everywhere"]],
    ["The", ["Great", "Big", "Little", "Old", "New", "Last", "Next", "Other", "Same", "True", "False", "Real", "Perfect", "Broken"],
     ["Escape", "Heist", "Robbery", "Game", "Hunt", "Race", "Chase", "Journey", "Adventure", "Discovery", "Mistake", "Betrayal"]],
    [["One", "Two", "Three", "Seven", "Twelve", "Thirteen", "A Hundred", "A Thousand", "Zero", "Infinite"],
     ["Days", "Nights", "Hours", "Years", "Lives", "Chances", "Reasons", "Seconds", "Moments", "Stories", "Lies", "Truths"]],
    [["Project", "Operation", "Mission", "Protocol", "Program", "Initiative", "Code Name:", "File:", "Case:"],
     ["Phoenix", "Shadow", "Titan", "Genesis", "Exodus", "Trinity", "Omega", "Alpha", "Delta", "Echo", "Raptor", "Viper", "Ghost", "Storm"]],
    [["Red", "Blue", "Black", "White", "Green", "Yellow", "Purple", "Orange", "Grey", "Golden", "Silver", "Crimson"],
     ["Dawn", "Dusk", "Sky", "Sea", "Mountain", "River", "Desert", "Forest", "City", "Memory", "Future", "Past"]],
    ["The", ["Art", "Science", "Mystery", "History", "Legend", "Myth", "Story", "Tale", "Secret", "Power"],
     ["of", "behind", "within", "beyond"],
     ["War", "Love", "Death", "Life", "Time", "Space", "Dreams", "Fear", "Revenge", "Redemption"]],
]

# Expanded plot elements
PROTAGONISTS = [
    "Maya", "Jack", "Elena", "Marcus", "Dr. Chen", "Agent Torres", "Detective Kim", "Sarah",
    "Alex", "Jordan", "Emma", "Michael", "Luna", "Kai", "Professor Hayes", "Nathan",
    "Sofia", "Oliver", "Isabella", "Ethan", "Aria", "Liam", "Zoe", "David",
    "Rachel", "James", "Olivia", "William", "Emily", "Benjamin", "Ava", "Daniel",
    "Mia", "Henry", "Charlotte", "Sebastian", "Harper", "Leo", "Evelyn", "Oscar"
]

OCCUPATIONS = [
    "scientist", "soldier", "detective", "teacher", "artist", "pilot", "doctor", "hacker",
    "journalist", "chef", "mechanic", "professor", "nurse", "architect", "musician", "lawyer",
    "therapist", "engineer", "writer", "photographer", "surgeon", "spy", "assassin", "thief",
    "bounty hunter", "ex-cop", "firefighter", "paramedic", "FBI agent", "CIA operative",
    "marine biologist", "archaeologist", "astronaut", "botanist", "cryptographer", "linguist"
]

LOCATIONS = [
    "a space station orbiting Mars", "the neon-lit streets of Neo Tokyo", "a remote Alaskan village",
    "the underground bunkers of post-war Europe", "a luxury cruise ship in the Pacific",
    "the frozen wastelands of Antarctica", "a crumbling mansion in the bayou",
    "the bustling markets of Marrakech", "a secret facility beneath the Pentagon",
    "an abandoned theme park in Chernobyl", "the floating cities of 2150",
    "a monastery in the Himalayas", "the criminal underworld of 1920s Chicago",
    "a research station in the Marianas Trench", "the last human colony on Europa",
    "Victorian London's fog-filled streets", "a maximum security prison in Siberia",
    "the glamorous casinos of Monaco", "an isolated lighthouse on the Scottish coast",
    "the war-torn streets of a fictional Middle Eastern city"
]

THEMES = [
    "identity and self-discovery", "the nature of reality", "love versus duty",
    "redemption and forgiveness", "power and its corrupting influence", "family bonds",
    "sacrifice for the greater good", "the cost of ambition", "truth versus illusion",
    "survival against impossible odds", "revenge and its consequences", "trust and betrayal",
    "freedom versus security", "the burden of the past", "hope in darkness",
    "the meaning of humanity", "connection in isolation", "legacy and inheritance",
    "justice versus law", "the price of progress"
]

ANTAGONISTS = [
    "a shadowy corporation", "a rogue AI", "their own government", "an ancient cult",
    "a brilliant serial killer", "a corrupt politician", "a rival spy agency",
    "their former mentor", "a pharmaceutical conglomerate", "a terrorist organization",
    "the military-industrial complex", "a ruthless cartel", "an interdimensional entity",
    "a tech billionaire with god complex", "a secret society", "their own dark side",
    "a vengeful ghost", "an alien species", "a pandemic bioweapon creator", "time itself"
]

TWISTS = [
    "they discover they've been the villain all along",
    "the person they trusted most is the mastermind",
    "everything was a simulation",
    "they're actually dead and in purgatory",
    "the cure is worse than the disease",
    "the hero and villain are the same person",
    "it was all to protect someone they love",
    "the conspiracy goes to the highest levels",
    "they have to become what they hate to win",
    "victory comes at an unbearable personal cost",
    "the real threat was humanity itself",
    "love was the answer all along",
    "the past cannot be changed",
    "sacrifice was the only option",
    "they were being tested the whole time"
]

# Extensive list of actors for variety
ACTORS = [
    # Hollywood A-List
    "Tom Hanks", "Leonardo DiCaprio", "Brad Pitt", "Denzel Washington", "Morgan Freeman",
    "Robert De Niro", "Al Pacino", "Meryl Streep", "Cate Blanchett", "Nicole Kidman",
    "Sandra Bullock", "Julia Roberts", "Angelina Jolie", "Johnny Depp", "Will Smith",
    "George Clooney", "Matt Damon", "Christian Bale", "Joaquin Phoenix", "Tom Cruise",
    "Scarlett Johansson", "Emma Stone", "Jennifer Lawrence", "Natalie Portman", "Anne Hathaway",
    "Kate Winslet", "Amy Adams", "Viola Davis", "Margot Robbie", "Charlize Theron",
    "Samuel L. Jackson", "Michael B. Jordan", "Dwayne Johnson", "Ryan Gosling", "Jake Gyllenhaal",
    "Oscar Isaac", "Adam Driver", "Timothée Chalamet", "Florence Pugh", "Zendaya",
    # Action Stars
    "Keanu Reeves", "Jason Statham", "Vin Diesel", "Michelle Rodriguez", "Gal Gadot",
    "Chris Hemsworth", "Chris Evans", "Chris Pratt", "Robert Downey Jr.", "Mark Ruffalo",
    "Tom Holland", "Brie Larson", "Simu Liu", "John Boyega", "Idris Elba",
    # Classic Hollywood
    "Marlon Brando", "James Dean", "Humphrey Bogart", "Audrey Hepburn", "Marilyn Monroe",
    "Gregory Peck", "Katharine Hepburn", "Ingrid Bergman", "Cary Grant", "Gene Kelly",
    "Elizabeth Taylor", "Paul Newman", "Robert Redford", "Dustin Hoffman", "Jack Nicholson",
    "Harrison Ford", "Sigourney Weaver", "Jodie Foster", "Anthony Hopkins", "Gary Oldman",
    # British Actors
    "Daniel Craig", "Benedict Cumberbatch", "Tom Hiddleston", "Eddie Redmayne", "Jude Law",
    "Emily Blunt", "Keira Knightley", "Emma Watson", "Tilda Swinton", "Helen Mirren",
    "Judi Dench", "Ian McKellen", "Patrick Stewart", "Ralph Fiennes", "Colin Firth",
    # International Stars
    "Penélope Cruz", "Javier Bardem", "Antonio Banderas", "Gael García Bernal", "Diego Luna",
    "Lupita Nyong'o", "Chiwetel Ejiofor", "Dev Patel", "Priyanka Chopra", "Deepika Padukone",
    "Tony Leung", "Gong Li", "Zhang Ziyi", "Jet Li", "Jackie Chan",
    "Song Kang-ho", "Bae Doona", "Park So-dam", "Choi Min-sik", "Lee Byung-hun",
    "Ken Watanabe", "Rinko Kikuchi", "Tadanobu Asano", "Toshiro Mifune", "Takeshi Kitano",
    "Mads Mikkelsen", "Noomi Rapace", "Alicia Vikander", "Alexander Skarsgård", "Rebecca Ferguson",
    # Rising Stars
    "Anya Taylor-Joy", "Sydney Sweeney", "Austin Butler", "Barry Keoghan", "Paul Mescal",
    "Jenna Ortega", "Xochitl Gomez", "Dominique Thorne", "Kathryn Newton", "Maitreyi Ramakrishnan",
    # Comedy Stars
    "Steve Carell", "Will Ferrell", "Adam Sandler", "Seth Rogen", "Jonah Hill",
    "Melissa McCarthy", "Tiffany Haddish", "Awkwafina", "Ken Jeong", "Kevin Hart",
    # Character Actors
    "Willem Dafoe", "John Turturro", "Steve Buscemi", "J.K. Simmons", "Walton Goggins",
    "Michael Shannon", "Ben Mendelsohn", "John Hawkes", "Sam Rockwell", "Richard Jenkins",
    "Frances McDormand", "Allison Janney", "Octavia Spencer", "Laurie Metcalf", "Margo Martindale",
]

def generate_plot(genre: str) -> str:
    """Generate a unique plot based on genre."""
    protagonist = random.choice(PROTAGONISTS)
    occupation = random.choice(OCCUPATIONS)
    location = random.choice(LOCATIONS)
    theme = random.choice(THEMES)
    antagonist = random.choice(ANTAGONISTS)

    templates = {
        "Sci-Fi": [
            f"In {random.randint(2050, 2300)}, when technology has reshaped humanity, {protagonist}, a {occupation}, discovers a truth that threatens everything. Set in {location}, this mind-bending journey explores {theme}.",
            f"After a catastrophic event leaves Earth uninhabitable, {protagonist} leads the last survivors in {location}. When they uncover {antagonist}'s secret, they must choose between safety and truth.",
            f"{protagonist} wakes up in {location} with no memory of how they got there. As they piece together the mystery, they realize {antagonist} has been manipulating reality itself. A gripping tale of {theme}.",
        ],
        "Drama": [
            f"{protagonist}, a {occupation} struggling with personal demons, finds unexpected connection in {location}. Through relationships forged in hardship, they learn about {theme}.",
            f"Spanning three generations, this intimate portrait follows {protagonist}'s journey from obscurity to significance. Set against the backdrop of {location}, it's a meditation on {theme}.",
            f"After tragedy strikes, {protagonist} retreats to {location} where they encounter people who challenge everything they believed about {theme}.",
        ],
        "Action": [
            f"When {antagonist} threatens global security, {protagonist}, a former {occupation}, comes out of retirement for one final mission in {location}. Explosive action ensues.",
            f"{protagonist} has 48 hours to stop {antagonist} before it's too late. Armed with nothing but their skills as a {occupation}, they'll fight their way through {location}.",
            f"Betrayed and left for dead, {protagonist} survives to seek revenge against {antagonist}. A brutal journey through {location} where {theme} is tested at every turn.",
        ],
        "Thriller": [
            f"{protagonist} thought they knew the truth until a discovery in {location} reveals {antagonist}'s terrifying plan. A psychological thriller exploring {theme}.",
            f"Someone is watching. {protagonist}, a {occupation}, realizes they've stumbled onto something deadly in {location}. Trust no one in this taut thriller.",
            f"A seemingly perfect life unravels when {protagonist} receives a message that leads them to {location} and a conspiracy involving {antagonist}.",
        ],
        "Horror": [
            f"Something ancient awakens in {location}. {protagonist}, a {occupation}, must survive the night as {antagonist} hunts them through the darkness.",
            f"The new house seemed perfect until {protagonist} discovered its horrifying past. Set in {location}, this terror explores {theme}.",
            f"After moving to {location}, {protagonist} begins experiencing visions that blur the line between nightmare and reality. What they discover about {antagonist} is worse than any dream.",
        ],
        "Comedy": [
            f"When {protagonist}, a hopelessly clumsy {occupation}, accidentally finds themselves in {location}, hilarious chaos ensues. A heartfelt comedy about {theme}.",
            f"{protagonist} must pretend to be something they're not to survive in {location}. When their lies spiral out of control, they discover the truth about {theme}.",
            f"A group of misfit friends attempt an impossible scheme in {location}. What could go wrong? Everything. A laugh-out-loud exploration of {theme}.",
        ],
        "Romance": [
            f"In the enchanting setting of {location}, {protagonist} meets someone who challenges everything they thought they knew about love. A sweeping tale of {theme}.",
            f"Years after they parted ways, {protagonist} and their lost love reunite in {location}. Old feelings resurface alongside old wounds.",
            f"A {occupation} and an unlikely partner discover connection in {location}. But {antagonist} threatens to tear them apart in this emotional journey through {theme}.",
        ],
        "Crime": [
            f"The perfect heist goes wrong when {antagonist} double-crosses {protagonist} in {location}. A gritty crime saga about {theme}.",
            f"Detective {protagonist} pursues a criminal mastermind through {location}, discovering {theme} along the way. The line between hunter and hunted blurs.",
            f"In the criminal underworld of {location}, {protagonist} must navigate betrayal, violence, and {antagonist} to survive. A noir-tinged exploration of {theme}.",
        ],
    }

    # Default templates for genres not specifically listed
    default_templates = [
        f"{protagonist}, a {occupation}, embarks on an extraordinary journey in {location}. Facing {antagonist}, they discover the true meaning of {theme}.",
        f"Set in {location}, this gripping story follows {protagonist} as they confront {antagonist} and learn about {theme}.",
        f"When fate brings {protagonist} to {location}, they must use their skills as a {occupation} to overcome {antagonist}. An unforgettable tale of {theme}.",
    ]

    genre_templates = templates.get(genre, default_templates)
    return random.choice(genre_templates)

def generate_title() -> str:
    """Generate a movie title."""
    pattern = random.choice(TITLE_PATTERNS)
    title_parts = []

    for part in pattern:
        if isinstance(part, list):
            title_parts.append(random.choice(part))
        else:
            title_parts.append(part)

    return " ".join(title_parts)

def generate_actors() -> list:
    """Generate a random cast of 2-6 actors."""
    num_actors = random.randint(2, 6)
    return random.sample(ACTORS, min(num_actors, len(ACTORS)))

def generate_movie() -> dict:
    """Generate a single movie entry."""
    genre = random.choice(GENRES)
    year = random.randint(1942, 2024)
    director = random.choice(DIRECTORS)

    # Generate unique plot
    plot = generate_plot(genre)

    # Generate cast
    actors = generate_actors()

    # Rating weighted toward 6-8 range (more realistic distribution)
    rating = round(random.triangular(5.0, 10.0, 7.2), 1)

    # Runtime varies by genre
    if genre in ["Documentary", "Animation"]:
        runtime = random.randint(75, 140)
    elif genre in ["Drama", "War", "Biography"]:
        runtime = random.randint(100, 195)
    else:
        runtime = random.randint(85, 160)

    return {
        "title": generate_title(),
        "year": year,
        "director": director,
        "genre": genre,
        "plot": plot,
        "rating": rating,
        "runtime_minutes": runtime,
        "actors": actors
    }

def batch_insert_movies(movies: list, batch_size: int = 500):
    """Insert movies in large batches for efficiency."""
    sql = """
        INSERT INTO rag_movies (title, year, director, genre, plot, rating, runtime_minutes, actors)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """

    total = len(movies)
    inserted = 0

    with get_cursor() as cursor:
        for i in range(0, total, batch_size):
            batch = movies[i:i + batch_size]
            for movie in batch:
                cursor.execute(sql, (
                    movie["title"],
                    movie["year"],
                    movie["director"],
                    movie["genre"],
                    movie["plot"],
                    movie["rating"],
                    movie["runtime_minutes"],
                    movie.get("actors", [])
                ))
            inserted += len(batch)
            print(f"  Inserted {inserted}/{total} movies...")

    return inserted

def main():
    parser = argparse.ArgumentParser(description='Generate massive movie dataset')
    parser.add_argument('--target', type=int, default=50000,
                        help='Target number of total movies (default: 50000)')
    parser.add_argument('--batch-size', type=int, default=500,
                        help='Batch size for database inserts (default: 500)')
    args = parser.parse_args()

    print("=" * 60)
    print("MASSIVE MOVIE DATASET GENERATOR")
    print("=" * 60)

    # Check current count
    result = execute_query("SELECT COUNT(*) as count FROM rag_movies")
    current_count = result[0]['count'] if result else 0
    print(f"\nCurrent movie count: {current_count:,}")
    print(f"Target movie count: {args.target:,}")

    to_generate = max(0, args.target - current_count)

    if to_generate == 0:
        print(f"Already have {current_count:,} movies. No generation needed.")
        return

    print(f"Generating {to_generate:,} new movies...")
    print()

    # Generate movies
    start_time = time.time()
    movies = []

    for i in range(to_generate):
        movie = generate_movie()
        movies.append(movie)

        if (i + 1) % 5000 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            remaining = (to_generate - i - 1) / rate
            print(f"  Generated {i + 1:,}/{to_generate:,} movies ({rate:.0f}/sec, ~{remaining:.0f}s remaining)")

    generation_time = time.time() - start_time
    print(f"\nGeneration complete in {generation_time:.1f}s ({len(movies)/generation_time:.0f} movies/sec)")

    # Insert into database
    print(f"\nInserting {len(movies):,} movies into database...")
    insert_start = time.time()
    inserted = batch_insert_movies(movies, args.batch_size)
    insert_time = time.time() - insert_start
    print(f"Insert complete in {insert_time:.1f}s ({inserted/insert_time:.0f} movies/sec)")

    # Verify final count
    result = execute_query("SELECT COUNT(*) as count FROM rag_movies")
    final_count = result[0]['count'] if result else 0

    print()
    print("=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    print(f"Previous count: {current_count:,}")
    print(f"Movies generated: {len(movies):,}")
    print(f"Final count: {final_count:,}")
    print()
    print("IMPORTANT: Run generate_embeddings.py to create vector embeddings")
    print("for semantic search to work on the new movies.")
    print("=" * 60)

if __name__ == "__main__":
    main()
