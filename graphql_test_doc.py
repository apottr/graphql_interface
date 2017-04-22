import graphene as g

class LatLngInput(g.InputObjectType):
    lat = g.String()
    lng = g.String()

class Camera(g.ObjectType):
    id = g.Int()
    latitude = g.String()
    longitude = g.String()
    
    def resolve_id(self,args,context,info):
        return 10
    
class Police(g.ObjectType):
    city = g.String()
    def resolve_city(self,args,context,info):
        return "BLUE POINT"

    
class Query(g.ObjectType):
    world = g.Int(name=g.Argument(g.String))
    camera = g.Field(Camera,geo=LatLngInput())
    police = g.Field(Police)
    
    def resolve_world(self,args,context,info):
        return args.get("name")
    
    def resolve_camera(self,args,context,info):
        if args.get("geo") != None:
        	return Camera(latitude=args.get("geo").get("lat"),
                     	longitude=args.get("geo").get("lng"))
       	else:
            return Camera()

    def resolve_police(self,args,context,info):
        return Police()

schema = g.Schema(query=Query)

import graphene as g

class TimeframeInput(g.InputObjectType):
    start = g.String(required=True)
    end = g.String(required=True)

class GeoPair(g.InputObjectType):
    lat = g.String()
    lng = g.String()
    
class Camera(g.ObjectType):
    count = g.Int()
    coords = g.String()
    geo = g.Field(g.List(g.String))
    time = g.Field(g.String)
    def resolve_count(self,args,context,info):
        return -1
    
    def resolve_coords(self,args,context,info):
    	return "[{},{}],[{},{}]".format(self.geo[0]["lat"],
                         self.geo[0]["lng"],
                         self.geo[1]["lat"],
                         self.geo[1]["lng"])
    def resolve_time(self,args,context,info):
        return "{} -- {}".format(self.time.get("start"),self.time.get("end"))

class Query(g.ObjectType):
    hello = g.String()
    camera = g.Field(Camera,geo=g.List(GeoPair),time=TimeframeInput())

    def resolve_hello(self,args,context,info):
        return "world"

    def resolve_camera(self,args,context,info):
        return Camera(geo=args.get("geo"),time=args.get("time"))

schema = g.Schema(query=Query)


