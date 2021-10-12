sorted_list = []
n = 7
remaining = 0

def test(my_list):
  sorted_list = []
  l = len(my_list)
  remaining = len(my_list) % n
  loop_end = int(l/n)
  start = 0
  for i in range(0, loop_end):
    chunk = my_list[start: start + n]
    chunk = sorted(chunk)
    sorted_list.append(chunk)
    start = n
    # sort
  if remaining:
    last_part = my_list[-remaining:]
    last_part = sorted(last_part)
    sorted_list.append(last_part)
  return sorted_list