from models import DataTransfer,GeoPoint,TimeRange,Police,Camera,Rss,CameraImages
import json
import MySQLdb as mysql
import graphene as g

def state_to_abbr(state):
    abbrs = {"ALAMABA": "AL",
             "ARIZONA": "AZ",
             "ARKANSAS": "AR",
             "CALIFORNIA": "CA",
             "COLORADO": "CO",
             "CONNECTICUT": "CT",
             "DELAWARE": "DE",
             "FLORIDA": "FL",
             "GEORGIA": "GA",
             "IDAHO": "ID",
             "ILLINOIS": "IL",
             "INDIANA": "IN",
             "IOWA": "IA",
             "KANSAS": "KS",
             "KENTUCKY": "KY",
             "LOUISIANA": "LA",
             "MAINE": "ME",
             "MARYLAND": "MD",
             "MASSACHUSETTS": "MA",
             "MICHIGAN": "MI",
             "MINNESOTA": "MN",
             "MISSISSIPPI": "MS",
             "MISSOURI": "MO",
             "MONTANA": "MT",
             "NEBRASKA": "NE",
             "NEVADA": "NV",
             "NEW HAMPSHIRE": "NH",
             "NEW JERSEY": "NJ",
             "NEW MEXICO": "NM",
             "NEW YORK": "NY",
             "NORTH CAROLINA": "NC",
             "NORTH DAKOTA": "ND",
             "OHIO": "OH",
             "OKLAHOMA": "OK",
             "OREGON": "OR",
             "PENNSYLVANIA": "PA",
             "RHODE ISLAND": "RI",
             "SOUTH CAROLINA": "SC",
             "SOUTH DAKOTA": "SD",
             "TENNESSEE": "TN",
             "TEXAS": "TX",
             "UTAH": "UT",
             "VERMONT": "VT",
             "VIRGINIA": "VA",
             "WASHINGTON": "WA",
             "WEST VIRGINIA": "WV",
             "WISCONSIN": "WI",
             "WYOMING": "WY"}
    return abbrs[state]
    
def gen_time(data):
    start = None
    end = None
    if data['timerange']:
        start = data['timerange'].get('start')
        end = data['timerange'].get('end')
    elif data['timestamp']:
        #make end increment by one minute
        start = data['timestamp']
        end = data['timestamp']
    elif data['date']:
        #make end increment by one day
        start = data['date']
        end = data['date']
        col_toggle=True
    
    return {"start": start, "end": end}


class Geo(g.ObjectType):
    country = g.Field(g.String, required=True)
    state = g.Field(g.String, required=True)
    #abbr = g.Field(g.String, required=True)
    county = g.Field(g.String, required=True)
    city = g.Field(g.String)
    timestamp = g.String()
    timerange = g.Field(g.String)
    date = g.String()
    police = g.Field(g.List(Police),count=g.Argument(
                                            g.Int, default_value=1)
                                    ,offset=g.Argument(
                                            g.Int, default_value=0))
    camera = g.Field(g.List(Camera),count=g.Argument(
                                            g.Int, default_value=1)
                                    ,offset=g.Argument(
                                            g.Int, default_value=0))
    def resolve_police(self,args,context,info):
        offset = args.get("offset")
        count = args.get("count")
        print "help"
        dat = gen_time({'timestamp': self.timestamp, 'timerange': self.timerange,'date': self.date})
        query = "SELECT * FROM panopticon.incidents WHERE ({}{}{}) AND {} LIMIT {}".format(
                        "city='{}'{}".format(self.city.upper(), 
                            ' AND ' if self.state else '') if self.city else '',
                        "chapter='{}'{}".format(self.state.upper(),
                            ' AND ' if self.county else '') if self.state else '',
                        "county='{}'".format(self.county.upper()) if self.county else '',
                        'str_to_date(concat(date,time),"%c/%d/%y%T") BETWEEN {} AND {}'
                            .format(dat['start'],dat['end'])
                        ,count)
        print query
        con = mysql.Connect(host="172.17.0.1",user="pandas",passwd="pandas")
        c = con.cursor()
        c.execute(query)
        print "executed police query"
        return [Police(data=";;".join([str(obj) for obj in item])) for item in c.fetchall()]
        #return [Police(data="0,1,2,3,4,5,6,7,8,9,10,11,12,13,14") for i in range(0,count)]
    
    def resolve_camera(self,args,context,info):
        offset = args.get("offset")
        count = args.get("count")
        q = ''.join(['select * from camera__metadata where ST_Intersects(',
            'ST_PointFromText(concat("POINT(",longitude," ",latitude,")"),1),',
            '(select shape from counties where county="{}" and state="{}"))',
            ' limit {}']).format(self.county.split(' ')[0],state_to_abbr(self.state.upper()),count)
        con = mysql.Connect(host="172.17.0.1", user="pandas", passwd="pandas", db="panopticon")
        print "executing camera query"
        c = con.cursor()
        c.execute(q)
        dat = c.fetchall()
        print q
        return [Camera(data=";;".join([str(obj) for obj in item])) for item in dat]

