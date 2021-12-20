import pandas as pd
import sys
from utils import *
import os

logger = get_logger('datacollection', file=True)
logger.setLevel(logging.DEBUG)

data_dir = 'data/umudga/csv/'
#dga_files = [_ for _ in os.listdir(data_dir) if _.endswith(r".csv")]
dga_files = ['alureon.csv', 'banjori.csv', 'cryptolocker.csv', 'dyre.csv', 'gozi.csv',
             'kraken.csv', 'locky.csv', 'matsnu.csv', 'murofet.csv', 'necurs.csv', 'padcrypt.csv', 'pushdo.csv',
             'pykspa.csv', 'qakbot.csv', 'ramdo.csv', 'ramnit.csv', 'rovnix.csv', 'suppobox.csv',
             'tinba.csv']
logger.info(f"Generating total DGA types: {len(dga_files)}")
#dga_files = ['cryptolocker', 'gozi', 'matsnu', 'pushdo', 'ramdo', 'suppobox']
legit_file = 'all_legit.txt'
dataset_file = data_dir + 'dataset_big_legit' + '.csv'
if os.path.exists(dataset_file):
    os.remove(dataset_file)
dataset = pd.DataFrame()
#dataset.columns = ['domain']
for dga in dga_files:
    logger.info(f'Parsing DGA: {dga}')
    dga_df = pd.read_csv(data_dir + dga)
    dga_df = dga_df.filter(['domain'])
    dga_df['label'] = os.path.splitext(dga)[0]
    logger.debug(f'{dga}_df shape: {dga_df.shape} and \n {dga_df.head()}')
    dataset = dataset.append(dga_df, ignore_index=True)

logger.debug(f'dataset: {dataset.shape} and \n{dataset.head()}')
logger.info(f"Combined DGA dataset stats:\n{dataset['label'].value_counts()}")

logger.info("Reading legit domains")

legit = pd.read_csv(data_dir + legit_file, header=None, sep=' ')
legit_df = pd.DataFrame(legit[0])  # take only domain name column
#legit_df = legit.sample(n=40000)
# legit_df.shape
legit_df.columns = ['domain']
legit_df.columns
legit_df['label'] = 'legit'
legit_df = legit_df[:500000]
logger.debug(f'legit_df shape:{legit_df.shape} and \n {legit_df.head()}')

logger.info('Appedning legit domains')
dataset = dataset.append(legit_df, ignore_index=True)

logger.debug(f'Size of dataset after adding legit domains: {dataset.shape} \
and \n {dataset.head()}')

logger.info(
    f"Stats after adding legit domains:\n{dataset['label'].value_counts()}")

logger.info(f'Saving complete dataset to file: {dataset_file}')
dataset.to_csv(dataset_file, index=False)

r_d = pd.read_csv(dataset_file)
r_d.label.value_counts()
r_d.head()
r_d.shape
logger.debug(f"r_d:\n{r_d.head()} \nand stats:\n{r_d['label'].value_counts()}")
