from galaxy.jobs import JobDestination
from galaxy.jobs.mapper import JobMappingException
import os
import logging

log = logging.getLogger(__name__)

def is_user_in_role(user, app, tool, required_role):

    if user is None:
        raise JobMappingException('You must login to use this tool!')

    if required_role is None:
         raise JobMappingException("Missing required_role for the tool id in the in job_conf.xml for tool '%s' " % tool.id)
 
    # Check that the required_role is in the set of role names associated with the user
    user_roles = user.all_roles() # a list of roles
    user_in_role = required_role in [role.name for role in user_roles]

    if user_in_role:
        return True
    else:
        return False


def analyse_and_plot(user, app, tool):

    required_role = "run_analyse_and_plot"
    if is_user_in_role(user, app, tool, required_role) is True:
         return JobDestination(runner="slurm")
    else:
         raise JobMappingException("This tool is restricted to users associated with the '%s' role, please contact a site administrator to be authorized!" % required_role)


def statistics(user, app, tool):
    required_role = "run_statistics"
    params = {}

    if is_user_in_role(user, app, tool, required_role) is True:
             cpus_per_task = '75'
    else:
             cpus_per_task = '20'

    params['nativeSpecification'] = "--cpus-per-task=%s" % (cpus_per_node)
    return JobDestination(runner="slurm", params=params)




def jupyter(user, app, tool):
    required_role = "run_statistics"
    params = {}
    
    params["docker_enabled"] = "true"
    params["docker_volumes"] = "$defaults,/storage/shared/data:ro,/storage/shared/software:ro"
    params["docker_sudo"] = "false"
    params["docker_net"] = "bridge"
    params["docker_auto_rm"] = "true"
    params["docker_set_user"] = ""
    params["require_container"] = "true"

    if is_user_in_role(user, app, tool, required_role) is True:
        cpus_per_node = '75'
    else:
        cpus_per_node = '20'
        
    params['nativeSpecification'] = "--cpus-per-task=%s" % (cpus_per_node)
    return JobDestination(runner="slurm", params=params)


    
