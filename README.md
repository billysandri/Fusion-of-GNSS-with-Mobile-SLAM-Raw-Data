# Fusion of GNSS mwith Mobile SLAM

#### This repository stores the raw data and processing scripts for the paper 'Fusion of GNSS with Mobile SLAM.'

- Raw data from the experiments including rejected data is included in 'raw_data_all_sets'
- Raw data for each circuit used in the results is given in 'raw_data_for_circuits'. This data includes the selected measurement points as 'device_points.csv,' 'gnss_points.csv' and 'fused_points.csv.' The 3 files are combined into one 'point_data.csv' file which was used for finding the results in the results excel spreedsheet. 'Range.csv' is the range of GNSS ids used in the scripts to find the measured point.
- Data processing scripts are stored in the 'data_processing_scripts' folder. The scripts may need hard coded filenames changed.
- Results data is placed in a convenient 'results_data' folder. These files are the 'points_data.csv' files from each circuit in 'raw_data_for_circuits.'
- 'final_testing.qgz' was used to visualise the raw data. Layer data may not load as filenames have changed.
- 'fusion_of_gnss_with_mobile_slam_results.xlsx' was used for calculating the results. Table data may not load as filenames will be different.
- Control point data is found in 'control_points.txt.'