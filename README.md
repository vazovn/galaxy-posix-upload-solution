 **MASTER** is the main branch for the *galaxy-hepp* instance. 

It contains the code which integrates all the features which are **currently available** in the Galaxy instance. The instance itself is being run from another branch called *PRODUCTION* which is a mirror of *MASTER*.

In case you want to make a change or develop a new feature, please checkout a new branch from *MASTER* and make your changes there. When ready, inform the team members to create a pull request for a merge from your branch to *MASTER*. The steps are detailed below:

## Rules for branching

- pull the entire repo to you local machine
- list the branches

	```git branch -a ```

- create a new local branch from the remote branch

	```checkout -b remote_branch(full path to MASTER) MASTER```

- create your new development branch 

	```checkout MASTER; checkout -b YOUR_DEV_BRANCH```

- work on the new branch
- when ready, let everybody know - we schedule a merge via a pull request to *MASTER*


# Details on setup
https://github.uio.no/IT-ITF/fi-internal-docs/blob/master/scientific-sw-and-portals-team/servers/galaxy-hepp.hpc/index.md



# Galaxy deployment to RHEL 8/Centos 8 via Ansible playbook

   
## Prerequisites

### Slurm client

Install the slurm client before the Galaxy platform installation. Run the ansible playbook from branch 

```slurm-installation```

### Galaxy setup

#### Password for UiO LDAP

In order to configure the auth_conf.xml file a password for the UiO LDAP is needed. It is located in `/ldap/galaxy_hepp_ldap_pass` in `galaxy-hepp.hpc.uio.no`. Ansible reads the contents of this file and inserts it into the `auth_conf.xml` file during the playbok execution. Copy this file to the machine where the playbook is executed and modify the path in the main playbook file `galaxy.yml` as shown below:

```
- hosts: galaxy_hepp
  become: true
  vars:
      passwd_file_contents: "{{ lookup('file', '<PATH-TO-THE-LDAP-PASSWORD-FILE>/galaxy_hepp_ldap_pass') }}"
```

#### Galaxy itself

In the repo there are two playbooks:

- galaxy-centos-rhel8.yml

- galaxy.yml


The  former contains  the  instructions to  install prerequisites  for
Galaxy and Podman to run in  the instance, the latter the installation
of Galaxy. Run the playbooks in that order

```
$ ansible-playbook galaxy-centos-rhel8.yml
$ ansible-playbook galaxy.yml
```

The    python   interpreter    is   predifined    as   `python3`    in
`ansible.cfg`. Comment out the line with the interpreter `python3` for
the run  of `galaxy-centos-rhel8`  in order  to avoid  possible issues
with the already bundled `platform-python`

```
[defaults]
interpreter_python = /usr/bin/python3
...
...
```
## Galaxy user creation


The RHEL 8  images are `maintained` by UiO and  therefore connected to
LDAP/Cerebrum. For  this particular  deployment we  do not  create the
galaxy user in the Ansible playbook `group_vars/galaxy_hepp.yml`


## Nginx and related to Galaxy

Make sure  the ssl certificates are  ordered and ready to  deploy once
the `nginx.centos` Ansible role installs Nginx. The role also contains
a template/copy of the galaxy.conf  to be in `/etc/nginx/conf.d/` with
the ssl configuration.

An important  change to be  made in the  `group_vars/galaxy-hepp.yml` when
the  ssl  certificates  are  in  place  is  to  change  in  the  uwsgi
configuration   part    from   `http:   0.0.0.0:8080`    to   `socket:
127.0.0.1:8080`.

If ssl certificates are not in place but still want to run Galaxy keep

    the `http: 0.0.0.0:8080` line in `group_vars/galaxy-hepp.yml`:

```
server {
    listen 80;
    server_name zpath.hepp.uiocloud.no;

    location / {
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host $http_host;

	proxy_pass http://127.0.0.1:8080;
	uwsgi_param UWSGI_SCHEME $scheme;
	include uwsgi_params;	
    }

```
The http .conf files are located in 

```
/etc/nginx/working_nginx_conf
/etc/nginx/conf.d/working_http_galaxy_conf
```

 # Tool details 
 
 ## Using Galaxy requirements/dependencies in tools
https://galaxyproject.org/admin/config/tool-dependencies/

To be able to use the requirements tag in your xml job-wrapper to either enable an environment or load a specific binary: 

In the main galaxy config (```/srv/galaxy/config/galaxy.yml```)
Set the ```tool_dependency_dir```to the path where your software is stored, in a dependency dir like this

```
tool_dependency_dir: /storage/software/dependencies
```

Galaxy expects a folder structure consiting of ```<tool_dependendy_dir>/dependencies/<software>/<version>```. In each software/version folder Galaxy expects either an env.sh file, or a bin folder which contains the binary of the software. 


