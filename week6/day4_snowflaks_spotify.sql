SHOW TABLES;

SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_ROLE();

SELECT *
FROM spotify_data
LIMIT 10;

-- 1. Which is the longest song released yet?

SELECT song_title,
       ARTIST,
       DURATION_MS,
       ROUND(DURATION_MS / 60000, 2) AS DURATION_MINUTES
FROM SPOTIFY_DATA
ORDER BY DURATION_MS DESC
LIMIT 1;


-- 2. How many songs has Drake sung? 
SELECT COUNT(*) AS DRAKE_SONG_COUNT
FROM SPOTIFY_DATA
WHERE ARTIST ILIKE '%Drake%';

-- 3. List those songs with letter ‘Love’ in them. 

SELECT song_title,
       artist
FROM SPOTIFY_DATA
WHERE song_title ILIKE '%Love%';


-- 4. Select songs which have a number in them.

SELECT song_title,
       artist
FROM SPOTIFY_DATA
WHERE REGEXP_LIKE(song_title, '.*[0-9].*');

-- 5. You have a bachelorette weekend, which songs would you play the most?
SELECT
    song_title,
    artist,
    energy,
    danceability
FROM SPOTIFY_DATA
ORDER BY
    (energy + danceability) DESC
LIMIT 15;

-- 6. In a dance battle, which 3 songs would you choose for a dance off ?
SELECT
    song_title,
    artist,
    energy,
    danceability,
    acousticness,
    liveness,
FROM SPOTIFY_DATA
ORDER BY
    (energy + danceability + liveness
     - acousticness - speechiness) DESC
LIMIT 3;

-- 7. Which artist has the max songs released?

SELECT
    artist,
    COUNT(*) AS total_songs
FROM SPOTIFY_DATA
GROUP BY artist
ORDER BY total_songs DESC
LIMIT 1;

-- 8. Make a ‘break-up’ song list >..< 

SELECT
    song_title,
    artist,
    energy,
    acousticness,
    mode
FROM SPOTIFY_DATA
WHERE song_title ILIKE ANY (
    '%Heartbreak%',
    '%Goodbye%',
    '%Sorry%',
    '%Alone%',
    '%Broken%',
    '%Without You%',
    '%Miss You%',
    '%Love%'
)
AND mode = 0
ORDER BY energy ASC
limit 10;
