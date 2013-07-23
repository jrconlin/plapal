CREATE TABLE if not exists description (id string primary key, artist string, title string, album string, genre number, rating integer default 0);
CREATE TABLE if not exists files (id string primary key, path string, host string);
CREATE TABLE if not exists playlists (name string, id string)
