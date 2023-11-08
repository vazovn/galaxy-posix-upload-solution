
# Galaxy on FOX

## PostgreSQL backup disable

Comment the backup of he DB in  `galaxyproject.postgresql/tasks/main.yml`

			#- include_tasks: backup.yml
			#  when: postgresql_backup_dir is defined


## OpenIdc 

Place the backend (*.py file*) here:

		/galaxy/srv/galaxy/venv/lib/python3.6/site-packages/social_core/backends

The necessary changes to the authnz files (the files managing the authentication procedure) :

		/galaxy/srv/galaxy/server/lib/galaxy/authnz : psa_authnz.py
		/galaxy/srv/galaxy/server/lib/galaxy/authnz: managers.py
		
are made in the role *lifeportal.customized* in *tasks/main.yml*. These changes add the icons of the endpoints and add backends and backends names


## Slurm (for submit host)

- copy all the _fox-slurm_ rpms from `/cluster/staff/slurm/20.11.8 or latest/`
- install them : `yum localinstall fox-slurm-*`
- copy all the `*.conf` files from  `/var/spool/slurmd/conf-cache` from any fox login host to `/etc/slurm/` on the galaxy server
- edit the value of `ControlMachine` in the file `/etc/slurm/slurm.conf` like this : `ControlMachine=los.fox.ad.fp.educloud.no`
- install munge with yum
- copy the `munge.key` file from any fox login node to `/etc/munge/` 
- add _slurm_ user to `/etc/passwd` - copy the line from any fox login node
- copy the controll machine ip to `/etc/hosts` - los

		10.110.0.2	los los.fox
		10.111.0.2	los-mgmt los-mgmt.fox
		10.112.0.2	los-ib los-ib.fox

- comment the line in


## Mounting of directories

- The directory `/galaxy` is a mounted directory from ESS
		aspasia.ad.fp.educloud.no:/fp/fox01/galaxy  /galaxy    nfs rw,bg,hard,intr,tcp,nfsvers=3
- The directory `/cluster`is a mounted directory from FOX
		aspasia.ad.fp.educloud.no:/fp/fox01  /cluster    nfs ro,bg,hard,intr,tcp,nfsvers=3
		
		
