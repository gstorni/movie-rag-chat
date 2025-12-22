"""
Generate 1000+ movies for the RAG database.
Uses a combination of real movie data patterns and procedural generation.
"""

import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import execute_query, get_cursor

# Movie data templates for generation
DIRECTORS = [
    "Steven Spielberg", "Martin Scorsese", "Christopher Nolan", "Quentin Tarantino",
    "Denis Villeneuve", "David Fincher", "Ridley Scott", "James Cameron",
    "Wes Anderson", "Coen Brothers", "Paul Thomas Anderson", "Guillermo del Toro",
    "Alfonso Cuarón", "Alejandro González Iñárritu", "Darren Aronofsky",
    "Stanley Kubrick", "Francis Ford Coppola", "Brian De Palma", "Michael Mann",
    "Kathryn Bigelow", "Greta Gerwig", "Sofia Coppola", "Ava DuVernay",
    "Barry Jenkins", "Jordan Peele", "Ryan Coogler", "Spike Lee",
    "Bong Joon-ho", "Park Chan-wook", "Wong Kar-wai", "Akira Kurosawa",
    "Hayao Miyazaki", "Satoshi Kon", "Mamoru Hosoda", "Makoto Shinkai",
    "Pedro Almodóvar", "Guillermo Arriaga", "Fernando Meirelles", "Walter Salles",
    "Michael Bay", "Roland Emmerich", "J.J. Abrams", "Zack Snyder",
    "Sam Raimi", "Tim Burton", "Terry Gilliam", "Luc Besson",
    "Guy Ritchie", "Matthew Vaughn", "Edgar Wright", "Taika Waititi",
    "Robert Eggers", "Ari Aster", "Mike Flanagan", "James Wan",
    "John Carpenter", "Wes Craven", "George Romero", "Tobe Hooper",
    "David Lynch", "David Cronenberg", "Lars von Trier", "Nicolas Winding Refn",
    "Terrence Malick", "Richard Linklater", "Kelly Reichardt", "Sean Baker",
    "Noah Baumbach", "Charlie Kaufman", "Spike Jonze", "Michel Gondry"
]

GENRES = [
    "Sci-Fi", "Drama", "Action", "Thriller", "Horror", "Comedy", "Romance",
    "Animation", "War", "Mystery", "Crime", "Fantasy", "Adventure", "Western",
    "Documentary", "Musical", "Biography", "Sport", "Family", "Noir"
]

