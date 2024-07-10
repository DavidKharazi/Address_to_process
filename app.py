from fastapi import FastAPI, Query
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field

app = FastAPI()

llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key="my-api-key")

class GetAddress(BaseModel):

    region: str = Field(...,
                         description="Write the full name of the area, e.g. Московская область")
    district: str = Field(f'городской округ{"ai_msg.tool_calls"}', description="Write the full name of the district, e.g. городскаой округ Истра")
    village: str = Field(f'деревня{"ai_msg.tool_calls"}', description="Write the full name of the village, e.g. деревня Чесноково")
    cottage_village: str = Field(f'коттеджный поселок{"ai_msg.tool_calls"}',
                         description="Write the full name of the cottage_village, e.g. коттеджный поселок Миллениум Парк")
    residential_complex: str = Field(f'жилой комплекс{"ai_msg.tool_calls"}',
                                 description="Write the full name of the residential_complex, e.g. жилой комплекс Футуро Парк")
    street: str = Field(f'{"ai_msg.tool_calls"}улица',
                                     description="Write the full name of the street, e.g. Луговая улица")


llm_with_tools = llm.bind_tools([GetAddress])


# Вариант с вводом через консоль
address = input("Адрес: ")
ai_msg = llm_with_tools.invoke(address)
data = ai_msg.tool_calls

result = {}
for item in data:
    if 'args' in item:
        result.update(item['args'])

ordered_result = []
for field in GetAddress.__fields__:
    if field in result and result[field]:
        ordered_result.append(result[field])

print(", ".join(ordered_result))


#Fastapi(Закоментить вариант ввода через консоль)
# class Address(BaseModel):
#     address: str
#
#
# @app.get("/process_address")
# async def process_address(address: str = Query(..., description="Address to process")):
#     ai_msg = llm_with_tools.invoke(address)
#     data = ai_msg.tool_calls
#
#     result = {}
#     for item in data:
#         if 'args' in item:
#             result.update(item['args'])
#
#     ordered_result = []
#     for field in GetWeather.__fields__:
#         if field in result and result[field]:
#             ordered_result.append(result[field])
#
#     return {"result": ", ".join(ordered_result)}
#
#
# if __name__ == "__main__":
#     import uvicorn
#
#     # Запуск FastAPI сервера
#     uvicorn.run("app:app", host="0.0.0.0", port=8000)