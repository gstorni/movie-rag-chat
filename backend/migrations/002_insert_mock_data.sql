-- Mock Movie Data for RAG Experiment
-- 50+ movies with detailed plots for semantic search

INSERT INTO rag_movies (title, year, director, genre, plot, rating, runtime_minutes) VALUES

-- Sci-Fi Classics
('Blade Runner', 1982, 'Ridley Scott', 'Sci-Fi', 'In a dystopian Los Angeles of 2019, former police officer Rick Deckard is forced to hunt down and "retire" four replicants who have escaped from an off-world colony. As he tracks them, he begins to question his own humanity and the nature of what it means to be alive. The film explores themes of identity, memory, and mortality through rain-soaked neon cityscapes.', 8.1, 117),

('2001: A Space Odyssey', 1968, 'Stanley Kubrick', 'Sci-Fi', 'A mysterious black monolith appears at the dawn of humanity, sparking evolution. Millions of years later, another monolith is discovered on the Moon, leading to a mission to Jupiter. The spacecraft''s AI, HAL 9000, malfunctions with deadly consequences as astronaut Dave Bowman must confront the unknown alone in this meditative exploration of human evolution and artificial intelligence.', 8.3, 149),

('The Matrix', 1999, 'Wachowskis', 'Sci-Fi', 'Computer hacker Neo discovers that reality as he knows it is a simulation created by machines to enslave humanity. Guided by the mysterious Morpheus and the warrior Trinity, Neo learns to bend the rules of the Matrix and embraces his destiny as "The One" who will free humanity from digital imprisonment.', 8.7, 136),

('Interstellar', 2014, 'Christopher Nolan', 'Sci-Fi', 'As Earth becomes increasingly uninhabitable, a team of astronauts travels through a wormhole near Saturn in search of a new home for humanity. Cooper, a former pilot and father, must navigate the relativistic effects of space travel, knowing that years pass on Earth while only hours pass for him, all while confronting love as a force that transcends dimensions.', 8.6, 169),

('Arrival', 2016, 'Denis Villeneuve', 'Sci-Fi', 'When twelve mysterious spacecraft land around the world, linguist Louise Banks is recruited to communicate with the alien visitors. As she learns their circular language, she begins to perceive time non-linearly, facing profound personal revelations about free will, loss, and the nature of time itself.', 7.9, 116),

('Ex Machina', 2014, 'Alex Garland', 'Sci-Fi', 'Programmer Caleb wins a contest to spend a week at the isolated estate of tech CEO Nathan. There, he discovers Nathan has created Ava, an advanced AI with human appearance. Caleb is tasked with determining if Ava has true consciousness, but becomes entangled in a psychological game where nothing is as it seems.', 7.7, 108),

('Dune', 2021, 'Denis Villeneuve', 'Sci-Fi', 'Paul Atreides, heir to House Atreides, must travel to the most dangerous planet in the universe, Arrakis, the only source of the valuable spice melange. When his family is betrayed, Paul must embrace his prophetic destiny among the desert-dwelling Fremen to avenge his father and fulfill an ancient prophecy.', 8.0, 155),

('Gattaca', 1997, 'Andrew Niccol', 'Sci-Fi', 'In a future where genetic engineering determines social class, Vincent Freeman, born naturally with a heart defect, dreams of space travel. He assumes the identity of a genetically superior man to infiltrate the Gattaca space program, proving that human spirit can overcome genetic determinism.', 7.8, 106),

-- Drama Masterpieces
('The Shawshank Redemption', 1994, 'Frank Darabont', 'Drama', 'Banker Andy Dufresne is sentenced to life in Shawshank prison for a crime he didn''t commit. Over two decades, he maintains his innocence and hope, befriending fellow inmate Red and secretly working on an elaborate escape plan. A profound meditation on hope, friendship, and the human spirit''s ability to endure.', 9.3, 142),

('The Godfather', 1972, 'Francis Ford Coppola', 'Drama', 'The aging patriarch of the Corleone crime family transfers control to his reluctant youngest son Michael. Initially wanting nothing to do with the family business, Michael is drawn deeper into the world of organized crime after an assassination attempt on his father, transforming from war hero to ruthless mob boss.', 9.2, 175),

