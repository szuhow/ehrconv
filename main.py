import pandas as pd
import json
import warnings
f = open('fin.json')
row = ""


def main():
    with open('data.txt', 'w') as outfile:
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            pd.options.display.max_colwidth = 1000
            workbook = pd.read_excel('fin.xlsx', engine="openpyxl")
            data = json.load(f)
            f.close()
            al = list()
            add = list()
            for index, row in workbook[1:300].iterrows():
                a = ""
                r = row["Path"].split("/")
                for i in r[1::]:
                    if "openEHR-EHR" in i:
                        # try:
                            i = i.replace(i, i.replace(i[i.find("[") + 1:i.rfind("]")], i[i.find("[") + 1:i.rfind("]")].replace(",","").split()[0]))
                        # except:
                        #     pass
                            # i = i.replace(i, i.replace(i[i.find("[") + 1:i.rfind("]")], i[i.find("[") + 1:i.rfind("]")].replace(",","").split()[0]))


                    a += "/"+i
                p = ""
                al.append(a)
                prev = ""
                for part in a.split("/"):
                    p += "/" + part
                    try:
                        if not p.split("/")[-1] == "other_context[at0001]":
                                path = p[1:]
                                a = extract(data, 'aqlPath')[path]
                                a = prev + "/" + a
                                prev = a
                    except KeyError:
                        a = None
                        pass
                    try:
                        if not p.split("/")[-1] == "other_context[at0001]":
                            path = p[1:] + "/value"
                            a = extract(data, 'aqlPath')[path]
                            a = prev + "/" + a
                            prev = a
                    except KeyError:
                        a = None
                        pass
                if a:
                    try:
                        path = a.split("|")[0]
                        code = a.split("|")[1]
                    except:
                        path = a.split("|")[0]
                        code = ""

                    try:
                        value = a.split("|")[2]

                    except:
                        value = ""

                    if value:
                        outfile.write(f'"{path[1:]}|code"' + ": " + f'"{code}"' + ",")
                        print(f'"{path[1:]}|code"' + ": " + f'"{code}"')
                        outfile.write('\n')
                        outfile.write(f'"{path[1:]}|value"' + ": " + f'"{value}"' + ",")
                        print(f'"{path[1:]}|value"' + ": " + f'"{value}"')
                        outfile.write('\n')
                    else:
                        print(f'"{path[1:]}"' + ": " + f'"{code}"'+"," + f'"{value}"')
                        outfile.write(f'"{path[1:]}"' + ": " + f'"{code}"'+",")
                        outfile.write('\n')



def extract(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = {}
    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        prev = 0
        if isinstance(obj, dict):
            max = ""
            code = ""
            value = ""
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == "max":
                    if str(v) == "-1":
                        max = ":0"
                    else:
                        max = ""
                elif k == "id":
                    prev = v
                elif k == key:
                    for a, b in obj.items():
                        if a == "inputs":
                            try:
                                code = "|" + str(b[0]['list'][0]['label'])
                            except:
                                if str(b[0]['type']) == "TEXT":
                                    code = "|" + "null"
                                elif str(b[0]['type']) == "BOOLEAN":
                                    code = "|" + "True"
                                else:
                                    code = "|" + "0"

                                pass

                            try:
                                if str(b[0]['terminology']):
                                    value =  "|" + "null"
                            except:
                                value = "|" + ""
                                pass
                    arr[v] = prev + max + code + value
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr
    results = extract(obj, arr, key)
    return results


if __name__ == '__main__':
    main()
