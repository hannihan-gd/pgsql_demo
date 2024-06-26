from basic.connection import get_async_connection_and_cursor
from static import test_employee
from logger import logger

async def run():
    # await test_select(cursor)
    await check_existence(False)
    await test_insert()
    await check_existence(True)

    await test_update()

    await test_delete()
    await check_existence(False)

    logger.info("test success")
            
async def test_select():
    async with get_async_connection_and_cursor() as (conn, cursor):
        get_top10_employees = "select * from employees.employees order by emp_no DESC LIMIT 10"
        await cursor.execute(get_top10_employees)
        async for emp in cursor:
            logger.debug(emp)
        
async def test_insert():
    async with get_async_connection_and_cursor() as (conn, cursor):
        query = """INSERT into employees.employees (emp_no, birth_date, first_name, last_name, gender, hire_date) 
            VALUES (%(emp_no)s, %(birth_date)s, %(first_name)s, %(last_name)s, %(gender)s, %(hire_date)s)"""
        try:
            await cursor.execute(query, test_employee)
            await conn.commit()
        except Exception as ex:
            logger.error("exception happens when executing insert")
            logger.error(ex)

async def test_update():
    async with get_async_connection_and_cursor() as (conn, cursor):
        query = "UPDATE employees.employees SET first_name = %s WHERE emp_no = %s"
        await cursor.execute(query, ("NoHanni", test_employee["emp_no"]))
        await conn.commit()

    async with get_async_connection_and_cursor() as (_, cursor):
        query = "select * from employees.employees where emp_no = %s"
        await cursor.execute(query, (test_employee["emp_no"], ))
        emp = await cursor.fetchone()
        if (emp["first_name"] != "NoHanni"):
            raise Exception("Update check failed")

async def test_delete():
    async with get_async_connection_and_cursor() as (conn, cursor):
        query = "DELETE FROM employees.employees WHERE emp_no = %s"
        await cursor.execute(query, (test_employee["emp_no"], ))
        await conn.commit()

async def check_existence(is_exist: bool):
    async with get_async_connection_and_cursor() as (conn, cursor):
        query = "select * from employees.employees where first_name = %s"
        await cursor.execute(query, (test_employee["first_name"],))
        emp = await cursor.fetchone()
        if ((emp is not None) != is_exist):
            raise Exception('check_existence is not as expected')
