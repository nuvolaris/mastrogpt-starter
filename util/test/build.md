task clean

task build:zip A=examples/withreqsjs
task build:zip A=examples/withreqsjs
echo " ">>packages/examples/withreqsjs/package.json
task build:zip A=examples/withreqsjs
task build:zip A=examples/withreqsjs

task build:zip A=examples/withreqspy
task build:zip A=examples/withreqspy
echo " ">>packages/examples/withreqspy/requirements.txt
task build:zip A=examples/withreqspy
task build:zip A=examples/withreqspy


task build:action A=examples/multifilejs
task build:action A=examples/multifilejs
echo " ">>packages/examples/multifilejs/hello.js
task build:action A=examples/multifilejs
task build:action A=examples/multifilejs

task build:action A=examples/multifilepy
task build:action A=examples/multifilepy
echo " ">>packages/examples/multifilepy/hello.py
task build:action A=examples/multifilepy
task build:action A=examples/multifilepy


task build:action A=examples/withreqsjs
task build:action A=examples/withreqsjs
echo " ">>packages/examples/withreqsjs/main.js
task build:action A=examples/withreqsjs
task build:action A=examples/withreqsjs
echo " ">>packages/examples/withreqsjs/package.json
task build:action A=examples/withreqsjs
task build:action A=examples/withreqsjs


task build:action A=examples/withreqspy
task build:action A=examples/withreqspy
echo " ">>packages/examples/withreqspy/__main__.py
task build:action A=examples/withreqspy
task build:action A=examples/withreqspy
echo " ">>packages/examples/withreqspy/requirements.txt
task build:action A=examples/withreqspy
task build:action A=examples/withreqspy





