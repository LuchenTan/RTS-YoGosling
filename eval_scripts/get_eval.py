from subprocess import Popen, PIPE, STDOUT
import logging
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--run', help='indicating the location of run file', required=True)
parser.add_argument('-y', '--year', help='indicating the RTS Track year',
                    choices=set(('16', '17')), required=True)
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

if args.year == '16':
    mobile_eval = 'rts2016-mobileA-eval.py'
    mobile_qrel = 'rts2016-mobileA-qrels.txt'
    mobile_epoch = 'rts2016-mobileA-tweets2dayepoch.txt'
    batch_eval = 'rts2016-batchA-eval.py'
    batch_qrel = 'rts2016-batch-qrels.txt'
    batch_cluster = 'rts2016-batch-clusters.json'
    batch_epoch = 'rts2016-batch-tweets2dayepoch.txt'
elif args.year == '17':
    mobile_eval = 'rts2017-mobile-eval.py'
    mobile_qrel = 'rts2017-mobile-qrels.txt'
    mobile_epoch = 'rts2017-mobile-tweets2dayepoch.txt'
    batch_eval = 'rts2017-batchA-eval.py'
    batch_qrel = 'rts2017-batch-qrels'
    batch_cluster = 'rts2017-batch-clusters.json'
    batch_epoch = 'rts2017-batch-tweets2dayepoch.txt'

logger.info('Mobile Assessment Results: ')
process_mobile = Popen('python3 {} -q {} -t {} -r {}'.format(mobile_eval,
                                                             mobile_qrel,
                                                             mobile_epoch,
                                                             args.run),
                       stdout=PIPE, stderr=STDOUT, shell=True)
process_mobile_output, _ = process_mobile.communicate()
lines = process_mobile_output.rstrip().splitlines()
for line in [lines[0], lines[-1]]:
    logger.info('\t'.join(str(line.rstrip()).split('\\t')))
sys.stdout.write = logger.info

logger.info('Batch Assessment Results:')
process_batch = Popen('python3 {} -q {} -t {} -c {} -r {}'.format(batch_eval,
                                                                  batch_qrel,
                                                                  batch_epoch,
                                                                  batch_cluster,
                                                                  args.run),
                      stdout=PIPE, stderr=STDOUT, shell=True)
process_batch_out, _ = process_batch.communicate()
lines = process_batch_out.rstrip().splitlines()
for line in [lines[0], lines[-1]]:
    logger.info('\t'.join(str(line.rstrip()).split('\\t')))