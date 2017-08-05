1. Place this directory somewhere on your harddrive
2. Get the path file of this directory
3. Add the path to the PATH variable in windows
	a. go to control panel > system > advanced system settings > environment variables... 
	b. Edit the PATH variable
	c. Add ;path-of-this-directory  to the end of the variables.

4. Go to kicad, open an eeschema
5. Click on BOM
6. Click on Add Plugin
7. Select one of the xsl files in this directory
8. you now added a plugin, check if it says: "xsltproc -o "%O.csv" "C: .... etc"
	With me it did not say "%O.csv" but just "%O" change it if needed.

9. Click on generate, the .csv will be placed in your project folder.


::::::::::::  xsltproc -o "%O.csv" "I:\GitHub\KicadBOM\bom2groupedCsv.xsl" "%I"
bom2groupedCsv1