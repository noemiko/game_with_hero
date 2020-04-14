from typing import NamedTuple

from duchshund_walk.utils import open_file
from duchshund_walk.utils import write_to_file


class ScoreRow(NamedTuple):
    nickname: str
    points: str
    date: str


def get_scores_results():
    rows = open_file("scores.csv")
    try:
        return list(map(ScoreRow._make, rows))
    except TypeError:
        return [ScoreRow("Contact with administrator about broken db", "", "")]


def save_new_scores(new_score: ScoreRow):
    users_scores = get_scores_results()
    new_table_scores = users_scores + [new_score]
    sorted_scores = sorted(new_table_scores, key=lambda x: int(x.points), reverse=True)
    write_to_file("scores.csv", sorted_scores)
