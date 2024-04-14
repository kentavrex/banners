from pydantic import BaseModel


class BannerSchema(BaseModel):
    id: int
    feature_id: int


class FeatureSchema(BaseModel):
    id: int


class TagSchema(BaseModel):
    id: int
