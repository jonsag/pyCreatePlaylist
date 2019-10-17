# pyCreatePlaylist
Python script to create playlists from audio and/or video

The script scans a directory, optionally recursive, searching for videos, and/or audio files. You can also state what file extensions you like to scan for.

All valid files are put into a playlist with choosable name, extension and location. Paths can be set to absolute or relative.

Usage:
pyCreatePlaylist <options>
----------------------------------------
    -o, --out <argument>
        Outfile. Either an existing or new directory, and/or a filename
        If you do not give a directory, it will be '<current directory>'
        If you do not give a filename, it will be 'playlist.m3u'
        If you do not give a file extension, .'m3u' will be added
        (changes can be made in configuration file 'config.ini')
    -i, --indir <argument>
        Input directory that will be scanned
        If you do not give a directory, '<current directory>' will be searched
    -e, --extension <argument>
        Comma separated list of extensions that will be searched for
    -m, --movies
        Video extensions will be searched for
        (changes can be made in configuration file 'config.ini')
    -s, --sound
        Audio extensions will be searched for
        (changes can be made in configuration file 'config.ini')
    -r, --recursive
        Serch will be recursive
    -a, --absolute
        Playlist will contain absolute paths
    -v, --verbose
        Verbose output
    -h, --help
        Prints this
