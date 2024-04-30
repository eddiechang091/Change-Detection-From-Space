1. The general principle:

You build a Docker image that will be executed based on the file in mission_config folder (that you got from WebNOVA UI). Put your code solution  in /entry_point folder.

Following docker image folders will be bind-mounted on the host, as following:
/input_queue - this folder will get the imagery from satellite, real or virtual
/output_queue - put your results there 
/mission_config - configuration file to tell host when to execute your container.

Example docker command to run your container is given in "docker_command.txt"


2. Challenge-specific changes:
- replace user1 in Dockerfile with your own user id to identify the author.
- replace ission_config1712967621622.json in Dockerfile with your own json file you get from WebNOVA UI
- replace run_executable.shell script or executable.py with your own code.

 
P.S. You can modify the Docker image template, for example add more libraries and tools, but keep the folder structure as is.