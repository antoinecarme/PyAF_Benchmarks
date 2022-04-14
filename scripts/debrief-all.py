import pandas as pd
import numpy as np
import os, glob

benches = "M2_COMP M3_OTHER_COMP M3_Y_COMP M4_COMP_CLIMATE M4_COMP_ECONOMICS  M4_COMP_INTERNET-TELECOM \
            NN3_PART_1  NN5  M1_COMP   M3_M_COMP  M3_Q_COMP M4_COMP_BUSINESS-INDUSTRY  M4_COMP_DEMOGRAPHICS \
            M4_COMP_FINANCE M4_COMP_INVENTORY  NN3_PART_2 FPP2_BENCH".split()

releases = "PyAF-1.0 PyAF-2.0 PyAF-4.0".split()

def create_dir_if_needed(iDir):
    try:
        os.makedirs(iDir);
    except:
        pass


def debrief_log_file(name):
    print("READING_LOG_FILE", name)
    rows = [];
    with open(name) as f:
        content = f.readlines()
    lName = None
    for line in content:
        line = line.replace(" + " , "+")
        if(line.startswith('BENCHMARK_PERF_DETAIL_SIGNAL_HORIZON')):
            (key , lName , lSignal, lLength , lHorizon) = line.split();
        if(line.startswith('BENCHMARK_PERF_DETAIL_BENCH_TIME_IN_SECONDS')):
            (key , lKey2,  lName , lSignal, lTrainingTime) = line.split();
        if(line.startswith('BENCHMARK_PERF_DETAIL_BEST_MODEL')):
            (key , lName , lSignal, lFormula) = line.split();
        if(line.startswith('BENCHMARK_PERF_DETAIL_PERF_COUNT')):
            (key , lName , lSignal, lCount) = line.split();
        if(line.startswith('BENCHMARK_PERF_DETAIL_PERF_MAPE_SMAPE_MASE')):
            (key , lName , lSignal, lMAPE,  lSMAPE, lMASE) = line.split();
            lMASE = lMASE if lMASE != "None" else 100.0
        if(line.startswith('BENCHMARK_PERF_DETAIL_PERF_L1_L2_R2')):
            (key , lName , lSignal, lL1,  lL2,  lR2) = line.split();
    df = pd.DataFrame()
    if(lName is not None):
        row = [lName , lSignal, lLength , lHorizon, round(float(lTrainingTime) , 2), lFormula, lCount, 
               lMAPE,  lSMAPE, lMASE,  lL1,  lL2,  lR2]
        rows = rows + [row]
        df = pd.DataFrame(rows);
        df.columns = "Name Signal Length Horizon TrainingTime Formula Count MAPE SMAPE MASE L1 L2 R2".split()
        for col in "MAPE SMAPE MASE L1 L2 R2".split():
            df[col] = df[col].astype(np.float64)
    return df


def debrief_log_files(names):
    dir_df = pd.DataFrame()
    from multiprocessing import Pool
    pool = Pool(6)

    for df in pool.imap(debrief_log_file, names):
        dir_df = dir_df.append(df)
    return dir_df

def debrief_directory(bench):
    rows = []
    lNames = ["Release", "Perf", "Quantile", "Value"]
    for release in sorted(releases):
        dirname = "run_logs/" + release + "/" + bench
        files = sorted(glob.glob(dirname + "/*.log"))
        dir_df = debrief_log_files(files)
        dir_df.info()
        if(len(dir_df.columns) > 0):
            print(dir_df.describe())
            Q = 10
            lRow = [release]
            for lPerf in ["L1" , "L2", "MAPE", "SMAPE", "TrainingTime"]:
                lQuantiles = dir_df[lPerf].quantile([q / Q for q in range(Q+1)]).round(4)
                lQuantiles = list(lQuantiles)
                print("QUANTILES", bench, release, lPerf, list(dir_df[lPerf].head(Q)), lQuantiles)
                for q in range(Q+1):
                    lRow = [release] + [lPerf] + [q*100//Q] + [lQuantiles[q]]
                    rows = rows + [lRow]
    return pd.DataFrame(rows, columns = lNames)

for bench in sorted(benches):
    print("PROCESSING", (bench))
    df_b = debrief_directory(bench)
    create_dir_if_needed("reports")
    df_b.to_csv( "reports/PyAF_Bench_Report_" + bench + "_debrief.csv", index=False)
