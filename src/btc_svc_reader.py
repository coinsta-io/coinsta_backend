def get_sample_btc_data():
    f = open("gemini_BTCUSD_1hr.csv", "r")

    lines = f.readlines()
    lines = lines[2::24]
    lines.sort()

    data = []
    for line in lines:
        split_line = line.split(',')
        date = split_line[1].split(' ')[0]
        price = split_line[3]
        data.append({
            'date': date,
            'price': price
        })
    return data


    