NUM_ROUTES = 64

file = open("routes.py", "w")
for i in range(NUM_ROUTES):

    file.write("@app.route(\"/" + str(i) + "\")\n")
    file.write("def fetch_" + str(i) + "():\n")
    file.write("\tfile = open(\"output.txt\", \"r\")\n")
    file.write("\tcontent = file.read()\n")
    file.write("\tstart_index = MAX_CHUNK_SIZE * " + str(i) + "\n")
    file.write("\tend_index = start_index + MAX_CHUNK_SIZE\n")
    file.write("\treturn content[int(start_index):int(end_index)]\n")
    file.write("\n")
