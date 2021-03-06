import luigi
import logging
import sciluigi.util

logfmt_stream   = '%(asctime)s | %(levelname)8s | %(message)s'
logfmt_luigi    = '%(asctime)s %(levelname)8s    LUIGI %(message)s'
logfmt_sciluigi = '%(asctime)s %(levelname)8s SCILUIGI %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'

def setup_logging():
    sciluigi.util.ensuredir('log')
    log_path = 'log/sciluigi_run_%s_detailed.log' % sciluigi.util.timepath()

    # Formatter
    stream_formatter = logging.Formatter(logfmt_stream, datefmt)
    luigi_log_formatter = logging.Formatter(logfmt_luigi, datefmt)
    sciluigi_log_formatter = logging.Formatter(logfmt_sciluigi, datefmt)

    # Stream handler (for STDERR)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(stream_formatter)
    stream_handler.setLevel(logging.INFO)

    # File handler
    luigi_file_handler = logging.FileHandler(log_path)
    luigi_file_handler.setFormatter(luigi_log_formatter)
    luigi_file_handler.setLevel(logging.DEBUG)

    sciluigi_file_handler = logging.FileHandler(log_path)
    sciluigi_file_handler.setFormatter(sciluigi_log_formatter)
    sciluigi_file_handler.setLevel(logging.DEBUG)

    # Loggers
    luigi_logger = logging.getLogger('luigi-interface')
    luigi_logger.addHandler(luigi_file_handler)
    luigi_logger.addHandler(stream_handler)
    luigi_logger.setLevel(logging.WARN)
    luigi.interface.setup_interface_logging.has_run = True

    sciluigi_logger = logging.getLogger('sciluigi-interface')
    sciluigi_logger.addHandler(stream_handler)
    sciluigi_logger.addHandler(sciluigi_file_handler)
    sciluigi_logger.setLevel(logging.DEBUG)

setup_logging()

def run(*args, **kwargs):
    luigi.run(*args, **kwargs)

def run_local(*args, **kwargs):
    run(local_scheduler=True, *args, **kwargs)
