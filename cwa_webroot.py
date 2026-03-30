import csv
from constants import *


cw_input_file = COMPANY_CWA_INPUT_FILE
wr_input_file = COMPANY_WR_INPUT_FILE
out_file = COMPANY_TOTAL_OUTPUT_FILE
output_list = []
new_headers = ['Device Name',
               'Domain',
               'Last logged on user',
               'OS',
               'Current AV',
               'Last seen in CWA',
               'Last seen in WR',
               ]

wr_device_name_list = []
cwa_device_name_list = []


def read_csv(input_csv):
    with open(input_csv, encoding='utf-8-sig') as csv_file:
        return list(csv.DictReader(csv_file))


def apply_mapping(records: list[dict], mapping: dict) -> list[dict]:
    """
    Takes a list of dicts and applies a mapping of fieldnames to new fieldnames.

    :param records: list of dicts
    :param mapping: dict where keys are new fieldnames and values are old fieldnames.
    :return: list of dicts
    """
    return [
        {out_key: record[in_key].strip() for out_key, in_key in mapping.items()}
        for record in records
    ]


if __name__ == '__main__':

    out_dict_list = []

    cwa_list = read_csv(cw_input_file)
    wr_list = read_csv(wr_input_file)

    cwa_map = {
        "Device Name": "Computer Name",
        "Domain": "Domain",
        "Last logged on user": "Last Logged in User",
        "OS": "OS",
        "Current AV": "Virus Scanner",
        "Last seen in CWA": "Last Contact",
    }

    wr_map = {
        "Device Name": "Name",
        "Domain": "Work Group",
        "Last logged on user": "Current User",
        "OS": "OS",
        "Last seen in WR": "Last Seen",
    }

    reformated_cwa_list = apply_mapping(cwa_list, cwa_map)
    reformated_wr_list = apply_mapping(wr_list, wr_map)

    for cw_device in reformated_cwa_list:
        out_dict = {}
        for mapping in cwa_map:
            out_dict[mapping] = cw_device[mapping]
        for wr_device in reformated_wr_list:
            if out_dict['Device Name'] == wr_device['Device Name']:
                out_dict['Last seen in WR'] = wr_device['Last seen in WR']
        if "Last seen in WR" not in out_dict:
            out_dict['Last seen in WR'] = "Not in Webroot"

        hcc = out_dict['Last seen in CWA'].strip() # "hcc" = horrible cwa checkin...

        # fix the hcc format using string slicing
        out_dict['Last seen in CWA'] = f"{hcc[5:7]}/{hcc[8:10]}/{hcc[0:4]} {hcc[11:16]}"

        out_dict_list.append(out_dict)

    for wr_device in reformated_wr_list:
        match = 0
        for device in out_dict_list:
            if wr_device['Device Name'] == device['Device Name']:
                match += 1
        if match > 0:
            continue
        else:
            wr_device['Last seen in CWA'] = "Not in Automate"
            wr_device['Current AV'] = "Webroot SecureAnywhere 64bit"
            out_dict_list.append(wr_device)


    with open(out_file, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=new_headers)
        writer.writeheader()
        writer.writerows(out_dict_list)