('Schindler''s List', 1993, 'Steven Spielberg', 'Drama', 'German industrialist Oskar Schindler becomes an unlikely savior during the Holocaust, using his factory to employ and protect over 1,100 Jewish workers from Nazi concentration camps. The film chronicles his transformation from opportunistic businessman to humanitarian hero through the horrors of World War II.', 9.0, 195),

('Forrest Gump', 1994, 'Robert Zemeckis', 'Drama', 'Forrest Gump, a man with a low IQ but pure heart, accidentally influences several major historical events in the 20th century American history. Through running, war heroism, ping pong diplomacy, and shrimp fishing, Forrest''s simple wisdom and unwavering love for Jenny provide a unique lens on American culture.', 8.8, 142),

('The Green Mile', 1999, 'Frank Darabont', 'Drama', 'Death row supervisor Paul Edgecomb discovers that giant inmate John Coffey possesses supernatural healing powers. As Paul witnesses miracles and confronts the injustice of Coffey''s conviction, he must face the moral complexity of executing a man who may be innocent and divine.', 8.6, 189),

('A Beautiful Mind', 2001, 'Ron Howard', 'Drama', 'Brilliant mathematician John Nash struggles with schizophrenia while making groundbreaking contributions to game theory. The film follows his journey from Princeton prodigy through mental illness and back, ultimately winning the Nobel Prize while learning to live with his condition through the support of his wife Alicia.', 8.2, 135),

-- Thrillers & Crime
('Pulp Fiction', 1994, 'Quentin Tarantino', 'Crime', 'Interconnected stories of Los Angeles criminals weave together: hitmen Vincent and Jules philosophize between jobs, boxer Butch double-crosses a mob boss, and a date between Vincent and his boss''s wife goes horribly wrong. Tarantino''s non-linear narrative revolutionized independent cinema.', 8.9, 154),

('The Dark Knight', 2008, 'Christopher Nolan', 'Action', 'Batman faces his greatest psychological challenge when the Joker, an agent of chaos, terrorizes Gotham City. As the Joker''s schemes force Batman, Commissioner Gordon, and District Attorney Harvey Dent into impossible moral choices, the line between hero and vigilante blurs in this exploration of chaos versus order.', 9.0, 152),

('Fight Club', 1999, 'David Fincher', 'Thriller', 'An insomniac office worker meets charismatic soap salesman Tyler Durden and forms an underground fight club that evolves into something more sinister. The film explores masculinity, consumerism, and identity through increasingly violent and anarchic acts, building to a shocking revelation about the narrator''s true nature.', 8.8, 139),

('Se7en', 1995, 'David Fincher', 'Thriller', 'Retiring detective Somerset and his hot-headed replacement Mills hunt a serial killer who stages elaborate murders based on the seven deadly sins. As they race to prevent more deaths, the case takes them into the darkest corners of human depravity, culminating in an unforgettable confrontation.', 8.6, 127),

('The Silence of the Lambs', 1991, 'Jonathan Demme', 'Thriller', 'FBI trainee Clarice Starling seeks the help of imprisoned cannibalistic psychiatrist Dr. Hannibal Lecter to catch another serial killer known as Buffalo Bill. The psychological cat-and-mouse game between Clarice and Lecter becomes as compelling as the hunt for the killer she seeks.', 8.6, 118),

('No Country for Old Men', 2007, 'Coen Brothers', 'Thriller', 'When hunter Llewelyn Moss finds drug money in the Texas desert, he sets off a violent chain of events. Psychopathic killer Anton Chigurh pursues him with relentless determination while aging Sheriff Bell tries to understand the modern evil he faces. A meditation on fate, violence, and moral decay.', 8.2, 122),

('Zodiac', 2007, 'David Fincher', 'Thriller', 'Based on true events, this film follows the investigation of the Zodiac Killer who terrorized San Francisco in the late 1960s and 70s. Cartoonist Robert Graysmith becomes obsessed with identifying the killer, spending decades pursuing clues while the case destroys careers and relationships.', 7.7, 157),

