import csv
from constants import *


cw_input_file = COMPANY_CWA_INPUT_FILE
wr_input_file = COMPANY_WR_INPUT_FILE
out_file = COMPANY_TOTAL_OUTPUT_FILE
output_list = []
new_headers = ['Device Name',
               'Domain',
               'Last logged on user',
               'OS Type',
               'Current AV',
               'Last seen in CWA',
               'Last seen in WR',
               ]

wr_device_name_list = []
cwa_device_name_list = []


def read_csv(input_csv):
    out_list = []
    with open(input_csv, encoding='utf-8') as csv_file:
        headers = csv_file.readline().strip('\n').split(',')
        reader = csv.reader(csv_file)
        for row in reader:
            out_list.append(row)
    return headers, out_list


if __name__ == '__main__':

    cwa_headers, cwa_list = read_csv(cw_input_file)
    wr_headers, wr_list = read_csv(wr_input_file)


    for wr_device in wr_list:
        wr_device_name_list.append(wr_device[0].strip())

    for cwa_device in cwa_list:
        cwa_device_name_list.append(cwa_device[1].strip())

    for device in cwa_list:
        prepped_device = []
        if device[1].strip() in wr_device_name_list:
            for wr_device in wr_list:
                if device[1].strip() == wr_device[0].strip():
                    wr_device_last_seen = wr_device[5].strip()
        else:
            wr_device_last_seen = 'not in Webroot'
        hcc = device[13].strip() # "hcc" = horrible cwa checkin...
        fixed_cwa_last_checkin = (f"{hcc[5:7]}/{hcc[8:10]}/{hcc[0:4]} {hcc[11:16]}")

        prepped_device.extend([device[1].strip(),
                               device[9].strip(),
                               device[14].strip(),
                               device[5].strip(),
                               device[11].strip(),
                               fixed_cwa_last_checkin,
                               wr_device_last_seen,
                               ])
        output_list.append(prepped_device)

    for device in wr_list:
        prepped_device = []
        if device[0].strip() in cwa_device_name_list:
            continue
        if 'Server' in device[14]:
            wr_os_type = 'Server'
        else:
            wr_os_type = 'Workstation'
        prepped_device.extend([device[0].strip(),
                               device[18].strip(),
                               device[19].strip(),
                               wr_os_type,
                               'Webroot SecureAnywhere 64bit',
                               'not in Automate',
                               device[5].strip(),
                               ])
        output_list.append(prepped_device)



    with open(out_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(new_headers)
        writer.writerows(output_list)

