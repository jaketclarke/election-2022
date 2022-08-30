import wget
import os
import pandas as pd
import geopandas as gpd
from functions import empty_directory, make_directorytree_if_not_exists

outputDir = 'output'
dataDir = 'data'
make_directorytree_if_not_exists(outputDir)

# initial job - read and unpivot the votetype data
voteTypeDataPath = f'{dataDir}{os.sep}aus-type.csv'
voteTypeData = pd.read_csv(voteTypeDataPath, skiprows=1)
# print(voteTypeData)

voteTypeDataUnpivot = pd.melt(
    voteTypeData,
    id_vars=['StateAb','DivisionID','DivisionNm','CandidateID','Surname','GivenNm','BallotPosition','Elected','HistoricElected','PartyAb','PartyNm'],
    value_vars=['OrdinaryVotes','AbsentVotes','ProvisionalVotes','PrePollVotes','PostalVotes','TotalVotes','Swing'],
    var_name='type',
    value_name='value'
)

voteTypeDataUnpivotFileName = 'aus-type-unpivot'
voteTypeDataUnpivotFilePath = f'{outputDir}{os.sep}{voteTypeDataUnpivotFileName}.csv'

voteTypeDataUnpivot.to_csv(voteTypeDataUnpivotFilePath, index=False)