-- War Films
('Saving Private Ryan', 1998, 'Steven Spielberg', 'War', 'Following the D-Day invasion of Normandy, Captain John Miller leads a squad through enemy territory to find and bring home Private James Ryan, whose three brothers have all been killed in action. The mission forces the soldiers to question the value of one life against many in the chaos of war.', 8.6, 169),

('Apocalypse Now', 1979, 'Francis Ford Coppola', 'War', 'During the Vietnam War, Captain Willard is sent on a classified mission up the Nung River into Cambodia to assassinate Colonel Kurtz, a decorated officer who has gone insane and set himself up as a god among local tribesmen. The journey becomes a surreal descent into the heart of darkness and madness of war.', 8.5, 147),

('Full Metal Jacket', 1987, 'Stanley Kubrick', 'War', 'The film follows a squad of Marines through brutal boot camp under sadistic Sergeant Hartman, then into the urban warfare of the Tet Offensive in Vietnam. Private Joker struggles to maintain his humanity while documenting the war''s absurdity as a military journalist, confronting the duality of man.', 8.3, 116),

('Dunkirk', 2017, 'Christopher Nolan', 'War', 'The evacuation of Allied soldiers from the beaches of Dunkirk is told through three perspectives on land, sea, and air, each operating on different time scales. With minimal dialogue, the film creates an immersive sensory experience of survival, heroism, and the desperate scramble to escape encircling German forces.', 7.8, 106),

('1917', 2019, 'Sam Mendes', 'War', 'Two young British soldiers are given an impossible mission during World War I: cross enemy territory in one day to deliver a message that will stop 1,600 men from walking into a deadly trap. Shot to appear as one continuous take, the film creates unprecedented immersion in their harrowing journey.', 8.3, 119),

-- Animation
('Spirited Away', 2001, 'Hayao Miyazaki', 'Animation', 'Ten-year-old Chihiro stumbles into a magical world of spirits and gods when her parents are transformed into pigs for eating enchanted food. To save them, she must work in a bathhouse for spirits and learn courage, resourcefulness, and the power of identity as she navigates this mysterious realm.', 8.6, 125),

('WALL-E', 2008, 'Andrew Stanton', 'Animation', 'In a future where Earth has been abandoned due to pollution, a lonely waste-collecting robot named WALL-E falls in love with a sleek reconnaissance robot named EVE. His pursuit of love leads him across the galaxy to rediscover what it means to be alive and restore hope for humanity''s return to Earth.', 8.4, 98),

('The Lion King', 1994, 'Roger Allers', 'Animation', 'Young lion prince Simba flees his homeland after his evil uncle Scar murders his father and convinces him he''s responsible. Years later, with help from carefree friends Timon and Pumbaa, Simba must confront his past and reclaim his rightful place as king. A coming-of-age tale of responsibility and identity.', 8.5, 88),

('Toy Story', 1995, 'John Lasseter', 'Animation', 'Woody, a cowboy doll, is Andy''s favorite toy until the arrival of Buzz Lightyear, a space ranger who doesn''t realize he''s a toy. Their rivalry evolves into friendship as they must work together to reunite with Andy after getting lost. The groundbreaking first fully computer-animated feature film.', 8.3, 81),

('Coco', 2017, 'Lee Unkrich', 'Animation', 'Aspiring musician Miguel accidentally enters the Land of the Dead during Día de los Muertos and must seek help from his deceased relatives to return to the living world. The journey reveals family secrets and the importance of remembering those who came before us.', 8.4, 105),

-- Horror
('The Shining', 1980, 'Stanley Kubrick', 'Horror', 'Jack Torrance takes a winter caretaker job at the isolated Overlook Hotel with his wife Wendy and psychic son Danny. As supernatural forces and cabin fever take hold, Jack descends into madness while Danny''s "shining" reveals the hotel''s horrific history and the danger they face.', 8.4, 146),

('Get Out', 2017, 'Jordan Peele', 'Horror', 'Black photographer Chris visits his white girlfriend''s family estate, where the overly accommodating behavior of the parents and the strange demeanor of the Black servants hint at something sinister. The weekend visit becomes a nightmarish trap revealing horrific secrets about liberal racism.', 7.7, 104),

