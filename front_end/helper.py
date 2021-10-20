
def sort_bboxes(my_list):
  sorted_list = []
  n = 7
  l = len(my_list)
  remaining = len(my_list) % n
  loop_end = int(l/n)
  start = 0
  for i in range(0, loop_end):
    end = start + n
    chunk = my_list[start: end]
    print(chunk[0][0][0],0)
    print('\n')
    #chunk = sorted(chunk)
    chunk = sorted(chunk, key=lambda y: y[0][0][0])
    sorted_list.append(chunk)
    start = n
    # sort
  if remaining:
    last_part = my_list[-remaining:]
    #last_part = sorted(last_part)
    last_part = sorted(last_part, key=lambda y: y[0][0][0])
    sorted_list.append(last_part)
  
  sorted_list = [item for my_list in sorted_list for item in my_list]
  
  return sorted_list