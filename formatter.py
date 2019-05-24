with open('descriptions', 'r') as rf:
     with open('formatted_descriptions', 'w') as wf:
        for line in rf:
            if line.startswith('b\''):
                wf.write(line[2:-3] + ',\n')
