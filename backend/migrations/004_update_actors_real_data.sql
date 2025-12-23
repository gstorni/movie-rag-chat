-- Update movies with real actor data
-- This provides accurate cast information for the 50 movies in the database

-- Sci-Fi Classics
UPDATE rag_movies SET actors = ARRAY['Harrison Ford', 'Rutger Hauer', 'Sean Young', 'Edward James Olmos', 'Daryl Hannah'] WHERE title = 'Blade Runner';
UPDATE rag_movies SET actors = ARRAY['Keir Dullea', 'Gary Lockwood', 'William Sylvester', 'Douglas Rain'] WHERE title = '2001: A Space Odyssey';
UPDATE rag_movies SET actors = ARRAY['Keanu Reeves', 'Laurence Fishburne', 'Carrie-Anne Moss', 'Hugo Weaving', 'Joe Pantoliano'] WHERE title = 'The Matrix';
UPDATE rag_movies SET actors = ARRAY['Matthew McConaughey', 'Anne Hathaway', 'Jessica Chastain', 'Michael Caine', 'Matt Damon'] WHERE title = 'Interstellar';
UPDATE rag_movies SET actors = ARRAY['Amy Adams', 'Jeremy Renner', 'Forest Whitaker', 'Michael Stuhlbarg'] WHERE title = 'Arrival';
UPDATE rag_movies SET actors = ARRAY['Domhnall Gleeson', 'Alicia Vikander', 'Oscar Isaac', 'Sonoya Mizuno'] WHERE title = 'Ex Machina';
UPDATE rag_movies SET actors = ARRAY['Timothée Chalamet', 'Rebecca Ferguson', 'Oscar Isaac', 'Josh Brolin', 'Zendaya', 'Jason Momoa'] WHERE title = 'Dune';
UPDATE rag_movies SET actors = ARRAY['Ethan Hawke', 'Uma Thurman', 'Jude Law', 'Gore Vidal'] WHERE title = 'Gattaca';

-- Drama Masterpieces
UPDATE rag_movies SET actors = ARRAY['Tim Robbins', 'Morgan Freeman', 'Bob Gunton', 'William Sadler', 'Clancy Brown'] WHERE title = 'The Shawshank Redemption';
UPDATE rag_movies SET actors = ARRAY['Marlon Brando', 'Al Pacino', 'James Caan', 'Robert Duvall', 'Diane Keaton'] WHERE title = 'The Godfather';
UPDATE rag_movies SET actors = ARRAY['Liam Neeson', 'Ben Kingsley', 'Ralph Fiennes', 'Caroline Goodall'] WHERE title = 'Schindler''s List';
UPDATE rag_movies SET actors = ARRAY['Tom Hanks', 'Robin Wright', 'Gary Sinise', 'Sally Field', 'Mykelti Williamson'] WHERE title = 'Forrest Gump';
UPDATE rag_movies SET actors = ARRAY['Tom Hanks', 'Michael Clarke Duncan', 'David Morse', 'Bonnie Hunt', 'James Cromwell'] WHERE title = 'The Green Mile';
UPDATE rag_movies SET actors = ARRAY['Russell Crowe', 'Ed Harris', 'Jennifer Connelly', 'Christopher Plummer', 'Paul Bettany'] WHERE title = 'A Beautiful Mind';

-- Thrillers & Crime
UPDATE rag_movies SET actors = ARRAY['John Travolta', 'Samuel L. Jackson', 'Uma Thurman', 'Bruce Willis', 'Ving Rhames', 'Tim Roth'] WHERE title = 'Pulp Fiction';
UPDATE rag_movies SET actors = ARRAY['Christian Bale', 'Heath Ledger', 'Aaron Eckhart', 'Michael Caine', 'Maggie Gyllenhaal', 'Gary Oldman', 'Morgan Freeman'] WHERE title = 'The Dark Knight';
UPDATE rag_movies SET actors = ARRAY['Brad Pitt', 'Edward Norton', 'Helena Bonham Carter', 'Meat Loaf', 'Jared Leto'] WHERE title = 'Fight Club';
UPDATE rag_movies SET actors = ARRAY['Brad Pitt', 'Morgan Freeman', 'Gwyneth Paltrow', 'Kevin Spacey', 'R. Lee Ermey'] WHERE title = 'Se7en';
UPDATE rag_movies SET actors = ARRAY['Jodie Foster', 'Anthony Hopkins', 'Scott Glenn', 'Ted Levine'] WHERE title = 'The Silence of the Lambs';
UPDATE rag_movies SET actors = ARRAY['Tommy Lee Jones', 'Javier Bardem', 'Josh Brolin', 'Woody Harrelson', 'Kelly Macdonald'] WHERE title = 'No Country for Old Men';
UPDATE rag_movies SET actors = ARRAY['Jake Gyllenhaal', 'Mark Ruffalo', 'Robert Downey Jr.', 'Chloë Sevigny', 'Anthony Edwards'] WHERE title = 'Zodiac';

