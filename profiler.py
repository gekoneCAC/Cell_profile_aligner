import pandas as pd

READFILECSV = r"data/S81 HL t360_6reg_profile.csv"
PROFILERCSV = r"data/profiler_result.csv"
PROFILERALIGNEDCSV = r"data/profiler_aligned.csv"

# read file
df = pd.read_csv(READFILECSV, sep=',')

# create range that I will align results
dfResults = list(range(-30, 31))
dfResults = pd.DataFrame(dfResults)
arrayShift = list(range(0, 24))

# normalize profiles to peak emisions (to get position from center)
for i in range(1, 73):
    dfx = df.iloc[:, i] # gets all the column 0
    normalized_dfx = (dfx - dfx.min()) / (dfx.max() - dfx.min()) # normalisation within 1 column
    frames = [dfResults, normalized_dfx]
    dfResults = pd.concat(frames, axis = 1)
    col1maxpos = df.loc[dfx.idxmax()]
    # populate array of shift; this will allow aligning other membranes to chlorophyll peaks
    if i >= 49:
        arrayShift[i-49] = 41 - int(col1maxpos[0])


# save first round of aligning
dfResults.to_csv(PROFILERCSV, sep=";", index = False)

# create new range that I will align results
dfResultsAligned = list(range(-40, 41))
dfResultsAligned = pd.DataFrame(dfResultsAligned)

# populate new range with Chlorophyll shifts
for i in range(0, 24):
    dfx = dfResults.iloc[:, i+1]
    dfxShift = dfx.shift(arrayShift[i-0])
    frames = [dfResultsAligned, dfxShift]
    dfResultsAligned = pd.concat(frames, axis = 1)
for i in range(25, 49):
    dfx = dfResults.iloc[:, i]
    dfxShift = dfx.shift(arrayShift[i-25])
    frames = [dfResultsAligned, dfxShift]
    dfResultsAligned = pd.concat(frames, axis = 1)
for i in range(49, 73):
    dfx = dfResults.iloc[:, i]
    dfxShift = dfx.shift(arrayShift[i-49])
    frames = [dfResultsAligned, dfxShift]
    dfResultsAligned = pd.concat(frames, axis = 1)
    
# save file
dfResultsAligned.to_csv(PROFILERALIGNEDCSV, sep=";", index = False)