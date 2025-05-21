#формула расчета процента выполнения и индикатор
def progress_bar(percentage):
    filled = '█' * int(percentage / 10)
    empty = '░' * (10 - len(filled))
    return f"{filled}{empty} {percentage:.1f}%"

def format_report(data):
    point = data['point']
    pd = data['point_data']