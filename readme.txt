######  README Applications Server   ######
######        Version : 1.0          ######
######  Created by Alexandre Fourgs  ######

######          ! WARNING !          ######
###### This server can only work on  ######
######       a Linux machine         ######


######        How to get it          ######
https://github.com/AlexFourgs/Actility


######       How to install it       ######
This project uses some API and external libraries. You must install them if you want it works fine.

1/ With pip
After downloading the source.
Open a terminal and go into the folder Actility/Documentations.
Then, enter "pip install -r requirements.txt" in your terminal and all libraries will be installed.

2/ With script shell
After downloading the source.
Open a terminal and go into the folder Actility/Documentations.
Then, enter "sh install.sh" or "bash install.sh" in your terminal and all libraries will be installed.

3/ By your own way.
If you want to install specific versions or for other reasons you can install them by your own way.
Three external libraries are used in this project :
- Bottlepy (http://bottlepy.org/)
- lxml (http://lxml.de/)
- SQLite3 (https://www.sqlite.org/) (Installed on Linux machine)

If you choose the third way, the creator of this project isn't responsible of the eventual bug that you will have.


######        How to use it         ######

After installing every libraries, in a terminal, go into the folder Actility/Programs and enter "python application_server.py".
Your server will start.
