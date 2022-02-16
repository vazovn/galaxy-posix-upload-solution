
# Lifeportal on FOX

# Some custom requirements

## Setup of `systemd` as a **galaxy** user

- all changes are in the branch *user-systemd*
- all patches are in the directory `user-systemd-patches`

## log4s issue and socks solution

To run the ansible paybook from your local machine on *galaxy01.educloud.no* :

- open a terminal and type:

	ssh -D 12354 fox.educloud.no

- type One-Time Code and your password
- leave the terminal open and use another terminal
- modify the main playbook file *galaxy-educloud.yml* file - add the proxy variable under `-hosts`

	  environment:
			http_proxy: socks5://127.0.0.1:12354
			https_proxy: socks5://127.0.0.1:12354
    
 - patch the file 

		/patches/virtenv_pythonpath.patch

    to

		/roles/galaxyproject.galaxy/tasks/virtualenv.yml

    The goal of this patch is to use system-wide installed socks package. Socks is needed to fetch the galaxy code 
    from other sources but is not available in the galaxy's venv. To avoid the catch 22 we append the system-wide pythonpath 


## OpenIdc 

Place the backend (*.py file*) here:

		/galaxy/srv/galaxy/venv/lib/python3.6/site-packages/social_core/backends

The necessary changes to the authnz files (the files managing the authentication procedure) :

		/galaxy/srv/galaxy/server/lib/galaxy/authnz : psa_authnz.py
		/galaxy/srv/galaxy/server/lib/galaxy/authnz: managers.py
		
are made in the role *lifeportal.customized* in *tasks/main.yml*. These changes add the icons of the endpoints and add backends and backends names