### Example - activate root software
In the job-wrapper, add a requirements field: 
```
<requirements>
    <requirement type="package" version="6.24.2">root</requirement>
  </requirements>
  ```

The version (6.24.2) and name (root) must match the folder-struccture, which it does here :
``` 
[root@zpath ~]# ls /storage/software/dependencies/root/6.24.2/
env.sh
```

The env.sh contains: 
```
[root@zpath ~]# cat /storage/software/dependencies/root/6.24.2/env.sh 
#!/bin/sh

if [ -z "$MODULEPATH" ] ; then
   #. /etc/profile.d/z00_lmod.sh
   #. /etc/profile.d/z01_StdEnv.sh
   . /storage/software/lmod/lmod/init/profile
   . /storage/software/lmod/lmod/init/sh
fi

module --ignore-cache load root/6.24.2
```

In this way galaxy will source the env.sh file before the job is run, ensuring that your environment is set up. 


 
 ## Conventional Analysis (not Jupyter notebooks)
 
**NB! All this is outdated**
 
 ###  `GenericConventionalAnalysis.xml `

#### Requirements to run the tool:

The default header and source file should to placed at location  `/storage/software/anaconda3/envs/fys5555_py3/macros/`
The runner (eg. runSelector.py/GenericRunSelector.py) should be at `/storage/software/bin/`


####  How to use the Tool

 1) Choose which header and source file to use: On Selection of the Use Default file Option the files place at '/storage/software/anaconda3/envs/fys5555_py3/macros/' will be used or If the User selects the Upload the files Option than the User should upload first header file(MySelector.h) and than the source file (MySelector.C).
  -  One should select the type of File when uploading (If its a source.h or a source.c file) and user can see If it is successfully uploaded in the history
 2) Please select the skim: The User should select the skim on which the Analysis should be done 1lep/2lep/3lep etc By defalut 3lep is selected.
 3) Select Specific for above selection: Select If the Analysis should run on Data or MC or both Data and MC .
   - On click Execute the job is send and output is visible in the History which can be downloaded .


## Galaxy interactive tools

### Notebook docker image

Built the fyshep specific jupyternotebook docker image on galaxy-hepp. 
Basis is Bjørns interactive notebook Dockerfile: https://github.com/bgruening/docker-jupyter-notebook.git. I just added root version 6.24.2 and other software to the. 

This was done on hepp02 since docker is installed there. 

I *think* one needs to make sure to manually docker pull the image on hepp02/03 before being able to run the tool.d

Links
- [Dockerfile and procedure here ](https://github.uio.no/IT-ITF/sw-portals-team-jupyter-docker-build)
- [Docker image on dockerhub](https://hub.docker.com/repository/docker/maikenp/docker-jupyter-notebook-fys5555)



### interactivetool_jupyter_notebook_fys5555_py3.xml
Uses the custom built image desribed above:
```
<container type="docker">maikenp/docker-jupyter-notebook_fys5555:latest</container>
``` 

### Outdated anaconda procedure
**This is now replaced with Easybuild by Sabry**

Followed https://github.uio.no/IT-ITF/internal-docs/blob/master/scientific-sw-and-portals-team/conda/index.md to set up anaconda. 
Anaconda is installed on /storage/anaconda3 (not /opt/anaconda3 as the instructions suggest)

To install packages one must first do

```
source /storage/software/anaconda3/conda.start
```

## FYS5555 course material
You can find the fyshep specific course material in 
```
/storage/shared/software
```

### First time setup 
To set up the anaconda software environment for fys5555 course:
```
source /storage/software/anaconda3/conda.start
conda env create -f /storage/software/src/FYS5555/environment_fys5555_py3.yml 

```
### Subsequent use

```
source /storage/software/anaconda3/conda.start
conda activate fys5555_py3
```


## SSL certificate dump
Just to have it saved somewhere, tried in the docker container after having copied the ca-bundle.crt from /etc/ssl/certs on galaxy-hepp:

```
awk 'BEGIN {c=0;} /BEGIN CERT/{c++} { print > "cert." c ".pem"}' < ca-bundle.crt 
c_rehash .
cp -P *.* /etc/ssl/certs/

#then I did (other approach)
awk 'BEGIN {c=0;} /BEGIN CERT/{c++} { print > "cert." c ".crt"}' < ca-bundle.crt 
  c_rehash .
  cp *crt /usr/local/share/ca-certificates/
update-ca-certificates 
  
```

## Python LDAP fix
Galaxy has a dependency requirement for ldap authenticaiton : ```python_ldap_3.2.0``` which kills the uwsgi server (Segmentation fault error). To fix this, a special task in the role _galaxyhepp.customized_ called `customized_dependencies.yml` replaces version 3.2.0 by 3.3.1

_Warning!_ The packages `python-devel` and `openldap-devel` must be installed on the host