('Hereditary', 2018, 'Ari Aster', 'Horror', 'After the family matriarch dies, the Graham family begins unraveling as terrifying secrets and a sinister presence haunt them. As daughter Charlie''s increasingly disturbing behavior escalates, mother Annie discovers their family''s dark history and the nightmare they''ve inherited.', 7.3, 127),

('The Exorcist', 1973, 'William Friedkin', 'Horror', 'When young Regan MacNeil begins exhibiting strange and violent behavior, her desperate mother seeks help from two priests to save her daughter from demonic possession. The battle between good and evil culminates in one of cinema''s most terrifying confrontations with the supernatural.', 8.1, 122),

('Alien', 1979, 'Ridley Scott', 'Horror', 'The crew of the commercial spaceship Nostromo is awakened to investigate a distress signal on a remote planetoid. They encounter a deadly alien organism that begins hunting them one by one through the ship''s corridors. Ripley must outwit the perfect killing machine to survive.', 8.5, 117),

-- Comedy
('The Grand Budapest Hotel', 2014, 'Wes Anderson', 'Comedy', 'The adventures of legendary concierge Gustave H. and his loyal lobby boy Zero Moustafa at a famous European hotel between the wars. When Gustave is framed for murder, the two embark on a wild chase involving a priceless painting, a family fortune, and the changing tides of history.', 8.1, 99),

('Groundhog Day', 1993, 'Harold Ramis', 'Comedy', 'Cynical TV weatherman Phil Connors finds himself reliving the same day over and over while covering the annual Groundhog Day event in Punxsutawney. Through countless repetitions, he transforms from selfish narcissist to a genuinely good person, discovering what makes life truly worth living.', 8.0, 101),

('The Big Lebowski', 1998, 'Coen Brothers', 'Comedy', 'Laid-back slacker Jeff "The Dude" Lebowski is mistaken for a millionaire of the same name and gets drawn into a kidnapping scheme involving nihilists, a pornographer, and a severed toe. His bowling buddies Walter and Donny help him navigate the absurdist mystery while he just wants his rug back.', 8.1, 117),

('Parasite', 2019, 'Bong Joon-ho', 'Comedy', 'The impoverished Kim family cons their way into jobs with the wealthy Parks, leading to an unexpected parasitic relationship. When the Kims'' scheme intersects with another household''s dark secret, class tensions explode into shocking violence in this genre-defying dark comedy.', 8.5, 132),

('In Bruges', 2008, 'Martin McDonagh', 'Comedy', 'After a job gone wrong, hitmen Ray and Ken are sent to hide out in the medieval Belgian city of Bruges. While Ken appreciates the historical charm, Ray hates every minute. Their forced vacation takes dark turns as guilt, romance, and their boss''s orders collide.', 7.9, 107),

-- Action & Adventure
('Mad Max: Fury Road', 2015, 'George Miller', 'Action', 'In a post-apocalyptic wasteland, Max Rockatansky joins forces with Imperator Furiosa, who is smuggling five wives away from tyrannical warlord Immortan Joe. The ensuing high-speed chase across the desert becomes an explosive symphony of practical effects and feminist rebellion.', 8.1, 120),

('Raiders of the Lost Ark', 1981, 'Steven Spielberg', 'Action', 'Archaeologist Indiana Jones races against Nazis to find the Ark of the Covenant before Hitler can harness its legendary power. From the jungles of South America to the deserts of Egypt, Indy faces deadly traps, snakes, and his own past while seeking one of history''s greatest treasures.', 8.4, 115),

('The Lord of the Rings: The Fellowship of the Ring', 2001, 'Peter Jackson', 'Fantasy', 'Young hobbit Frodo Baggins inherits a powerful ring and must journey across Middle-earth to destroy it in the fires of Mount Doom. Joined by a fellowship of hobbits, elves, dwarves, and men, he faces the forces of the Dark Lord Sauron in this epic beginning to an unforgettable trilogy.', 8.8, 178),

('Inception', 2010, 'Christopher Nolan', 'Action', 'Dom Cobb is a thief who extracts secrets from people''s dreams. Offered a chance to have his criminal record erased, he must perform inception: planting an idea in someone''s mind. The team descends through multiple dream layers, each with its own time dilation, in a mind-bending heist.', 8.8, 148),

