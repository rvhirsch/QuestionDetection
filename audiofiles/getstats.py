import csv

with open('./sentdata/sents.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    total = 0
    line_count = 0
    for row in csv_reader:
        if row[-1] == "":
            break
        print(row[-1])
        val = row[-1]
        # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
        total += int(val)
        line_count += 1
    print(f'Processed {line_count} lines.')
    print(f'Processed {total} positive lines.')
    print(f'Processed {line_count - total} negative lines.')


# f = open("./sentdata/sents.csv", 'r')
#
# count = 0
# total1 = 0
#
# for line in f:
#     print(line)
#     count += 1
#     splits = line.strip().split(",")
#     total1 += int(splits[-1])
#
# print("total sents:\t", count)
# print("total1:\t", total1)
# print("total0:\t", count-total1)
