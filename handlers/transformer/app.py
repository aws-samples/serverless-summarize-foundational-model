# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import trp
from textractprettyprinter.t_pretty_print import convert_table_to_list, Pretty_Print_Table_Format, Textract_Pretty_Print, get_string

def collect_text(event):
    text = []

    for item in event["Blocks"]:
        if item["BlockType"] == "LINE":
            text.append(item["Text"])

    textract_text = " ".join(text)
    return textract_text

def collect_tables(extracted):
    '''
    Write code to extract tables from textract output
    '''

    kv_list = get_string(
        textract_json=extracted,
        table_format=Pretty_Print_Table_Format.csv,
        output_type=[Textract_Pretty_Print.FORMS]
    )
    print(kv_list)

    dfs = []
    doc = trp.Document(extracted)
    for page in doc.pages:
        for table in page.tables:
            tab_list = convert_table_to_list(trp_table=table)
            dfs.extend(tab_list)

    return [{'key':a[0], 'value': a[1]} for a in dfs]

def lambda_handler(event, context):
    # print(json.dumps(event))

    text = collect_text(event)
    tables = collect_tables(event)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "text": text,
            "tables": tables,
            "forms": ""
        }),
    }
