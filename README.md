
# Lifeportal on FOX

# Some custom requirements

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
		
## OpenIdc 

