import csv, json, sys
from pathlib import Path

def flattenjson(b, delim):
    val = {}
    for i in b.keys():
        if isinstance( b[i], dict ):
            get = flattenjson( b[i], delim )
            for j in get.keys():
                val[ i + delim + j ] = get[j]
        else:
            val[i] = b[i]

    return val


header = [
    "macro_avg",
    "micro_avg",
    "weighted_avg",
]

if sys.argv[1] is not None and sys.argv[2] is not None:
    fileInput = sys.argv[1]
    fileOutput = sys.argv[2]
    inputFile = Path(fileInput)

    dataJSON = json.loads(inputFile.read_text())
    data = flattenjson(dataJSON, "__")

    with open(fileOutput, "w") as file:
        csv_file = csv.writer(file)

        header_names = []
        for header_name in header:
            for field in ["f1-score", "precision", "recall", "support"]:
                header_names.append(header_name+"__"+field)
        header_names.append("accuracy")

        csv_file.writerow(["name"] + header_names)

        for data_name in dataJSON:
            for configuration in dataJSON[data_name]:
                for row in dataJSON[data_name][configuration]:
                    data = dataJSON[data_name][configuration]
                    row_data = flattenjson(data[row], "__")

                    result = [f"{data_name}/{configuration}/{row}"]
                    for field in header_names:
                        try:
                            result.append(row_data[field])
                        except KeyError:
                            result.append("n/a")

                    csv_file.writerow(result)
