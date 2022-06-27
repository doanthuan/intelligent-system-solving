class Logs:
    g_outputs = []
    def log_output(*texts):
        # str_list = []
        # for text in texts:
        #     str_list.append(text)
        g_outputs.append(texts)

    def print_output():
        while len(g_outputs) > 0:
            texts = g_outputs.pop(0)
            print(*texts)