# Plot templates by genre
PLOT_TEMPLATES = {
    "Sci-Fi": [
        "In a future where {technology}, {protagonist} must {mission} before {threat}. Along the way, they discover {revelation} that changes everything about {theme}.",
        "After {disaster}, humanity retreats to {location}. {protagonist}, a {occupation}, uncovers a conspiracy involving {antagonist} and the true nature of {mystery}.",
        "{protagonist} awakens in {setting} with no memory of {past}. As they piece together the truth, they realize {revelation} and must choose between {choice1} and {choice2}.",
        "When {discovery} threatens to {consequence}, {protagonist} leads a team of {team} on a desperate {mission}. The fate of {stakes} hangs in the balance.",
        "In {year}, {technology} has transformed society. {protagonist}, who {backstory}, becomes entangled in {conflict} that will determine humanity's future.",
    ],
    "Drama": [
        "{protagonist}, a {occupation} struggling with {problem}, finds unexpected {resolution} through {relationship}. Set against {backdrop}, this is a story about {theme}.",
        "Three generations of the {family_name} family confront {conflict} during {time_period}. As secrets emerge, {protagonist} must reconcile {choice1} with {choice2}.",
        "After {tragedy}, {protagonist} retreats to {location} where they meet {character} who helps them understand {lesson}. A meditation on {theme1} and {theme2}.",
        "{protagonist}'s world unravels when {revelation}. Forced to confront {past}, they embark on a journey of {transformation} that tests their {quality}.",
        "In {setting}, {protagonist} fights for {goal} against {opposition}. Based on {inspiration}, this powerful drama explores {theme} through one person's {struggle}.",
    ],
    "Action": [
        "When {antagonist} threatens {stakes}, {protagonist}, a former {occupation}, comes out of retirement for one last {mission}. Explosive action and {element} ensue.",
        "{protagonist} must fight through {obstacle} to rescue {person} from {antagonist}'s fortress. Armed with only {weapon} and {skill}, the odds are impossible.",
        "A routine {operation} goes wrong when {complication}. Now {protagonist} has {time_limit} to {goal} before {consequence}. Non-stop action from start to finish.",
        "After {betrayal}, {protagonist} seeks revenge against {antagonist} and their {organization}. What follows is a brutal journey through {locations} with {action_style} action.",
        "{protagonist}, an elite {occupation}, discovers {conspiracy}. Hunted by {enemies}, they must use {skills} to expose the truth and save {stakes}.",
    ],
    "Thriller": [
        "{protagonist} thought they knew {character}, until {discovery}. Now trapped in a web of {element}, they must unravel {mystery} before becoming the next victim.",
        "A seemingly perfect {setting} hides dark secrets. When {protagonist} arrives, they trigger a chain of events that exposes {revelation} and threatens {stakes}.",
        "{protagonist}, a {occupation}, receives {message} that sends them into {situation}. As the truth emerges, they realize {revelation} and nobody can be trusted.",
        "Someone is {threat}. {protagonist} has {time_limit} to stop them, but the killer is always one step ahead. A taut thriller about {theme} and paranoia.",
        "When {protagonist} witnesses {event}, they become the target of {antagonist}. A cat-and-mouse game ensues through {setting} with deadly consequences.",
    ],
    "Horror": [
        "{family} moves into {location}, unaware of {horror}. As {events} escalate, they realize the house holds {secret} connected to {backstory}.",
        "{protagonist} and friends visit {location} for {reason}. One by one, they fall victim to {horror}. Only by understanding {mystery} can anyone survive.",
        "After {event}, {protagonist} begins experiencing {horror}. Is it {explanation1} or {explanation2}? The terrifying truth is far worse than either.",
        "{setting} is haunted by {entity} seeking {goal}. {protagonist} must confront {fear} to stop the {horror} before {consequence}.",
        "Something ancient awakens in {location}. {protagonist}, a {occupation}, must use {knowledge} to combat {horror} that threatens to {consequence}.",
    ],
    "Comedy": [
        "{protagonist}, a lovable {occupation}, accidentally {incident} and must {mission} before {deadline}. Hilarious chaos ensues involving {element1} and {element2}.",
        "When {situation}, {protagonist} and {character} are forced to work together despite their differences. What starts as {conflict} becomes an unlikely {relationship}.",
        "{protagonist} pretends to be {fake_identity} to {goal}, but the lies spiral out of control when {complication}. A screwball comedy about {theme}.",
        "A group of {characters} attempt {plan} that goes hilariously wrong at every turn. Features {style} humor and heartfelt moments about {theme}.",
        "{protagonist}'s life is turned upside down when {event}. Armed with {quality} and terrible {skill}, they stumble through {situation} in this feel-good comedy.",
    ],
    "Romance": [
        "{protagonist1} and {protagonist2} meet under {circumstances}. Despite {obstacle}, they discover {connection} that transforms both their lives. A story about {theme}.",
        "In {setting}, {protagonist} isn't looking for love until {character} arrives and challenges everything they thought they wanted. {obstacle} threatens to tear them apart.",
        "{protagonist} must choose between {choice1} and {choice2} in this sweeping romance set against {backdrop}. A tale of {theme1} and {theme2}.",
        "Years after {past_event}, {protagonist1} and {protagonist2} reunite. Old feelings resurface alongside old wounds in this mature exploration of {theme}.",
        "Two people from different {difference} find connection through {shared_element}. But when {conflict} arises, they must decide if love is worth {sacrifice}.",
    ],
    "Animation": [
        "In a world where {premise}, young {protagonist} dreams of {goal}. With the help of {sidekick}, they embark on an adventure to {mission} and discover {lesson}.",
        "{protagonist}, a {creature}, must journey through {world} to save {stakes}. Along the way, they learn about {theme} and find unexpected allies in {characters}.",
        "When {disaster} threatens {world}, an unlikely hero emerges. {protagonist} must master {ability} and unite {groups} to restore {goal}.",
        "The magical world of {setting} comes alive in this tale of {protagonist} who {situation}. A visually stunning adventure about {theme1} and {theme2}.",
        "{protagonist} discovers they are {revelation} and must navigate {world} while learning to {ability}. A heartfelt story about {theme} and finding where you belong.",
    ],
    "War": [
        "Based on {inspiration}, this film follows {protagonist} through {conflict}. Amid the horrors of war, moments of {element} reveal the cost of {theme}.",
        "{unit} is sent on {mission} behind enemy lines during {war}. As casualties mount, {protagonist} must lead the survivors through {obstacle} to {goal}.",
        "Through the eyes of {protagonist}, a {occupation}, we witness the {battle}. A harrowing portrayal of war's impact on {aspect} and the human spirit.",
        "{protagonist} struggles to survive in {location} during {war}. When {event} changes everything, they must choose between {choice1} and {choice2}.",
        "Two soldiers from opposite sides of {conflict} form an unlikely bond. {protagonist} and {character} discover {theme} transcends the lines drawn by war.",
    ],
    "Mystery": [
        "When {victim} is found {state} in {location}, {detective} must unravel a web of {elements} to find the killer. Everyone has secrets in this {style} mystery.",
        "{protagonist} receives {clue} that leads them into {investigation}. Each answer raises more questions in this twisting tale of {theme} and deception.",
        "A locked-room mystery: {scenario}. {detective} must determine how {crime} was committed and who among the {suspects} is responsible.",
        "{protagonist}, a {occupation}, notices {detail} that others miss. This observation leads to uncovering {conspiracy} that someone will kill to keep hidden.",
        "The disappearance of {person} from {setting} seems straightforward until {protagonist} discovers {revelation}. Nothing is as it appears in this atmospheric mystery.",
    ],
    "Crime": [
        "{protagonist} plans the perfect {crime}, but when {complication} throws everything into chaos, loyalties are tested and blood is spilled. A {style} crime saga.",
        "Rise and fall of {protagonist} in the {setting} underworld. From {beginning} to {end}, witness the cost of {theme} in this sprawling crime epic.",
        "{detective} pursues {criminal} across {locations} in this tense cat-and-mouse thriller. Both hunter and hunted blur the line between {duality}.",
        "When {event} disrupts the criminal ecosystem of {city}, various {players} compete to fill the void. A multi-perspective crime drama about {theme}.",
        "{protagonist}, a {occupation}, gets pulled into {criminal_world} when {situation}. To survive, they must become something they never thought possible.",
    ],
    "Fantasy": [
        "In the realm of {world}, {protagonist} discovers they are {revelation}. To save {stakes}, they must find {macguffin} and defeat {antagonist}.",
        "{protagonist}, a humble {occupation}, is thrust into adventure when {event}. With companions {characters}, they journey to {destination} facing {obstacles}.",
        "Ancient prophecy speaks of {prophecy}. {protagonist} may be the one to fulfill it, but first must overcome {challenge} and master {ability}.",
        "Magic returns to {world} after {time}. {protagonist} must navigate {political_situation} while unlocking {power} that could save or destroy everything.",
        "Two worlds collide when {event}. {protagonist} from {world1} and {character} from {world2} must work together to prevent {catastrophe}.",
    ],
    "Adventure": [
        "{protagonist} discovers {clue} leading to {treasure}. Racing against {antagonist}, they journey through {locations} facing {dangers} at every turn.",
        "Stranded in {location}, {protagonist} must survive {challenges} while searching for {goal}. An epic tale of human endurance and {theme}.",
        "{protagonist} assembles a team of {specialists} for an impossible {mission}: {objective}. Each member brings {skill}, but can they trust each other?",
        "The map to {destination} falls into {protagonist}'s hands. What begins as {motivation} becomes a journey of {transformation} through {world}.",
        "{protagonist} and {companion} traverse {landscape} in search of {goal}. Along the way, they encounter {elements} that test their {qualities}.",
    ],
    "Western": [
        "In the lawless town of {town}, {protagonist}, a {occupation}, stands against {antagonist} and their gang. A classic tale of {theme} in the Old West.",
        "{protagonist} rides across the frontier seeking {goal}. But the West is changing, and they must confront {reality} while staying true to {code}.",
        "Revenge drives {protagonist} to hunt {antagonist} across {territory}. A brutal, beautiful Western about the price of {theme}.",
        "When {event} threatens {settlement}, unlikely allies must unite. {protagonist}, {character1}, and {character2} face impossible odds in this ensemble Western.",
        "The final days of the Old West. {protagonist}, a legendary {occupation}, finds the world has no place for people like them. A meditation on {theme}.",
    ],
    "Biography": [
        "The extraordinary life of {person}, who rose from {origin} to {achievement}. Through {obstacles}, their story inspires {theme}.",
        "Before they changed the world, {person} was {origin_description}. This intimate portrait reveals the {quality} behind the legend.",
        "{person}'s struggle against {opposition} defined an era. Based on true events, witness their fight for {cause} that cost them {sacrifice}.",
        "The untold story of {person} and their role in {event}. History books remember {public_achievement}, but the truth is more complex.",
        "Spanning {time_period}, this epic chronicles {person}'s journey from {beginning} to {legacy}. A testament to human {quality}.",
    ],
    "Noir": [
        "In the rain-soaked streets of {city}, {detective} takes a case that will drag them into {underworld}. Nothing is clean in this {style} noir.",
        "{protagonist} thought they'd left {past} behind. But when {femme_fatale} walks in with {problem}, they're pulled back into the shadows.",
        "Everyone has an angle in {setting}. {protagonist} must navigate {web} while staying alive long enough to find {goal}. Classic noir at its finest.",
        "A voice from the past. A body in {location}. {protagonist} has {time} to solve the case before becoming the next victim in this atmospheric noir.",
        "{protagonist}, a {occupation}, stumbles into {conspiracy}. Double-crosses and dark alleys await in this homage to classic film noir.",
    ],
}

