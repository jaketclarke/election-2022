import wget
import os
import numpy as np
import pandas as pd
import geopandas as gpd
from functions import empty_directory, make_directorytree_if_not_exists

outputDir = 'output'
dataDir = 'test'
make_directorytree_if_not_exists(outputDir)

# sa1 data
sa1DataPath = f'{dataDir}{os.sep}pp-by-sa1.csv'
sa1Data = pd.read_csv(sa1DataPath)
print(sa1Data)

# normalise with df file names
# note - checked the underlying data and the ccd column (change the name for god sake!) is 2016 SA1s
sa1Data.rename({
    'state_ab': 'StateAb',
    'div_nm': 'DivisionNm',
    'ccd_id': "sa1_2016",
    'pp_id': 'PollingPlaceID',
    'pp_nm': 'PollingPlace',
    'votes': 'VotesSA1'
}, axis=1, inplace=True)

print(sa1Data)
# # vote data
# voteTypeDataPath = f'{outputDir}{os.sep}aus-type-unpivot.csv'
# voteTypeData = pd.read_csv(voteTypeDataPath)
# print(voteTypeData)

