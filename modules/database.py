import pymysql
from configs.config import *
from modules.errors import *


class DataBase:
    def __ping(func):
        def function_wrapper(self, *args, **kwargs):
            self._conn.ping()
            return func(self, *args, **kwargs)
        return function_wrapper

    def __init__(self):
        self._conn = pymysql.connect(
            host=HOST,
            port=3306,
            user=USER,
            password=PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        self._cursor = self._conn.cursor()

    @__ping
    def add_thought(self, thought: str) -> None:
        """
        Add a thought to the list of thoughts.

        :param thought: The thought to add.
        :type thought: str
        :return: None
        """
        rows = self._cursor.execute(
            "INSERT INTO `thoughts` (thought) VALUES (%s)", (thought,))
        if rows != 1:
            raise RowsError()
        self._conn.commit()

    @__ping
    def get_thought_random(self) -> tuple:
        """
        Get a random thought.

        :return: A tuple containing the thought.
        :rtype: tuple
        """
        self._cursor.execute(
            "SELECT * FROM `thoughts` ORDER BY RAND() LIMIT 1")
        return self._cursor.fetchone()

    @__ping
    def get_thought_id(self, id: int) -> tuple | None:
        """
        Get a thought by its id.

        :param id: The id of the thought.
        :type id: int
        :return: A tuple containing the thought or None if the thought does not exist.
        :rtype: tuple | None
        """
        self._cursor.execute(
            "SELECT * FROM `thoughts` WHERE id = (%s)", (id,))
        return self._cursor.fetchone()

    @__ping
    def edit_rating(self, id: int, rating: int) -> int:
        """
        Edit the rating of a thought.

        :param id: The id of the thought to edit.
        :type id: int
        :param rating: The new rating of the thought.
        :type rating: int
        :return: The new rating of the thought.
        :rtype: int
        """
        rows = self._cursor.execute(
            "UPDATE `thoughts` SET rating = rating + %s WHERE id = %s", (id, rating))
        if rows != 1:
            raise RowsError()
        self._conn.commit()
        self._cursor.execute(
            "SELECT * FROM `thoughts` WHERE id = (%s)", (id,))
        return self._cursor.fetchone()