# Fill-in values for templates
FILL_VALUES = {
    "technology": ["neural interfaces control everything", "AI governs society", "teleportation is commonplace",
                   "consciousness can be uploaded", "genetic modification defines class", "time travel exists",
                   "virtual reality replaces real life", "faster-than-light travel connects galaxies"],
    "protagonist": ["Maya", "Jack", "Elena", "Marcus", "Dr. Chen", "Agent Torres", "Detective Kim", "Sarah",
                    "Alex", "Jordan", "The Stranger", "Emma", "Michael", "Luna", "Kai", "Professor Hayes"],
    "mission": ["infiltrate the system", "rescue the hostages", "stop the weapon", "find the cure",
                "expose the truth", "save their family", "prevent the apocalypse", "escape the facility"],
    "threat": ["it's too late", "the corporation wins", "civilization falls", "they lose everything",
               "the loop resets", "the portal closes forever", "the system becomes unstoppable"],
    "revelation": ["the truth about their past", "a conspiracy spanning decades", "the nature of reality itself",
                   "who they really are", "what the government has hidden", "the cost of progress"],
    "theme": ["identity", "freedom", "what it means to be human", "the price of progress", "love",
              "sacrifice", "redemption", "power", "family", "truth", "justice", "survival"],
    "disaster": ["the collapse", "the plague", "the war", "the flood", "first contact", "the singularity"],
    "location": ["an underground city", "a space station", "a remote island", "an old mansion",
                 "the desert", "New York", "Tokyo", "a small town", "the mountains", "the ocean depths"],
    "occupation": ["scientist", "soldier", "detective", "teacher", "artist", "pilot", "doctor", "hacker",
                   "journalist", "chef", "mechanic", "professor", "nurse", "architect", "musician"],
    "antagonist": ["the Corporation", "General Kane", "Dr. Vex", "the Syndicate", "the Algorithm",
                   "Marcus Stone", "the Shadow Council", "the Collective", "Director Hayes"],
    "mystery": ["their origin", "the disappearances", "the signal", "the artifact", "the murders",
                "the prophecy", "the code", "the ritual", "their connection"],
    "setting": ["a space colony", "post-war Europe", "1920s Chicago", "a remote village", "the suburbs",
                "a prestigious university", "a dying town", "the criminal underworld", "high society"],
    "past": ["the accident", "their childhood", "the war", "their former life", "the trauma",
             "their marriage", "their career", "the incident"],
    "discovery": ["alien technology", "a cure for death", "evidence of conspiracy", "ancient texts",
                  "a parallel universe", "the truth about history", "a new element"],
    "consequence": ["destroy humanity", "start a war", "change history", "unleash chaos", "end everything"],
    "team": ["specialists", "misfits", "scientists", "soldiers", "survivors", "rebels"],
    "stakes": ["humanity", "the city", "the world", "their family", "the future", "everything"],
    "year": ["2084", "2150", "the year 3000", "2047", "the near future", "a dystopian future"],
    "backstory": ["lost everything in the war", "was created in a lab", "escaped the system",
                  "remembers a different timeline", "was betrayed by those they trusted"],
    "conflict": ["a power struggle", "a revolution", "a conspiracy", "a war", "a hunt"],
    "problem": ["addiction", "grief", "guilt", "isolation", "a dark secret", "illness", "debt"],
    "resolution": ["hope", "purpose", "peace", "love", "redemption", "acceptance"],
    "relationship": ["an unlikely friendship", "a forbidden romance", "reconnecting with family",
                     "finding community", "a mentorship"],
    "backdrop": ["the Civil Rights movement", "World War II", "the Great Depression", "modern America",
                 "industrial revolution", "the tech boom"],
    "family_name": ["Morrison", "Chen", "Garcia", "O'Brien", "Yamamoto", "Anderson", "Okafor"],
    "time_period": ["a summer in the 1960s", "the tumultuous 1990s", "wartime Britain", "the Roaring Twenties"],
    "tragedy": ["losing a child", "a devastating accident", "betrayal", "the death of a spouse", "a scandal"],
    "character": ["a kindred spirit", "an unlikely mentor", "someone from their past", "a mysterious stranger"],
    "lesson": ["the meaning of forgiveness", "what truly matters", "how to let go", "the power of connection"],
    "transformation": ["self-discovery", "healing", "acceptance", "redemption"],
    "quality": ["courage", "faith", "integrity", "love", "hope", "resilience"],
    "goal": ["justice", "recognition", "freedom", "equality", "survival", "peace"],
    "opposition": ["systemic oppression", "powerful interests", "their own demons", "impossible odds"],
    "inspiration": ["true events", "a remarkable life", "a forgotten hero", "historical records"],
    "struggle": ["extraordinary resilience", "unwavering determination", "quiet courage"],
    "operation": ["heist", "rescue", "mission", "extraction", "delivery"],
    "complication": ["betrayal", "an ambush", "a double-cross", "unexpected enemies"],
    "time_limit": ["24 hours", "before dawn", "one week", "until midnight"],
    "betrayal": ["their partner's death", "being framed", "losing everything", "the ultimate betrayal"],
    "organization": ["criminal empire", "shadow government", "terrorist network", "corporate conspiracy"],
    "locations": ["three continents", "the criminal underworld", "hostile territory", "major cities"],
    "action_style": ["brutal", "balletic", "explosive", "tactical", "relentless"],
    "enemies": ["assassins", "the government", "his former allies", "an army"],
    "skills": ["lethal training", "sharp instincts", "military experience", "hacking abilities"],
    "element": ["lies", "deceit", "manipulation", "paranoia", "obsession", "betrayal"],
    "message": ["a cryptic letter", "a strange phone call", "an anonymous tip", "a warning"],
    "situation": ["a nightmare", "a web of lies", "mortal danger", "a deadly game"],
    "event": ["the murder", "the accident", "the disappearance", "the discovery"],
    "family": ["The Johnsons", "A young couple", "The Marshalls", "A single mother and her children"],
    "horror": ["its violent past", "an ancient evil", "something watching them", "the curse"],
    "events": ["strange occurrences", "violent incidents", "terrifying visions", "possessions"],
    "secret": ["a terrible truth", "buried sins", "an ancient ritual", "trapped souls"],
    "reason": ["a vacation", "an inheritance", "work", "a dare", "research"],
    "explanation1": ["madness", "trauma", "illness", "imagination"],
    "explanation2": ["something supernatural", "a curse", "possession", "a haunting"],
    "entity": ["a vengeful spirit", "an ancient demon", "the darkness", "something unspeakable"],
    "fear": ["their deepest terror", "the past", "their own guilt", "the unknown"],
    "knowledge": ["ancient lore", "science", "faith", "forbidden knowledge"],
    "incident": ["switches bodies with their boss", "inherits a zoo", "crashes a wedding",
                 "becomes famous", "gets stuck in a time loop"],
    "deadline": ["the big day", "their parents visit", "the wedding", "the presentation"],
    "element1": ["mistaken identities", "a talking animal", "awkward relatives", "social media disasters"],
    "element2": ["romantic complications", "physical comedy", "fish-out-of-water situations"],
    "fake_identity": ["a doctor", "royalty", "an expert", "their ex's new partner", "a celebrity"],
    "characters": ["friends", "coworkers", "strangers on a trip", "wedding guests", "neighbors"],
    "plan": ["a heist", "winning back an ex", "avoiding work", "throwing a party", "a road trip"],
    "style": ["dark", "physical", "witty", "absurdist", "deadpan", "heartfelt"],
    "protagonist1": ["Sophie", "Tom", "Maria", "David", "Claire", "Ben"],
    "protagonist2": ["Alex", "James", "Nina", "Carlos", "Emma", "Michael"],
    "circumstances": ["impossible circumstances", "by chance", "through friends", "at work", "in Paris"],
    "obstacle": ["distance", "past pain", "family opposition", "career ambitions", "timing"],
    "connection": ["a deep bond", "unexpected love", "a shared destiny", "true partnership"],
    "choice1": ["safety", "duty", "the familiar", "their dreams"],
    "choice2": ["love", "passion", "the unknown", "their heart"],
    "past_event": ["their breakup", "graduation", "the summer", "that night"],
    "difference": ["worlds", "backgrounds", "generations", "countries", "classes"],
    "shared_element": ["music", "art", "a project", "tragedy", "dance", "food"],
    "sacrifice": ["the risk", "everything they've built", "their reputation", "their dreams"],
    "premise": ["toys come alive", "animals talk", "magic exists", "machines have feelings"],
    "sidekick": ["loyal companion", "wisecracking friend", "magical creature", "unlikely ally"],
    "creature": ["young dragon", "lost robot", "magical being", "forest spirit", "small monster"],
    "world": ["their kingdom", "the magical realm", "the ecosystem", "their home"],
    "characters": ["a ragtag group", "sworn enemies", "animal friends", "magical beings"],
    "groups": ["the warring factions", "different species", "the kingdoms", "unlikely allies"],
    "ability": ["their unique power", "the ancient art", "their true potential", "forgotten magic"],
    "world1": ["the modern world", "the magical realm", "above ground", "the human world"],
    "world2": ["a hidden kingdom", "the spirit world", "beneath the sea", "the fairy realm"],
    "catastrophe": ["the destruction of both worlds", "eternal darkness", "the end of magic"],
    "unit": ["A squad of soldiers", "A special forces team", "A group of volunteers", "The remnants"],
    "war": ["World War II", "Vietnam", "World War I", "the Civil War", "a future conflict"],
    "battle": ["D-Day", "the Pacific theater", "the trenches", "the siege", "the offensive"],
    "aspect": ["the soul", "families", "innocence", "brotherhood", "humanity"],
    "detective": ["Detective Rivera", "Inspector Mills", "Agent Stone", "Private eye Jack"],
    "victim": ["a wealthy heiress", "the CEO", "a prominent figure", "a stranger"],
    "state": ["dead", "missing", "changed", "with a cryptic message"],
    "elements": ["jealousy, greed, and old grudges", "corporate espionage", "family secrets"],
    "clue": ["a mysterious package", "a coded message", "an old photograph", "a dying whisper"],
    "investigation": ["a world of secrets", "a cold case", "dangerous territory", "the past"],
    "suspects": ["guests", "family members", "colleagues", "residents"],
    "scenario": ["a billionaire dead in his locked study", "a murder on a train",
                 "an impossible theft"],
    "crime": ["the murder", "the theft", "the disappearance"],
    "conspiracy": ["a vast conspiracy", "a cover-up", "a pattern others missed"],
    "detail": ["something others overlook", "a small inconsistency", "a telling pattern"],
    "criminal": ["a mastermind", "a serial killer", "an elusive thief", "a kingpin"],
    "duality": ["law and chaos", "justice and revenge", "duty and obsession"],
    "city": ["the city", "Los Angeles", "New York", "Chicago", "London", "Tokyo"],
    "players": ["crime families", "gangs", "ambitious newcomers", "corrupt officials"],
    "criminal_world": ["organized crime", "the drug trade", "underground fighting", "smuggling"],
    "macguffin": ["the sacred amulet", "the ancient sword", "the lost artifact", "the crystal"],
    "prophecy": ["a chosen one", "the end times", "a great war", "the return of magic"],
    "challenge": ["their fears", "impossible trials", "their own darkness", "political intrigue"],
    "power": ["ancient magic", "forbidden powers", "their birthright", "the source"],
    "political_situation": ["a court of vipers", "a war for succession", "political intrigue"],
    "treasure": ["legendary gold", "an ancient artifact", "lost technology", "a sacred relic"],
    "dangers": ["traps", "rivals", "the elements", "ancient guardians", "betrayal"],
    "specialists": ["experts", "misfits", "professionals", "veterans", "talented outcasts"],
    "objective": ["steal the impossible", "reach the unreachable", "survive the unsurvivable"],
    "skill": ["unique abilities", "particular expertise", "a crucial role"],
    "landscape": ["dangerous terrain", "hostile wilderness", "uncharted territory"],
    "companion": ["a loyal friend", "an unlikely ally", "their sworn enemy", "a mysterious guide"],
    "elements": ["strange cultures", "dangerous creatures", "moral dilemmas", "ancient ruins"],
    "qualities": ["resolve", "friendship", "character", "beliefs"],
    "town": ["Redemption", "Deadwood", "Tombstone", "Purgatory", "Last Chance"],
    "territory": ["the territories", "three states", "lawless land", "the frontier"],
    "code": ["their personal code", "the old ways", "their honor", "the law"],
    "settlement": ["the town", "the homesteaders", "the tribe", "the valley"],
    "character1": ["an outlaw", "a former enemy", "a woman with secrets"],
    "character2": ["a native guide", "a greenhorn", "a preacher"],
    "person": ["Albert Einstein", "Marie Curie", "Abraham Lincoln", "a forgotten pioneer",
               "an unsung hero", "a visionary leader"],
    "origin": ["poverty", "obscurity", "discrimination", "humble beginnings", "tragedy"],
    "achievement": ["change the world", "make history", "revolutionize their field", "inspire millions"],
    "obstacles": ["prejudice", "personal tragedy", "political opposition", "their own flaws"],
    "origin_description": ["nobody special", "struggling", "dismissed", "underestimated"],
    "cause": ["justice", "equality", "freedom", "recognition", "their people"],
    "public_achievement": ["the victory", "the discovery", "the achievement"],
    "beginning": ["nothing", "tragedy", "obscurity"],
    "legacy": ["legend", "their lasting impact", "immortality"],
    "underworld": ["a world of corruption", "the criminal depths", "dangerous territory"],
    "femme_fatale": ["a mysterious woman", "trouble in heels", "someone from the past"],
    "web": ["lies and betrayal", "corruption and vice", "dangerous games"],
}