('Kill Bill: Volume 1', 2003, 'Quentin Tarantino', 'Action', 'After awakening from a four-year coma, former assassin "The Bride" seeks revenge on her ex-colleagues who betrayed her, particularly Bill, who left her for dead on her wedding day. Her bloody path of vengeance takes her from Texas to Tokyo in this stylish homage to martial arts cinema.', 8.2, 111),

('John Wick', 2014, 'Chad Stahelski', 'Action', 'Retired hitman John Wick returns to the criminal underworld after Russian gangsters kill the puppy left to him by his dying wife. What starts as a simple revenge story unfolds into an elaborate world of assassins, rules, and consequences as John carves through anyone in his path.', 7.4, 101),

-- Romance
('Eternal Sunshine of the Spotless Mind', 2004, 'Michel Gondry', 'Romance', 'After a painful breakup, Joel discovers his ex-girlfriend Clementine has undergone a procedure to erase him from her memory. He decides to do the same, but as his memories disappear, he realizes he wants to hold onto their love. A surreal journey through consciousness and the persistence of emotion.', 8.3, 108),

('Before Sunrise', 1995, 'Richard Linklater', 'Romance', 'American tourist Jesse and French student Celine meet on a train and spend one night walking through Vienna, sharing their thoughts, fears, and dreams. Their connection is instant and profound as they explore philosophy, love, and the magic of human connection before dawn separates them.', 8.1, 101),

('La La Land', 2016, 'Damien Chazelle', 'Romance', 'Aspiring actress Mia and jazz pianist Sebastian fall in love while pursuing their dreams in Los Angeles. As their careers begin to take off, they must face whether their ambitions can coexist with their relationship in this modern musical celebrating dreamers and the bittersweet nature of success.', 8.0, 128),

('Casablanca', 1942, 'Michael Curtiz', 'Romance', 'American expatriate Rick runs a nightclub in Casablanca during World War II. When his former lover Ilsa arrives with her Resistance leader husband seeking transit papers, Rick must choose between his love for her and the cause of freedom. "Here''s looking at you, kid."', 8.5, 102),

-- Mystery
('Memento', 2000, 'Christopher Nolan', 'Mystery', 'Leonard Shelby suffers from short-term memory loss and uses tattoos and notes to hunt for his wife''s killer. The story unfolds in reverse chronological order, placing the viewer in Leonard''s fragmented perspective as the truth about his condition and past reveals itself in shocking ways.', 8.4, 113),

('Knives Out', 2019, 'Rian Johnson', 'Mystery', 'When wealthy crime novelist Harlan Thrombey is found dead after his 85th birthday, detective Benoit Blanc investigates his dysfunctional family. Each member has motive, and the truth emerges through clever twists that subvert classic whodunit expectations while celebrating the genre.', 7.9, 130),

('Chinatown', 1974, 'Roman Polanski', 'Mystery', 'Private detective Jake Gittes investigates a routine adultery case that spirals into a web of corruption involving Los Angeles water rights and dark family secrets. The deeper he digs, the more danger he faces, leading to one of cinema''s most devastating conclusions.', 8.2, 130),

('Shutter Island', 2010, 'Martin Scorsese', 'Mystery', 'U.S. Marshal Teddy Daniels investigates the disappearance of a patient from a psychiatric facility on a remote island. As a hurricane traps him there, he uncovers disturbing secrets about the institution and himself, questioning what''s real in this psychological thriller about trauma and identity.', 8.2, 138);

-- Insert some reviews for variety
INSERT INTO rag_reviews (movie_id, reviewer_name, review_text, rating, review_date) VALUES

-- Blade Runner reviews
(1, 'CinematicDreamer', 'A visual masterpiece that defined the cyberpunk genre. The rain-soaked streets and neon lights create an unforgettable atmosphere. Roy Batty''s final monologue is poetry in motion.', 9.0, '2023-01-15'),
(1, 'FilmNoir_Fan', 'Ridley Scott combines film noir sensibilities with science fiction brilliance. The questions about what makes us human remain as relevant today as ever. Essential viewing.', 8.5, '2023-02-20'),

