PlaPal - The directory independent Play List manager
====

One of the downsides of having lots of devices that can play music is that
stuff can be scattered all over.

Play lists, DJ love them, all use directories to figure out where songs are.
That's fantastic and all, but kinda sucks when you want to port a playlist from
one machine to another.

This app is a work in progress to try and resolve that. It does a few things to
try and fix the problem.

1. *File names aren't honest.* 

Some systems "helpfully" change the name and path of files to be more
"efficient" (may they burn in hell). This system takes the smallest, unique
portion of a file (the first 1MB) and creates a SHA256 hash of it. That
provides a fairly good fingerprint for a given file. (See notes about that)
Added bonus, it's great at finding mislabled duplicates.

2. *Files are their own source of truth.*

Music info is pulled from the ID3 section of the MP3. Period.

3. *A portable list should be portable*

So, based on 1 & 2, a portable playlist should have only information that's
common to mp3 files. In this case, it's Artist, Title and Album separated by
"|"s. To build a local playlist, just query the matching paths. 



NOTES: 
---
1. *The hash.*  

Honestly, I should pick something other than the first MB. The problem there is
that for MP3 files, there's metadata stuffed in there that can muck with things
(e.g. Amazon uses that area to fingerprint files, so your copy of "Amsterdamn"
isn't the same as mine.) I really need to dig into the formatting of MP3 files
to figure out how to get to the first 1MB of actual audio to sample. 

2. *The DB*

currently, i'm using simpledb because that's reasonably portable.  That does
mean that if you have millions of songs, you're probably screwed. I've got only
a couple of thousand, so scanning the initial list on my desktop was fast. No
idea how it'll preform on android
