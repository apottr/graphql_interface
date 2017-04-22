import graphene as g

class GeoPoint(g.InputObjectType):
    lat = g.String()
    lon = g.String()
    
class TimeRange(g.InputObjectType):
    start = g.String()
    end = g.String()

class DataTransfer(g.ObjectType):
    timestamp = g.String()
    timerange = g.String()
    date = g.String()
    time = g.String()

class Rss(g.ObjectType):
    headlines = g.List(g.String)
    url = g.String()
    data = g.Field(g.String)

    def resolve_headlines(self,args,context,info):
        h = self.data.split(";")
        return eval(h[0])

    def resolve_url(self,args,context,info):
        h = self.data.split(";")
        return h[1]

class Police(g.ObjectType):
    description = g.String()
    address = g.String()
    date = g.String()
    chapter = g.String()
    city = g.String()
    county = g.String()
    dispatcher = g.String()
    frequency = g.String()
    fullIncident = g.String()
    incidentType = g.String()
    mutualAid1 = g.String()
    mutualAid2 = g.String()
    relayDispatcher = g.String()
    time = g.String()
    data = g.Field(g.String)
    debug = g.String()

    def resolve_debug(self,args,context,info):
        return "{}".format(self.data)

    def resolve_address(self,args,context,info):
        return self.data.split(';;')[1]
    
    def resolve_chapter(self,args,context,info):
        return self.data.split(';;')[2]
    
    def resolve_city(self,args,context,info):
        return self.data.split(';;')[3]
    
    def resolve_county(self,args,context,info):
        return self.data.split(';;')[4]
    
    def resolve_date(self,args,context,info):
        return self.data.split(';;')[5]
    
    def resolve_dispatcher(self,args,context,info):
        return self.data.split(';;')[7]
    
    def resolve_frequency(self,args,context,info):
        return self.data.split(';;')[8]
    
    def resolve_fullIncident(self,args,context,info):
        return self.data.split(';;')[9]
    
    def resolve_incidentType(self,args,context,info):
        return self.data.split(';;')[10]
    
    def resolve_mutualAid1(self,args,context,info):
        return self.data.split(';;')[11]
    
    def resolve_mutualAid2(self,args,context,info):
        return self.data.split(';;')[12]
    
    def resolve_relayDispatcher(self,args,context,info):
        return self.data.split(';;')[13]
    
    def resolve_time(self,args,context,info):
        return self.data.split(';;')[14]
    
    def resolve_description(self,args,context,info):
        return self.data.split(';;')[6]
    
class Camera(g.ObjectType):
    id = g.String()
    latitude = g.String()
    longitude = g.String()
    data = g.Field(g.String)
    
    def resolve_id(self,args,context,info):
        return self.data.split(';;')[0]

    def resolve_latitude(self,args,context,info):
        return self.data.split(';;')[1]

    def resolve_longitude(self,args,context,info):
        return self.data.split(';;')[2]


class CameraImages(g.ObjectType):
    date = g.String()
    filename = g.String()
    data = g.Field(g.String)

    def resolve_filename(self,args,context,info):
        return self.data.split(';;')[0]

    def resolve_date(self,args,context,info):
        return self.data.split(';;')[1]
