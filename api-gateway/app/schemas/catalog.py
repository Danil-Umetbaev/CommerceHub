from pydantic import BaseModel, ConfigDict

class ProductSchemas(BaseModel):
    id: str
    name: str
    description: str
    price: int
    image:  str
    category: str

    model_config = ConfigDict(from_attributes=True)


class ProductCreateSchemas(BaseModel):
    name: str
    description: str
    price: int
    image:  str
    category: str

    model_config = ConfigDict(from_attributes=True)

class ProductUpdateSchemas(ProductCreateSchemas):
    pass

class ProductPartialUpdateSchemas(BaseModel):
    name: str | None
    description: str | None
    price: int | None
    image:  str | None
    category: str | None

    model_config = ConfigDict(from_attributes=True)

