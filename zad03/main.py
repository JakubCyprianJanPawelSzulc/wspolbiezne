from multiprocessing import Process, Value, Queue

def count_word_occurrences(file_path, word, total_occurrences):
    with open(file_path, 'r') as file:
        text = file.read()
        with total_occurrences.get_lock():
            total_occurrences.value += text.count(word)

def process_file(file_path, word, total_occurrences, process_order_queue):
    input_directives = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('\\input{') and line.endswith('}\n'):
                input_directives.append(line[7:-2])
    
    count_word_occurrences(file_path, word, total_occurrences)
    
    child_processes = []
    for directive in input_directives:
        process = Process(target=process_file, args=(directive, word, total_occurrences, process_order_queue))
        process.start()
        child_processes.append(process)
    
    for process in child_processes:
        process.join()
    
    process_order_queue.put(file_path)

if __name__ == '__main__':
    file_path = "plikA.txt"
    word = "i"
    total_occurrences = Value('i', 0)
    process_order_queue = Queue()

    process_file(file_path, word, total_occurrences, process_order_queue)

    finished_processes = []
    while not process_order_queue.empty():
        finished_processes.append(process_order_queue.get())

    print("Wszytskie wystąpienia:", total_occurrences.value)
    print("Kolejność zakończonych procesów:", finished_processes)
