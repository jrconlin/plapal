/*
 * This is a hack-tastic console script that will scan the Google Music playlist
 * page (e.g. "Highly Rated") and print out the list of songs on it.
 */
songs = document.getElementsByClassName("song-row")
buffer = ""
for (i=0;i<songs.length;i++) {
        song = songs[i];
            console.debug(song);
                title = song.querySelector('[data-col="title"]').textContent;
                    album = song.querySelector('[data-col="album"]').textContent;
                        artist = song.querySelector('[data-col="artist"]').textContent;
                            buffer += artist + "|" + title + "|" + album + "\n";
}
console.debug(buffer)