def fill_template(template: str, values: dict) -> str:
    """Fill in a template with random values."""
    result = template
    import re
    placeholders = re.findall(r'\{(\w+)\}', template)

    for placeholder in placeholders:
        if placeholder in values:
            replacement = random.choice(values[placeholder])
            result = result.replace('{' + placeholder + '}', replacement, 1)

    return result

def generate_movie_title() -> str:
    """Generate a movie title."""
    patterns = [
        ["The", ["Last", "Final", "First", "Lost", "Dark", "Silent", "Forgotten", "Eternal", "Hidden", "Secret"],
         ["Night", "Day", "Hour", "Dawn", "Storm", "Dream", "Shadow", "Light", "Truth", "Promise"]],
        [["Dark", "Bright", "Cold", "Deep", "High", "Long", "Short", "Hard", "Soft", "Sharp"],
         ["Water", "Fire", "Earth", "Sky", "Road", "Path", "Line", "Edge", "Point", "Corner"]],
        ["The", ["Man", "Woman", "Girl", "Boy", "King", "Queen", "Stranger", "Ghost", "Hunter", "Witness"],
         ["Who", "in", "from", "of", "with"], ["Knew", "the", "Too Much", "Everything", "Nothing", "Shadows", "Time"]],
        [["Blood", "Iron", "Steel", "Gold", "Silver", "Stone", "Glass", "Paper", "Silk", "Ice"],
         ["and", "&"], ["Honor", "Fire", "Thunder", "Lightning", "Tears", "Dreams", "Bones", "Roses"]],
        [["Running", "Falling", "Rising", "Burning", "Breaking", "Chasing", "Hunting", "Finding", "Losing", "Seeking"],
         ["Down", "Up", "Away", "Home", "Free", "Wild", "Alone", "Together"]],
        ["The", ["Great", "Big", "Little", "Old", "New", "Last", "Next", "Other", "Same"],
         ["Escape", "Heist", "Robbery", "Game", "Hunt", "Race", "Chase", "Journey", "Adventure"]],
        [["One", "Two", "Three", "Seven", "Twelve", "A Hundred", "A Thousand"],
         ["Days", "Nights", "Hours", "Years", "Lives", "Chances", "Reasons", "Seconds", "Moments"]],
        [["Project", "Operation", "Mission", "Protocol", "Program", "Initiative", "Code Name:"],
         ["Phoenix", "Shadow", "Titan", "Genesis", "Exodus", "Trinity", "Omega", "Alpha", "Delta", "Echo"]],
    ]

    pattern = random.choice(patterns)
    title_parts = []
    for part in pattern:
        if isinstance(part, list):
            title_parts.append(random.choice(part))
        else:
            title_parts.append(part)

    return " ".join(title_parts)

