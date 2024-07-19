Manga Update Script

My idea with this program was to get the latest updates from all my favourite mangas that may or may not update weekly, 
instead of checking each website manually this program will automatically go to the stored mangas and search if there 
have been any updates since the last time you checked.

Right now the implementation is pretty static, there is only support for 2 websites but I plan to add more. 

The program works by making a HTTP request to the url page of the manga from there it will search for the HTML ID and get
the contents of the chapter list. From their it will compare it against the already stored JSON and check if the HTTP 
request differs.
