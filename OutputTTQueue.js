var jsonObj = [];
for(var file in turntable.playlist.songsByFid){
	var item=turntable.playlist.songsByFid[file].metadata;
	jsonObj.push({song:item.song,album:item.album, artist:item.artist})
}
var buffer = "";

for (var i = 0; i < jsonObj.length; i++){
    var artist = jsonObj[i].artist == "" ? "undefined" : jsonObj[i].artist;
    var song = jsonObj[i].song == "" ? "undefined" : jsonObj[i].song;
    var album = jsonObj[i].album == "" ? "undefined" : jsonObj[i].album;
    buffer += artist + "|" + song + "|" + album + "\n";
}