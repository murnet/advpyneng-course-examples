

def sum_arg(**kwargs):
    print(f"{kwargs=}")
    sum_num = 0
    for arg in kwargs.values():
        sum_num += arg
    return sum_num
