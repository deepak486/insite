## AUAV inSite&trade;


#### Build and Install Quickstart:
- for these instructions [APP_DIR] refers to your local location, i.e /your_computer/some_path/inSite
- install git (from https://git-scm.com)
- install node.js (from https://nodejs.org)
- open a command prompt (for windows) or terminal (for linux) and change your current directory to where you want to store your local inSite code repository.
- run 'git clone https://github.com/AustralianUAV/inSite.git' to clone the repository. Your local 'inSite' folder is referred to below as [APP_DIR]
- change current directory to '[APP_DIR]'
- run 'git submodule update --init --recursive' to pull in the sub-modules (check files under '[APP_DIR]/modules/cesium' and '[APP_DIR]/modules/bootstrap') [help link for loading the sub modules: https://stackoverflow.com/questions/10168449/git-update-submodule-recursive]
- change current directory to '[APP_DIR]/modules/bootstrap' folder, run 'npm install'. Confirm no errors.
- change current directory to '[APP_DIR]/modules/cesium' folder, run 'npm install' and then run 'npm run release', confirm no errors, after which you should have 'cesium/Build/Cesium/Cesium.js'. 
- Create a symlink 'ln -s [APP_DIR]/modules/cesium/node_modules [APP_DIR]/node_modules' in Linux/OSX or 'mklink /D node_modules inSite\modules\cesium\node_modules' in Windows (annoying workaround, can't configure node.js to find these elsewhere)
- change current directory to [APP_DIR], and run 'node server.js --public' in command prompt
- you should get a message about a local server running, and then be able to connect with a web browser to http://localhost:8080/
- that will allow you to run the web app, you should see the default cesium globe, but you won't have the AUAV custom content. You can add your own or copy/link in the existing dev/demo data from [DROPBOX]/INSITE/DATA to [APP_DIR]/DATA

#### Webpack integration:
- open a command prompt (for windows) or terminal (for linux)
- change your current directory to [APP_DIR]
- run `npm install webpack webpack-cli --save-dev`
- run `npm i babel-core babel-loader babel-preset-env --save-dev`
- run `npm run dev` to build in development mode
- run `npm run build` to build in production mode
- run `npm run watch` to build in development mode automatically when you make some changes in files. 

#### Instruction for future development with Webpack:
- Learn ES6 module style coding.
- If you need to make some 'Object' global: You can do the same process that has been in `[APP_DIR]/js/index.js` file.
- If you need to make some 'String' or 'Number' variable global: use ` window["your_var_name"] = 'desired value'; ` in index.js or your JS file.
- It's good practice to declare all global variable in a single location(in this case it is `[APP_DIR]/js/index.js`), as this way it's easy to track.

 **Instruction for addition of new JS file:**
	- If there is some initialization that must be done when script is loaded, then you have add a entry for your JS file under **entry/app/**.
	- If there is some variable that you want to be in global scope, then add a entry for your JS file in `[APP_DIR]/js/index.js` file.
	- If you need both of the above, then do the both process.


#### Troubleshooting:
- re-run the npm commands again and check for errors
- this is all pretty cutting edge stuff, you may need to update your version of npm, node, cesium
- check you can run node on its own on the command line
- if node seems to be running fine, but you don't get the right result in the web browser, open the javascript console and look for errors there
- if you get the default Cesium globe, and it is functional (i.e. you can rotate and zoom it) but no AUAV data (and links in the 'Naigate To' menu don't work) then you are just getting stuck on the dev/demo data being in the right place. Irrespective of Cesium and inSite, you should be able to view the .json files listed in the inSite/config/default.js file in your web browser (e.g. http://localhost:8080/DATA/AusGrid/Beacon_Hill_demo/model/Ausgrid_Cesium.json). These are just text files, if you can't load them directly in the web browser then they're not in the right place for inSite to load them either

