import xlrd
import json
def read_excel_and_create_dict(file_path, sheet_name):
    # 读取Excel表格
    wb = xlrd.open_workbook(file_path)
    sheet = wb.sheet_by_name(sheet_name)

    # 创建一个字典，将第5列作为键，第6和25列作为值
    data_dict = {}
    for row_idx in range(1, sheet.nrows):
        key = sheet.cell_value(row_idx, 7)  # 第8列作为键
        value_1 = sheet.cell_value(row_idx, 6)  # 第7列作为第一个值
        value_2 = sheet.cell_value(row_idx, 24)  # 第25列作为第二个值
        data_dict[key] = (value_1, value_2)

    return data_dict

def filter_and_process_data(data_dict):
    new_dict = {}
    for key, values in data_dict.items():
        g_column_data = values[0]
        y_column_data = values[1]
        if y_column_data != '':
                # 将第25列的字符串以'\n'为分隔符拆分为列表
                split_values = y_column_data.strip().split('\n')
                # 将数据存储在新的字典中
                new_dict[key] = (g_column_data,split_values)
    
    return new_dict


file_path = "sample.xls"  # 替换成Excel文件路径
sheet_name = "BDCAN"  # 替换成表格名称
data_dict = read_excel_and_create_dict(file_path, sheet_name)
filtered_dict = filter_and_process_data(data_dict)
output = []
for key, (signal_name, params) in filtered_dict.items():
    item = {
        '名称': key+signal_name,

        '参数': params
    }
    output.append(item)

# Convert the output list to a JSON string
json_output = json.dumps(output, ensure_ascii=False, indent=4)

# Print the JSON output
print(json_output)

# Write the JSON output to a text file
with open('data.json', 'w', encoding='utf-8') as file:
    file.write(json_output)

print("JSON data has been written to 'data.txt'")