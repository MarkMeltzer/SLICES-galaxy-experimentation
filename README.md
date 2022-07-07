# Galaxy for SLICES experimentation
This is a copy of the [galaxy project repo](https://github.com/galaxyproject/galaxy) that is used for some experimentation for the [SLICES design study](https://slices-ds.eu/). It includes some experimental tools as well as some experimental workflows.

# How to install
### Install the instance
1. Clone this repo
3. run `run.sh` to install all dependencies and run the instance locally.

### Get admin rights
1. Register account through the web interface.
2. Edit `admin_users` in `/config/galaxy.yml` to the email of your galaxy account to get access to the admin panel. Restart the instance (see below).

### Install tool dependencies
Some tools require their own dependencies. These can be installed via the web-interface by going to the Admin panel --> manage dependencies, selecting the missing dependencies and pressing install.

### Loading the workflows
Some (partially working) example workflows are provided in the `workflows` folder. To import them go to the workflows folder click import and select the .ga files. 

# Starting/stopping the instance
To **start** the instance simply run `./run.sh` again.
To **stop** the instance stop the running script AND run `./run.sh stop` to stop the service as well.

