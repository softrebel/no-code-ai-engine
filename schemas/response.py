
from typing import Generic, TypeVar
from pydantic.generics import GenericModel
from bson import ObjectId
from fastapi import status
DataT = TypeVar('DataT')


def OK(data: DataT | None, message='successfull'):
    return Response(status=status.HTTP_200_OK,
                    message=message, data=data)


def ERRROR(data: DataT | None, message='failed'):
    return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    message=message, data={})


class Response(GenericModel, Generic[DataT]):
    status: int | None
    message: str | None
    data: DataT | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    # @validator('error', always=True)
    # def check_consistency(cls, v, values):
    #     if v is not None and values['data'] is not None:
    #         raise ValueError('must not provide both data and error')
    #     if v is None and values.get('data') is None:
    #         raise ValueError('must provide data or error')
    #     return v