-- War Films
UPDATE rag_movies SET actors = ARRAY['Tom Hanks', 'Matt Damon', 'Tom Sizemore', 'Edward Burns', 'Barry Pepper', 'Vin Diesel'] WHERE title = 'Saving Private Ryan';
UPDATE rag_movies SET actors = ARRAY['Martin Sheen', 'Marlon Brando', 'Robert Duvall', 'Dennis Hopper', 'Laurence Fishburne'] WHERE title = 'Apocalypse Now';
UPDATE rag_movies SET actors = ARRAY['Matthew Modine', 'R. Lee Ermey', 'Vincent D''Onofrio', 'Adam Baldwin', 'Dorian Harewood'] WHERE title = 'Full Metal Jacket';
UPDATE rag_movies SET actors = ARRAY['Fionn Whitehead', 'Tom Glynn-Carney', 'Jack Lowden', 'Harry Styles', 'Mark Rylance', 'Kenneth Branagh', 'Tom Hardy'] WHERE title = 'Dunkirk';
UPDATE rag_movies SET actors = ARRAY['George MacKay', 'Dean-Charles Chapman', 'Mark Strong', 'Andrew Scott', 'Richard Madden', 'Colin Firth', 'Benedict Cumberbatch'] WHERE title = '1917';

-- Animation
UPDATE rag_movies SET actors = ARRAY['Daveigh Chase', 'Suzanne Pleshette', 'Miyu Irino', 'Rumi Hiiragi'] WHERE title = 'Spirited Away';
UPDATE rag_movies SET actors = ARRAY['Ben Burtt', 'Elissa Knight', 'Jeff Garlin', 'Fred Willard', 'John Ratzenberger'] WHERE title = 'WALL-E';
UPDATE rag_movies SET actors = ARRAY['Matthew Broderick', 'Jeremy Irons', 'James Earl Jones', 'Jonathan Taylor Thomas', 'Moira Kelly', 'Nathan Lane', 'Ernie Sabella'] WHERE title = 'The Lion King';
UPDATE rag_movies SET actors = ARRAY['Tom Hanks', 'Tim Allen', 'Don Rickles', 'Jim Varney', 'Wallace Shawn', 'John Ratzenberger'] WHERE title = 'Toy Story';
UPDATE rag_movies SET actors = ARRAY['Anthony Gonzalez', 'Gael García Bernal', 'Benjamin Bratt', 'Alanna Ubach', 'Renée Victor'] WHERE title = 'Coco';

-- Horror
UPDATE rag_movies SET actors = ARRAY['Jack Nicholson', 'Shelley Duvall', 'Danny Lloyd', 'Scatman Crothers'] WHERE title = 'The Shining';
UPDATE rag_movies SET actors = ARRAY['Daniel Kaluuya', 'Allison Williams', 'Catherine Keener', 'Bradley Whitford', 'Caleb Landry Jones'] WHERE title = 'Get Out';
UPDATE rag_movies SET actors = ARRAY['Toni Collette', 'Alex Wolff', 'Milly Shapiro', 'Ann Dowd', 'Gabriel Byrne'] WHERE title = 'Hereditary';
UPDATE rag_movies SET actors = ARRAY['Ellen Burstyn', 'Max von Sydow', 'Linda Blair', 'Lee J. Cobb', 'Jason Miller'] WHERE title = 'The Exorcist';
UPDATE rag_movies SET actors = ARRAY['Sigourney Weaver', 'Tom Skerritt', 'John Hurt', 'Veronica Cartwright', 'Harry Dean Stanton', 'Ian Holm'] WHERE title = 'Alien';

