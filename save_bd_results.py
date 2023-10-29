import sqlite3


def write_sqlite(game_name, winner):
    """функция используется для записи в БД для всех игр"""
    con = sqlite3.connect("assets/data_for_qt.db")
    cur = con.cursor()
    data = list(cur.execute('Select * from main_table').fetchall())
    if len(data) == 0:
        cur.execute(f"INSERT INTO main_table VALUES ({1}, "
                    f"(Select game_id from game where name = '{game_name}'), "
                    f"(Select player_id from players_and_results where name = '{winner}'))")
    elif len(data) < 30 and len(data) > 0:
        cur.execute(f"INSERT INTO main_table VALUES ({len(data) + 1}, "
                    f"(Select game_id from game where name = '{game_name}'), "
                    f"(Select player_id from players_and_results where name = '{winner}'))")
    else:
        cur.execute(f'Delete from main_table where game_num = {data[0][0]}')
        con.commit()
        cur.execute('UPDATE main_table SET game_num = game_num - 1')
        con.commit()
        data = list(cur.execute('Select * from main_table').fetchall())
        cur.execute(f"INSERT INTO main_table VALUES ({len(data) + 1}, "
                    f"(Select game_id from game where name = '{game_name}'), "
                    f"(Select player_id from players_and_results where name = '{winner}'))")
    con.commit()
