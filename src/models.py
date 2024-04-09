from pydantic import BaseModel


class Route(BaseModel):
    route_id: int
    from_port: str
    to_port: str
    leg_duration: int


class RouteInDB(Route):
    route_id: int
    from_port: str
    to_port: str
    leg_duration: int


class GeoJSON(BaseModel):
    type: str = "LineString"
    coordinates: list
