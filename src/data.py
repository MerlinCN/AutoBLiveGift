from tortoise import Tortoise, fields, models
from tortoise.exceptions import DoesNotExist, MultipleObjectsReturned

class DateFlag(models.Model):
    id = fields.IntField(pk=True)
    date = fields.DateField()

    class Meta:
        table = "date_flag"

    def __str__(self):
        return f"{self.date}"
    


async def init_db():
    db_path = "data.db"
    await Tortoise.init(
        db_url=f"sqlite://{db_path}",
        modules={"models": ["src.data"]},  # 指定模型所在的模块
    )
    await Tortoise.generate_schemas()  # 生成数据库表结构

async def get_date_flag(date: str) -> bool:
    try:
        await DateFlag.get(date=date)
        return True
    except DoesNotExist:
        return False
    except MultipleObjectsReturned:
        # 如果有多条记录，说明今天已经执行过了
        return True
    
async def set_date_flag(date: str) -> None:
    # 检查是否已存在相同日期的记录
    existing_records = await DateFlag.filter(date=date)
    if not existing_records:
        await DateFlag.create(date=date)
    
    