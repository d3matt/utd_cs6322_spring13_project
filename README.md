utd_cs6322_spring13_project
===========================

team project for CS6322 - ACL citation analysis

Setup
-----
 1. run ./bootstrap - this initializes the python environment for your unix machine.  This environment is fully self-contained in the .pyenv folder thanks to virtualenv
 2. ./index/manage runserver - launches webserver.  it will tell you the IP:PORT to point your web browser


Re-creating Index
-----------------
 1. cd crawl
 2. ./crawl.sh #this crawls the aclweb site
 3. make -j <# of processors to use> -k  #ignore any errors...  the pre-processor isn't perfect
 4. cd ../index
 5. ./pre-index #this took over 40 hours to load up the sql.  There's a memory leak so the process needs to be restart multiple times
