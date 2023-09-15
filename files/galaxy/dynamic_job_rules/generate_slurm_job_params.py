from galaxy.jobs.mapper import JobMappingException
import os
import logging

log = logging.getLogger(__name__)

FAILURE_MESSAGE = 'This tool could not be run because of a misconfiguration in the Galaxy job running system, please report this error'

def integrate_job_destination_params(app, tool, job):
    
     destination = None
     destination_id = 'slurm'
     
     param_dict = job.get_param_values(app)
     log.debug("Parameteres dictionary list %s " % param_dict)

     if param_dict['__job_resource']['__job_resource__select'] == "no" :
         destination = app.job_config.get_destination(destination_id)
         # set walltime
         if 'nativeSpecification' not in destination.params:
              destination.params['nativeSpecification'] = ''
         destination.params['nativeSpecification'] = "--account=ec73   --time=01:00:00   --mem-per-cpu=1024"

         log.info('returning destination: %s', destination_id)
         log.info('native specification: %s', destination.params.get('nativeSpecification'))
         return destination or destination_id
     
     else:

         try:

   	         # Get all required params from the tool menu : job resource parameters
              time = str(param_dict['__job_resource']['time'])
              memory = str(param_dict['__job_resource']['memory'])
              project = str(param_dict['__job_resource']['project'])

              destination = app.job_config.get_destination(destination_id)
              # set walltime
              if 'nativeSpecification' not in destination.params:
                      destination.params['nativeSpecification'] = ''
              destination.params['nativeSpecification'] = "--account=%s  --time=%s:00:00  --mem-per-cpu=%s " % (project,time,memory)
         except:
         
             # resource param selector not sent with tool form, job_conf.xml misconfigured
             log.warning('(%s) error, keys were: %s', job.id, param_dict.keys())
             raise JobMappingException(FAILURE_MESSAGE)
    
         log.info('returning destination: %s', destination_id)
         log.info('native specification: %s', destination.params.get('nativeSpecification'))
         return destination or destination_id

