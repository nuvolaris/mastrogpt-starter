task clean
task undeploy

task single A=examples/simplejs.js
nuv invoke examples/simplejs

task single A=examples/multifilejs
nuv invoke examples/multifilejs


task single A=examples/withreqsjs
nuv invoke examples/withreqsjs



