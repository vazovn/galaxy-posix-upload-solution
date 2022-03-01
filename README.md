
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


## Slurm (for submit host)

- copy all the _fox-slurm_ rpms from `/cluster/staff/slurm/20.11.8/`
- install them : `yum localinstall fox-slurm-*`
- copy
		all the `*.conf` files from  `/etc/slurm` in any fox login host
		edit the value of  ControlMachine` in the file `/etc/slurm/slurm.conf` like this : `ControlMachine=los.fox.ad.fp.educloud.no`
- install munge with yum
- copy the `munge.key` file from any fox login node to `/etc/munge/` 
- add _slurm_ user to `/etc/passwd` - copy the line from any fox login node
- copy the controll machine ip to `/etc/hosts` - los

		10.110.0.2	los los.fox
		10.111.0.2	los-mgmt los-mgmt.fox
		10.112.0.2	los-ib los-ib.fox


