from galaxy.jobs.mapper import JobMappingException
from galaxy.jobs import JobDestination
import os
import logging

log = logging.getLogger(__name__)

FAILURE_MESSAGE = 'This tool could not be run because of a misconfiguration in the Galaxy job running system, please report this error'

def integrate_job_destination_params(app, tool, job):

         param_dict = job.get_param_values(app)
         log.debug("Parameteres dictionary list %s " % param_dict)

         time = str(param_dict['__job_resource']['time'])
         memory = str(param_dict['__job_resource']['memory'])
         project = str(param_dict['__job_resource']['project'])
         nodes = str(param_dict['__job_resource']['nodes'])
         partition = str(param_dict['__job_resource']['partition'])
         processors = str(param_dict['__job_resource']['processors'])

         log.info('=================================== Generate SLURM JOB PARAMS ====================')
         log.info('returning SLURM JOB PARAMS time: %s , memory: %s, project: %s, processors: %s, partition: %s, nodes: %s ' % (time, memory, project, processors, partition, nodes))

         params = {}
         params['nativeSpecification'] = "--account=%s  --time=%s:00:00  --mem-per-cpu=%s  --ntasks=%s --partition=%s --nodes=%s" % (  project, time, memory, processors, partition, nodes)

         return JobDestination(id="real_user_cluster", runner="slurm", params=params)

