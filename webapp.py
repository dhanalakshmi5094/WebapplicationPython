import pandas as pd
from datetime import datetime
import time
from tabulate import tabulate

# Define attributes
sub_task_status = []
duration = []
start_time = []
end_time = []
task_start_time_stamp = []
task_end_time_stamp = []
task_id = []
task_name = []
start_date = []
end_date = []
start_time_stamp = []
end_time_stamp = []
duration = []
net_duration = []
sum_net_time = []
net_time = []
time_start = []
time_end = []
task_status = []

# read a comma separated values into DataFrame
df = pd.read_csv('data.csv')

# output_df is copying required columns from existing DataFrame
output_df = df[['task_id', 'task_name']]

# display current time and Date
current_date = datetime.now()
'''
Calculates start_time_stamp,end_time_stamp duration,net_duration,and status of each task
by iterating through each row of data.csv file
'''
for i in range(0, df.index.size):
    if df.parent_task_id[i] != "Nan":
        # calculate sub task start,end timestamps,status,duration and net duration
        timesince1 = time.strptime(df.end_date[i], "%Y:%m:%d:%H:%M:%S")
        timesince2 = time.strptime(df.start_date[i], "%Y:%m:%d:%H:%M:%S")
        # This method returns a floating point number, for compatibility with time() in seconds.
        timesince = time.mktime(timesince1) - time.mktime(timesince2)
        # Calculates duration in minutes
        duration = int(timesince / 60.0)
        start_time_stamp = df.start_date[i]
        end_time_stamp = df.end_date[i]
        # calculating status of sub_task based on given conditions as per assignment
        if df.start_date[i] > str(current_date):
            task_status = "Scheduled"
        elif df.start_date[i] < str(current_date) < df.end_date[i]:
            task_status = "Running"
        elif str(current_date) > df.end_date[i]:
            task_status = "Complete"
        # for sub_task ,duration and net_duration will be same
        net_duration = duration
        # adding all values calculated above to output data frame
        output_df.loc[i, 'start_time_stamp'] = start_time_stamp
        output_df.loc[i, 'end_time_stamp'] = end_time_stamp
        output_df.loc[i, 'duration'] = duration
        output_df.loc[i, 'net_duration'] = net_duration
        output_df.loc[i, 'task_status'] = task_status
    else:
        # this is for the last row of data frame and for which parent_task_id is "Nan"
        if int(df.task_id[i]) == int(df.index.size):
            timesince1 = time.strptime(df.end_date[i], "%Y:%m:%d:%H:%M:%S")
            timesince2 = time.strptime(df.start_date[i], "%Y:%m:%d:%H:%M:%S")
            timesince = time.mktime(timesince1) - time.mktime(timesince2)
            duration = int(timesince / 60.0)
            start_time_stamp = df.start_date[i]
            end_time_stamp = df.end_date[i]
            # calculating status of task based on given conditions as per assignment
            if df.start_date[i] > str(current_date):
                task_status = "Scheduled"
            elif df.start_date[i] < str(current_date) < df.end_date[i]:
                task_status = "Running"
            elif str(current_date) > df.end_date[i]:
                task_status = "Complete"
            net_duration = duration
            output_df.loc[i, 'start_time_stamp'] = start_time_stamp
            output_df.loc[i, 'end_time_stamp'] = end_time_stamp
            output_df.loc[i, 'duration'] = duration
            output_df.loc[i, 'net_duration'] = net_duration
            output_df.loc[i, 'task_status'] = task_status
        else:
            # this is for the row which parent_task_id is "Nan"
            count = 0
            j = df.task_id[i]
            # which compares the present row  task_id with parent_task_id of next rows.
            for j in range(j, df.index.size):
                if df.parent_task_id[j] != "Nan":
                    if int(df.task_id[i]) == int(df.parent_task_id[j]):
                        start_time.insert(count, df.start_date[j])
                        end_time.insert(count, df.end_date[j])
                        count += 1
                        j += 1
                    else:
                        j += 1
                else:
                    j += 1
            # Calculates the net_duration of each task
            for k in range(0, len(start_time)):
                time_start.insert(k, time.mktime(time.strptime(start_time[k], "%Y:%m:%d:%H:%M:%S")))
                k += 1
            for m in range(0, len(end_time)):
                time_end.insert(m, time.mktime(time.strptime(end_time[m], "%Y:%m:%d:%H:%M:%S")))
                m += 1
            # zip()  returns an iterator of tuples
            zip_object = zip(time_start, time_end)
            for start_time_p, end_time_p in zip_object:
                net_time.append(end_time_p - start_time_p)
            sum_net_time = 0.0
            for r in range(0, len(net_time)):
                sum_net_time += net_time[r]
                r += 1
            sum_net_time = int(sum_net_time / 60.0)
            start_time_stamp = min(start_time)
            end_time_stamp = max(end_time)
            timesince1 = time.strptime(end_time_stamp, "%Y:%m:%d:%H:%M:%S")
            timesince2 = time.strptime(start_time_stamp, "%Y:%m:%d:%H:%M:%S")
            timesince = time.mktime(timesince1) - time.mktime(timesince2)
            duration = int(timesince / 60.0)
            # Calculates status of parent_task based on given conditions as per assignment
            runs_count = 0
            # Calculates how many times a task is running
            for q in start_time:
                for s in end_time:
                    if q < str(current_date) < s:
                        runs_count += 1
                        break
                    else:
                        break
                continue
            if start_time_stamp > str(current_date):
                task_status = "Scheduled"
            elif runs_count == 1:
                task_status = "Running"
            elif runs_count > 1:
                task_status = "Multi-Runs"
            else:
                task_status = "Idle"

            output_df.loc[i, 'start_time_stamp'] = start_time_stamp
            output_df.loc[i, 'end_time_stamp'] = end_time_stamp
            output_df.loc[i, 'duration'] = duration
            output_df.loc[i, 'net_duration'] = sum_net_time
            output_df.loc[i, 'task_status'] = task_status

i += 1
# for printing the output in tabular format
headers = ["task_id", "task_name", "start_time_stamp", "end_time_stamp", "duration", "net_duration", "task_status"]
print(tabulate(output_df, headers, tablefmt="grid"))