def generate_movie() -> dict:
    """Generate a single movie entry."""
    genre = random.choice(GENRES)
    year = random.randint(1960, 2024)
    director = random.choice(DIRECTORS)

    # Generate plot from template
    templates = PLOT_TEMPLATES.get(genre, PLOT_TEMPLATES["Drama"])
    plot_template = random.choice(templates)
    plot = fill_template(plot_template, FILL_VALUES)

    # Generate rating (slightly weighted toward higher ratings)
    rating = round(random.triangular(5.0, 10.0, 7.5), 1)

    # Generate runtime
    runtime = random.randint(85, 180)

    return {
        "title": generate_movie_title(),
        "year": year,
        "director": director,
        "genre": genre,
        "plot": plot,
        "rating": rating,
        "runtime_minutes": runtime
    }

def insert_movies(movies: list):
    """Insert movies into database."""
    sql = """
        INSERT INTO rag_movies (title, year, director, genre, plot, rating, runtime_minutes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """

    with get_cursor() as cursor:
        for movie in movies:
            cursor.execute(sql, (
                movie["title"],
                movie["year"],
                movie["director"],
                movie["genre"],
                movie["plot"],
                movie["rating"],
                movie["runtime_minutes"]
            ))

def main():
    """Generate and insert 1000 movies."""
    print("=" * 50)
    print("BULK MOVIE GENERATION")
    print("=" * 50)

    # Check current count
    result = execute_query("SELECT COUNT(*) as count FROM rag_movies")
    current_count = result[0]['count'] if result else 0
    print(f"\nCurrent movie count: {current_count}")

    target = 1000
    to_generate = max(0, target - current_count)

    if to_generate == 0:
        print(f"Already have {current_count} movies. No generation needed.")
        return

    print(f"Generating {to_generate} new movies...")

    movies = []
    for i in range(to_generate):
        movie = generate_movie()
        movies.append(movie)
        if (i + 1) % 100 == 0:
            print(f"  Generated {i + 1}/{to_generate} movies...")

    print(f"\nInserting {len(movies)} movies into database...")
    insert_movies(movies)

    # Verify
    result = execute_query("SELECT COUNT(*) as count FROM rag_movies")
    new_count = result[0]['count'] if result else 0
    print(f"New movie count: {new_count}")

    print("\n" + "=" * 50)
    print("GENERATION COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    main()
