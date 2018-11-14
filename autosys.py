from re import match

class JilParser:

    """Class that parses JIL into jobs"""

    job_comment = '/* -----------------'

    def __init__(self, path):
        """Instantiates a new instance"""

        self.path = path

    def read_jil(self):
        """Reads JIL from a file"""

        lines = []

        with open(self.path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue # skip if line is empty
                lines.append(line.strip())
        
        return lines

    def find_jobs(self, lines):
        """Finds jobs from lines"""

        jobs = {}
        job = ''

        for line in lines:
            
            if line.startswith(self.job_comment):
                matches = match(AutoSysJob.job_start_regex, line)
                if matches:
                    job = matches.group(1)
                    jobs.update({ job : [] })
            else:
                jobs[job].append(line)
        
        return jobs
    
    def parse_jobs(self):
        """Parses jobs from JIL"""

        lines = self.read_jil()
        raw_jobs = self.find_jobs(lines)
        parsed_jobs = []

        for definition in raw_jobs.values():
            job = AutoSysJob.from_str('\n'.join(definition))
            parsed_jobs.append(job)
        
        return parsed_jobs

class AutoSysJob:

    """Class that represents a job within AutoSys and its attributes"""

    comments = ('/*', '#')
    default_attributes = {'insert_job': '','job_type': '','box_name': '','command': '','machine': '','owner': '','permission': '','date_conditions': '','days_of_week': '','start_times': '','run_window': '','condition': '','description': '','n_retrys': '','term_run_time': '','box_terminator': '','job_terminator': '','std_out_file': '','std_err_file': '','min_run_alarm': '','max_run_alarm': '','alarm_if_fail': '','max_exit_status': '','chk_files': '','profile': '','job_load': '','priority': '','auto_delete': '','group': '','application': '', 'exclude_calendar': '', 'send_notification': '', 'notification_msg': '', 'notification_emailaddress': '', 'success_codes': ''}
    
    job_name_comment = '/* ----------------- {} ----------------- */'
    job_start_regex = '\\/\\*\\s*\\-*\\s*([a-zA-Z0-9\\.\\#_-]{1,64})\\s*\\-*\\s*\\*\\/'    

    def __init__(self, job_name = ''):
        """Instantiates a new instance"""

        self.job_name = job_name
        self._attributes = {}
    
    @property
    def attributes(self):
        """Returns attributes"""

        return self._attributes
    
    def __repr__(self):
        """Returns string representation"""

        job_str = self.job_name_comment.format(self._attributes['insert_job']) + '\n\n'

        for attribute, value in self._attributes.items():
            if attribute == 'job_type':
                continue
            if attribute == 'insert_job':
                job_str += '{}: {}   {}: {}\n'.format(attribute, value, 'job_type', self._attributes['job_type'])
            else:
                job_str += '{}: {}\n'.format(attribute, value)

        return job_str

    @classmethod
    def from_str(cls, jil):
        """Creates a new job from a string"""

        job = cls()

        jil = jil.replace('job_type', '\njob_type', 1)
        jil = jil.replace('\r\n', '\n')

        lines = [line.strip() for line in jil.split('\n') if line.strip() != '']

        for line in lines:
            if line.startswith(cls.comments):
                continue
            attribute, value = line.split(':', 1)
            job.attributes[attribute.strip()] = value.strip()

        job.job_name = job.attributes['insert_job']

        return job

# EOF