# Real user setup
(https://docs.galaxyproject.org/en/master/admin/cluster.html?highlight=drmaa_external_killer#submitting-jobs-as-the-real-user)

## Copy the python scripts which _ec-galaxy_ runs as root

		external_chown_script.py
		drmaa_external_runner.py
		drmaa_external_killer.py

to

		{{ galaxy_server_dir}}/scripts/

## Edit the file _ec-galaxy_

Manually create the file 'ec-galaxy' with the following content and put into /etc/sudoers.d/.
The file will be inluded by the includedir statement in sudoers file

	```
	Defaults:ec-galaxy    !requiretty
	ec-galaxy  ALL = (root) NOPASSWD: SETENV:  /cluster/galaxy-data-prod/scripts/drmaa_external_runner.py
	ec-galaxy  ALL = (root) NOPASSWD: SETENV:  /cluster/galaxy-data-prod/scripts/drmaa_external_killer.py
	ec-galaxy  ALL = (root) NOPASSWD: SETENV:  /cluster/galaxy-data-prod/scripts/external_chown_script.py
	ec-galaxy  ALL = (root) NOPASSWD: SETENV:  /cluster/galaxy-data-prod/scripts/list_cluster_directories.py
	ec-galaxy  ALL = (root) NOPASSWD: SETENV:  /usr/bin/ls
	```


## Edit the file

	group_vars/galaxy01_educloud.yml

1. add block (inside `galaxy_config.galaxy`)

	```
	#-- Run jobs as real user setup ----------------------------------------
    outputs_to_working_directory: true
    real_system_username: username
    drmaa_external_runjob_script: "sudo -E DRMAA_LIBRARY_PATH=/drmaa/lib/libdrmaa.so.1   {{ galaxy_scripts_dir }}/drmaa_external_runner.py --assign_all_groups"
    drmaa_external_killjob_script: "sudo -E DRMAA_LIBRARY_PATH=/drmaa/lib/libdrmaa.so.1   {{ galaxy_scripts_dir }}/drmaa_external_killer.py -- assign_all_groups"
    external_chown_script: "sudo -E DRMAA_LIBRARY_PATH=/drmaa/lib/libdrmaa.so.1   {{ galaxy_scripts_dir }}/external_chown_script.py --assign_all_groups"
    ```

2. add the paths to the files

	```
	# Paths to real user setup files
	galaxy_scripts_dir: "{{ galaxy_server_dir }}/scripts"
	galaxy_scripts_src_dir: files/galaxy/scripts
	```

3. define the files to be copied

	```
	#-- REAL USER setup files ----------------------------------------
	# in lifeportal_customized.galaxy/tasks/main.yml?
	galaxy_scripts_files:
		- src: "{{ galaxy_scripts_src_dir}}/drmaa_external_killer.py"
		  dest: "{{ galaxy_scripts_dir }}/drmaa_external_killer.py"
		- src: "{{ galaxy_scripts_src_dir }}/drmaa_external_runner.py"
		  dest: "{{ galaxy_scripts_dir }}/drmaa_external_runner.py"
		- src: "{{ galaxy_scripts_src_dir }}/external_chown_script.py"
		  dest: "{{ galaxy_scripts_dir }}/external_chown_script.py"
	```

## Manage the task copying the file

1. Add the task to main

	```
	## Task copying the scripts for the real user setup
	- name: Include copy chown customized scripts
	  include_tasks: copy_chown_customized_scripts.yml
      when: galaxy_manage_static_setup
	  tags: galaxy_manage_static_setup
	```

2. Create (copy) the file _copy_chown_customized_scripts.yml_

	This task copies the scripts defined in {{ galaxy_scripts_files }} here above and creates the necessary directories with the appropriate permissions and ownership

	```
	---

	# Create "slurm", "compiled_templates" and "tmp" directories (when "job_working_directory" and "files" directories are created, these three are usually not by the galaxy role)
	# Copy scripts for real user job submission which change ownership of job working dir to real user (ran by sudo)

	- name: Create the directory scripts for real user support if it does not exist
  	  ansible.builtin.file:
    	     path: /cluster/galaxy-data-prod/scripts
    	     state: directory
    	     mode: '0730'
    	     group: "{{ galaxy_group_id }}"

	- name: Install modified scripts for real user job submission
  	  copy:
	      src: "{{ item.src }}"
	      dest: "{{ item.dest }}"
	  with_items: "{{ galaxy_scripts_files }}"


	# SLURM DIR
	- name: Check directory slurm
  	  stat: path=/cluster/galaxy-data-prod/slurm
  	  register: directory_slurm

	- debug: var=directory_slurm.stat.path

	- name: Create slurm directory if it doesn't already exist
  	  ansible.builtin.file:
    	      path: /cluster/galaxy-data-prod/slurm
    	      state: directory
    	      mode: '0730'
    	      group: "{{ galaxy_group_id }}"
  	  when: not directory_slurm.stat.exists

	# TMP DIR
	- name: Check directory tmp
  	  stat: path=/cluster/galaxy-data-prod/tmp
  	  register: directory_tmp

	- debug: var=directory_tmp.stat.path

	- name: Create tmp directory if it doesn't already exist
  	  ansible.builtin.file:
    	     path: /cluster/galaxy-data-prod/tmp
    	     state: directory
    	     mode: '0730'
    	     group: "{{ galaxy_group_id }}"
  	  when: not directory_tmp.stat.exists

	# COMPILED TEMPLATES DIR
	- name: Check directory compiled_templates
  	  stat: path=/cluster/galaxy-data-prod/compiled_templates
  	  register: directory_compiled_templates

	- debug: var=directory_compiled_templates.stat.path

	- name: Create compiled_templates directory if it doesn't already exist
  	  ansible.builtin.file:
    	    path: /cluster/galaxy-data-prod/compiled_templates
    	    state: directory
    	    mode: '0730'
    	    group: "{{ galaxy_group_id }}"
  	  when: not directory_compiled_templates.stat.exists

	```

## Edit the main playbook file - add post-tasks
```
  post_tasks:

    - name: Change data folder ownership
      become: true
      become_user: root
      command: "{{ item }} chdir=/cluster/galaxy-data-prod"
      with_items:
      - chown -R ec-galaxy:ec01-galaxy-group compiled_templates
      - chown -R ec-galaxy:ec01-galaxy-group files
      - chown -R ec-galaxy:ec01-galaxy-group jobs_directory
      - chown -R ec-galaxy:ec01-galaxy-group tmp
      - chown -R ec-galaxy:ec01-galaxy-group tools
      - chown ec-galaxy:ec01-galaxy-group scripts
      changed_when: false

    - name: Change data folder mode
      become: true
      become_user: root
      command: "{{ item }} chdir=/cluster/galaxy-data-prod"
      with_items:
      - chmod -R 750 compiled_templates
      - chmod -R 730 files
      - chmod -R 730 jobs_directory
      - chmod -R 777 tmp
      - chmod -R g+s tmp
      - chmod -R 750 tools
      - chmod -R 500 scripts
      changed_when: false

    - name: Change ownership to scripts folder
      become: true
      become_user: root
      command: "{{ item }} chdir=/cluster/galaxy-data-prod/scripts/"
      with_items:
      - chown root:ec01-galaxy-group drmaa_external_runner.py
      - chown root:ec01-galaxy-group drmaa_external_killer.py
      - chown root:ec01-galaxy-group external_chown_script.py
      changed_when: false

    - name: Set 500 to the permission escalating scripts used for real user setup
      become: true
      become_user: root
      command: "{{ item }} chdir=/cluster/galaxy-data-prod/scripts/"
      with_items:
      - chmod 500 drmaa_external_runner.py
      - chmod 500 drmaa_external_killer.py
      - chmod 500 external_chown_script.py
      changed_when: false
```


## Monitoring and reports

The program _gxadmin_ allows the admin (as _galaxy_ user) to query the framework for various parameteres. It is installed as a separate role `galaxyproject.gxadmin` which is set in the `requirements.yml`. To use it set the PGDATABASE variable in `.bashrc`for _galaxy_ user.

		export PGDATABASE=galaxy
		
Then run the commands like

		gxadmin query latest-users
		gxadmin query job-info
		
etc.

For more info see: *https://training.galaxyproject.org/training-material/topics/admin/tutorials/gxadmin/tutorial.html*


## Mounts

Partitions and access:

	| ess-fp-proto01 /fp/fox01 # ls -ld galaxy*
	| drwxr-s---  2 ec-galaxy ec01-galaxy-group 4096 Nov  2 10:23 galaxy
	| drwxrws--x  2 ec-galaxy ec01-galaxy-group 4096 Nov  2 10:28 galaxy-data-prod
	| drwxrws--x 10 ec-galaxy ec01-galaxy-group 4096 Nov  2 10:21 galaxy-data-test
	| drwxr-x---  3 ec-galaxy ec01-galaxy-group 4096 Sep  7 15:01 galaxy-test

Exports : RO/RW and (NO_)ROOT_SQUASH:

	| Path                            Clients                        Access_Type  Protocols  Transports  Squash          SecType
	| ------------------------------  -----------------------------  -----------  ---------  ----------  --------------  -------
	| /fp/fox01/galaxy                galaxy01.educloud.no           RW           3          TCP         ROOT_SQUASH     SYS
	| /fp/fox01/galaxy-data-prod      galaxy01.educloud.no           RW           3          TCP         NO_ROOT_SQUASH  SYS
	| /fp/fox01/galaxy-data-test      galaxy01-test.educloud.no      RW           3          TCP         NO_ROOT_SQUASH  SYS
	| /fp/fox01/galaxy-test           galaxy01-test.educloud.no      RW           3          TCP         ROOT_SQUASH     SYS
	| /fp/homes01                     galaxy01-test.educloud.no      RO           3          TCP         ROOT_SQUASH     SYS
	| /fp/homes01                     galaxy01.educloud.no           RO           3          TCP         ROOT_SQUASH     SYS
	| /fp/projects01                  galaxy01-test.educloud.no      RO           3          TCP         ROOT_SQUASH     SYS
	| /fp/projects01                  galaxy01.educloud.no           RO           3          TCP         ROOT_SQUASH     SYS
