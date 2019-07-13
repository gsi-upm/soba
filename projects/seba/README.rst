SEBA
----

**Simulation of Evacuations based on SOBA**

Steps for the execution of the simulation service in a Docker container. 

Construction of the image (named seba), for execution in visual mode

	docker build -t seba --build-arg mode=v .

or in batch mode.

	docker build -t seba --build-arg mode=b .

execution of the service in the container (named sebarunning)

	docker run -p 7777:7777 -p 10000:10000 --name sebarunning seba

the ports to provide visualization on the browser (7777) and a REST service (10000) are defined.

**Instructions for using the precomputed routes with the AStar algorithm:**

Modify the parameter 'astar' to 'True' of the configuration and execution file 'run.py'. The calculated routes of the map will be stored in the waysAStar file.