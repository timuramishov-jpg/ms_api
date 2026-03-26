"""
Практическая работа №2 — Вариант 2
Студент: Амишов Тимур | Группа: ВБ-9822-22

Задание 2:
  Простой уровень    — вывести список всех картин (type_id = 1)
  Продвинутый уровень — найти 10 самых рентабельных картин с profit > 1.5
"""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

# Импорт get_db берём из уже существующего файла проекта
from backend.database import get_db

router = APIRouter(
    prefix="/api/v1/pr2",
    tags=["ПР2 — Амишов Тимур ВБ-9822-22"],
)


# ──────────────────────────────────────────────────────────────────────────────
# ПРОСТОЙ УРОВЕНЬ
# GET /api/v1/pr2/paintings
# Вернуть все экспонаты с type_id = 1 (Картина)
# ──────────────────────────────────────────────────────────────────────────────
@router.get("/paintings", summary="Все картины (type_id = 1)")
def get_all_paintings(db: Session = Depends(get_db)):
    """
    Простой уровень — задание 2.

    Возвращает список всех экспонатов категории «Картина» (type_id = 1).

    SQL:
        SELECT id, name, owner_id, profit
        FROM wings
        WHERE type_id = 1;
    """
    sql = text("""
        SELECT id,
               name,
               owner_id,
               profit
        FROM   wings
        WHERE  type_id = 1
    """)

    rows = db.execute(sql).fetchall()

    return {
        "sql": (
            "SELECT id, name, owner_id, profit "
            "FROM wings "
            "WHERE type_id = 1"
        ),
        "total": len(rows),
        "data": [
            {
                "id":       r.id,
                "name":     r.name,
                "owner_id": r.owner_id,
                "profit":   r.profit,
            }
            for r in rows
        ],
    }


# ──────────────────────────────────────────────────────────────────────────────
# ПРОДВИНУТЫЙ УРОВЕНЬ
# GET /api/v1/pr2/paintings/top-profitable
# Топ-10 самых рентабельных картин с profit > 1.5
# ──────────────────────────────────────────────────────────────────────────────
@router.get(
    "/paintings/top-profitable",
    summary="Топ-10 рентабельных картин (profit > 1.5)",
)
def get_top_profitable_paintings(db: Session = Depends(get_db)):
    """
    Продвинутый уровень — задание 2.

    Возвращает 10 наиболее рентабельных картин (profit > 1.5),
    отсортированных по убыванию рентабельности.
    Дополнительно выводится имя владельца через JOIN с таблицей owners.

    SQL:
        SELECT w.id,
               w.name,
               w.profit,
               o.first_name || ' ' || o.last_name AS owner
        FROM   wings w
        JOIN   owners o ON w.owner_id = o.id
        WHERE  w.type_id = 1
          AND  w.profit  > 1.5
        ORDER  BY w.profit DESC
        LIMIT  10;
    """
    sql = text("""
        SELECT w.id,
               w.name,
               w.profit,
               o.first_name || ' ' || o.last_name AS owner
        FROM   wings  w
        JOIN   owners o ON w.owner_id = o.id
        WHERE  w.type_id = 1
          AND  w.profit  > 1.5
        ORDER  BY w.profit DESC
        LIMIT  10
    """)

    rows = db.execute(sql).fetchall()

    return {
        "sql": (
            "SELECT w.id, w.name, w.profit, "
            "o.first_name || ' ' || o.last_name AS owner "
            "FROM wings w "
            "JOIN owners o ON w.owner_id = o.id "
            "WHERE w.type_id = 1 AND w.profit > 1.5 "
            "ORDER BY w.profit DESC "
            "LIMIT 10"
        ),
        "total": len(rows),
        "data": [
            {
                "id":     r.id,
                "name":   r.name,
                "profit": r.profit,
                "owner":  r.owner,
            }
            for r in rows
        ],
    }