class Time(g.ObjectType):
    timestamp = g.Field(g.String)
    timerange = g.Field(g.String)
    date = g.Field(g.String)
    debug = g.String()
    geo = g.Field(Geo,country=g.Argument(g.String,default_value="usa")
            ,state=g.String()
            ,county=g.String()
            ,city=g.String()
            ,timestamp=g.String()
            ,timerange=TimeRange()
            ,date=g.String())

    police = g.Field(g.List(Police),count=g.Argument(
                                            g.Int, default_value=1)
                                    ,offset=g.Argument(
                                            g.Int, default_value=0))
    camera = g.Field(g.List(CameraImages),id=g.Argument(g.Int, default_value=10)
                                            ,count=g.Argument(
                                            g.Int, default_value=1)
                                    ,offset=g.Argument(
                                            g.Int,default_value=0))
    rss = g.Field(g.List(Rss),count=g.Argument(
                                        g.Int, default_value=1),
                                offset=g.Argument(
                                        g.Int, default_value=0))

    def resolve_geo(self,args,context,info):
        return Geo(
                country=args.get("country"),
                state=args.get("state"),
                county=args.get("county"),
                city=args.get("city"),
                timestamp=self.timestamp,
                timerange=self.timerange,
                date=self.date)
    def resolve_police(self,args,context,info):
        return [Police(data="0,1,2,3,4,5,6,7,8,9,10,11,12,13,14") for i in range(0,args.get("count"))]
    
    def resolve_camera(self,args,context,info):
        #this function will take an id as an argument and return the images that are in the corresponding
        #temporal space
        obj = gen_time({'timestamp':self.timestamp,'timerange':self.timerange,'date':self.date})
        q = 'SELECT * FROM cameras WHERE filename LIKE "camera_{}-%" AND {} LIMIT {}'.format(
                str(args.get('id')),
                'date BETWEEN {} AND {}'.format(obj['start'],obj['end'])
                ,args.get("count"))
        print q
        con = mysql.Connect(host="172.17.0.1", user="pandas", passwd="pandas", db="panopticon")
        c = con.cursor()
        c.execute(q)
        print "executed camera image query"
        return [CameraImages(data=";;".join([obj for obj in item])) for item in c.fetchall()]

    def resolve_rss(self,args,context,info):
        return [Rss(data="['1','2','3'];http://example.com/") for i in range(0,args.get("count"))]

class Query(g.ObjectType):
    police = g.String()
    camera = g.String()
    rss = g.String()
    time = g.Field(Time,timestamp=g.String(),
                   timerange=TimeRange(),
                   date=g.String())
    
    def resolve_time(self,args,context,info):
        return Time(timestamp=args.get("timestamp"),
                   timerange=args.get("range"),
                   date=args.get("date"))