-- The Matrix reviews
(3, 'ActionJunkie99', 'Revolutionary special effects and a mind-bending story. The bullet-time sequences changed action cinema forever. Keanu Reeves found his perfect role.', 9.0, '2023-03-10'),
(3, 'PhilosophyBuff', 'Beyond the action lies a deep philosophical exploration of reality, free will, and the nature of existence. The Wachowskis created a modern myth for the digital age.', 8.5, '2023-04-05'),

-- The Shawshank Redemption reviews
(9, 'MovieClassicist', 'The greatest prison movie ever made. Tim Robbins and Morgan Freeman have incredible chemistry. The ending is absolutely perfect - hope really is a good thing.', 10.0, '2023-01-20'),
(9, 'DramaLover', 'Stephen King adaptation that transcends the genre. Every scene serves the story, building to a cathartic finale that earns every emotional beat.', 9.5, '2023-02-14'),

-- Interstellar reviews
(4, 'SpaceExplorer', 'Nolan creates a beautiful meditation on love, time, and sacrifice. The docking scene is one of the most intense sequences ever filmed. Hans Zimmer''s score is transcendent.', 9.0, '2023-03-25'),
(4, 'ScienceFiction_Expert', 'Hard science fiction that doesn''t sacrifice emotion for accuracy. The black hole visualization is groundbreaking. A film that makes you feel small and significant simultaneously.', 8.5, '2023-04-30'),

-- Spirited Away reviews
(27, 'AnimeAppreciator', 'Miyazaki''s imagination knows no bounds. Every frame could hang in a museum. The bathhouse sequence is a triumph of world-building and character development.', 9.5, '2023-05-12'),
(27, 'FamilyFilmFan', 'Perfect for all ages but never talks down to children. Chihiro''s journey from frightened child to courageous hero is inspiring. Studio Ghibli at its absolute best.', 9.0, '2023-06-18'),

-- Parasite reviews
(39, 'KoreanCinemaFan', 'Bong Joon-ho crafts a genre-defying masterpiece. The social commentary is sharp, the tension unbearable, and the ending will haunt you. Deserved every Oscar.', 9.0, '2023-07-22'),
(39, 'IndieFilmBuff', 'A perfect script where every detail matters. The architectural metaphors are brilliant. Each family represents a class with devastating precision.', 9.5, '2023-08-15'),

-- Get Out reviews
(33, 'HorrorEnthusiast', 'Jordan Peele reinvented horror for a new generation. The social commentary is razor-sharp but never overshadows the genuine scares. The sunken place is iconic.', 8.5, '2023-09-10'),
(33, 'SocialCommentary', 'More than horror - it''s a cultural landmark. Peele exposes uncomfortable truths about liberal racism with dark humor and mounting dread. Genuinely important cinema.', 8.0, '2023-10-05'),

-- Inception reviews
(44, 'MindBender', 'Nolan creates a heist movie inside the architecture of dreams. The rotating hallway fight is breathtaking. The ending is the perfect ambiguity.', 9.0, '2023-11-12'),
(44, 'BlockbusterFan', 'Proves that blockbusters can be intelligent. Each dream layer adds complexity without losing the audience. Hans Zimmer''s BRRRAAAM changed movie trailers forever.', 8.5, '2023-12-01'),

-- Eternal Sunshine reviews
(47, 'RomanceCritic', 'The most honest portrayal of love and loss ever filmed. Carrey and Winslet are perfect together. The crumbling memories are heartbreaking.', 9.0, '2023-01-30'),
(47, 'SurrealCinema', 'Charlie Kaufman''s script is a labyrinth of emotion. The visual representation of memory decay is inspired. Gondry brings poetry to the impossible.', 8.5, '2023-02-28'),

-- The Dark Knight reviews
(16, 'ComicBookFan', 'Heath Ledger''s Joker is the greatest villain performance in cinema history. Nolan elevated superhero films to art. "Why so serious?" indeed.', 9.5, '2023-03-15'),
(16, 'ThrillerAddict', 'A crime epic that happens to feature Batman. The ferry dilemma is a masterclass in tension. Gotham feels lived-in and dangerous.', 9.0, '2023-04-20');
