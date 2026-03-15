NUM_ROUTES = 64

file = open("routes.py", "w")
for i in range(NUM_ROUTES):

    file.write("@app.route(\"/" + str(i) + "\")\n")
    file.write("def fetch_" + str(i) + "():\n")
    file.write("\twith open(\"output.txt\", \"r\") as file:\n")
    file.write("\t\tcontent = file.read()\n")
    file.write("\t\tstart_index = MAX_CHUNK_SIZE * " + str(i) + "\n")
    file.write("\t\tend_index = start_index + MAX_CHUNK_SIZE\n")
    file.write("\tgc.collect()\n")
    file.write("\t\treturn content[int(start_index):int(end_index)]\n")
    file.write("\n")
