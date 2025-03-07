from typing import List, Optional

from tests.typing.models import Test, ProjectionTest


async def find_many() -> List[Test]:
    return await Test.find().to_list()


async def find_many_with_projection() -> List[ProjectionTest]:
    return await Test.find().project(projection_model=ProjectionTest).to_list()


async def find_many_generator() -> List[Test]:
    docs: List[Test] = []
    async for doc in Test.find():
        docs.append(doc)
    return docs


async def find_many_generator_with_projection() -> List[ProjectionTest]:
    docs: List[ProjectionTest] = []
    async for doc in Test.find().project(projection_model=ProjectionTest):
        docs.append(doc)
    return docs


async def find_one() -> Optional[Test]:
    t = await Test.find_one()
    if t is not None:
        t1: Test = t
        print(t1)
    return t


async def find_one_with_projection() -> Optional[ProjectionTest]:
    doc = await Test.find_one().project(projection_model=ProjectionTest)
    if doc is not None:
        doc_1: ProjectionTest = doc
        print(doc_1)
    return doc