-- Comedy
UPDATE rag_movies SET actors = ARRAY['Ralph Fiennes', 'F. Murray Abraham', 'Mathieu Amalric', 'Adrien Brody', 'Willem Dafoe', 'Jude Law', 'Tilda Swinton'] WHERE title = 'The Grand Budapest Hotel';
UPDATE rag_movies SET actors = ARRAY['Bill Murray', 'Andie MacDowell', 'Chris Elliott', 'Stephen Tobolowsky', 'Brian Doyle-Murray'] WHERE title = 'Groundhog Day';
UPDATE rag_movies SET actors = ARRAY['Jeff Bridges', 'John Goodman', 'Julianne Moore', 'Steve Buscemi', 'Philip Seymour Hoffman', 'John Turturro'] WHERE title = 'The Big Lebowski';
UPDATE rag_movies SET actors = ARRAY['Song Kang-ho', 'Lee Sun-kyun', 'Cho Yeo-jeong', 'Choi Woo-shik', 'Park So-dam'] WHERE title = 'Parasite';
UPDATE rag_movies SET actors = ARRAY['Colin Farrell', 'Brendan Gleeson', 'Ralph Fiennes', 'Clémence Poésy'] WHERE title = 'In Bruges';

-- Action & Adventure
UPDATE rag_movies SET actors = ARRAY['Tom Hardy', 'Charlize Theron', 'Nicholas Hoult', 'Hugh Keays-Byrne', 'Rosie Huntington-Whiteley'] WHERE title = 'Mad Max: Fury Road';
UPDATE rag_movies SET actors = ARRAY['Harrison Ford', 'Karen Allen', 'Paul Freeman', 'Ronald Lacey', 'John Rhys-Davies', 'Denholm Elliott'] WHERE title = 'Raiders of the Lost Ark';
UPDATE rag_movies SET actors = ARRAY['Elijah Wood', 'Ian McKellen', 'Viggo Mortensen', 'Sean Astin', 'Orlando Bloom', 'Sean Bean', 'Cate Blanchett', 'Ian Holm'] WHERE title = 'The Lord of the Rings: The Fellowship of the Ring';
UPDATE rag_movies SET actors = ARRAY['Leonardo DiCaprio', 'Joseph Gordon-Levitt', 'Ellen Page', 'Tom Hardy', 'Ken Watanabe', 'Marion Cotillard', 'Cillian Murphy', 'Michael Caine'] WHERE title = 'Inception';
UPDATE rag_movies SET actors = ARRAY['Uma Thurman', 'Lucy Liu', 'Vivica A. Fox', 'Daryl Hannah', 'David Carradine', 'Michael Madsen'] WHERE title = 'Kill Bill: Volume 1';
UPDATE rag_movies SET actors = ARRAY['Keanu Reeves', 'Michael Nyqvist', 'Alfie Allen', 'Willem Dafoe', 'Adrianne Palicki', 'Ian McShane'] WHERE title = 'John Wick';

-- Romance
UPDATE rag_movies SET actors = ARRAY['Jim Carrey', 'Kate Winslet', 'Kirsten Dunst', 'Mark Ruffalo', 'Elijah Wood', 'Tom Wilkinson'] WHERE title = 'Eternal Sunshine of the Spotless Mind';
UPDATE rag_movies SET actors = ARRAY['Ethan Hawke', 'Julie Delpy', 'Andrea Eckert'] WHERE title = 'Before Sunrise';
UPDATE rag_movies SET actors = ARRAY['Ryan Gosling', 'Emma Stone', 'John Legend', 'Rosemarie DeWitt', 'J.K. Simmons'] WHERE title = 'La La Land';
UPDATE rag_movies SET actors = ARRAY['Humphrey Bogart', 'Ingrid Bergman', 'Paul Henreid', 'Claude Rains', 'Conrad Veidt'] WHERE title = 'Casablanca';

-- Mystery
UPDATE rag_movies SET actors = ARRAY['Guy Pearce', 'Carrie-Anne Moss', 'Joe Pantoliano', 'Mark Boone Junior'] WHERE title = 'Memento';
UPDATE rag_movies SET actors = ARRAY['Daniel Craig', 'Ana de Armas', 'Chris Evans', 'Jamie Lee Curtis', 'Toni Collette', 'Christopher Plummer', 'Michael Shannon'] WHERE title = 'Knives Out';
UPDATE rag_movies SET actors = ARRAY['Jack Nicholson', 'Faye Dunaway', 'John Huston', 'Perry Lopez', 'John Hillerman'] WHERE title = 'Chinatown';
UPDATE rag_movies SET actors = ARRAY['Leonardo DiCaprio', 'Mark Ruffalo', 'Ben Kingsley', 'Michelle Williams', 'Emily Mortimer', 'Max von Sydow'] WHERE title = 'Shutter Island';

-- Verify update
SELECT title, actors FROM rag_movies WHERE actors IS NOT NULL ORDER BY title LIMIT 5;
