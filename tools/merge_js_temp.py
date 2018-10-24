# TEMP solution to a minified build, this will merge our JS scripts, then we run through some online tools to produce the minified and uglified versions
# will replace with webpack soon
#
# Minify: https://www.minifier.org
# Obfuscate: https://javascriptobfuscator.com/Javascript-Obfuscator.aspx
#
# Run from the top level directory (i.e. python tools/merge_js_temp.py)
#

filenames = ['js/insite_data.js', 'js/inSite_userdata.js', 'js/inSite_lib.js', 'js/inSite_camera.js', 'js/insite_annotation.js', 'js/site_marker.js', 'js/cameraOrbit.js', 'js/inSite.js', 'js/areaMeasurement.js', 'js/insite_config.js', 'js/insite_UI.js']
with open('js/merged.js', 'w') as outfile:
    for fname in filenames:
        outfile.write("\n/* start of " + fname +" */\n\n")
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
        outfile.write("\n\n/* end of " + fname +" */\n")
