try:
    from vega_caller import render_graph
except:
    print("Mock render")
    def render_graph(js):
        print(js)

class Chart:
    # TODO allow data to be specified as a URL
    def __init__(self, data, title=None):
        self.title=title
        if isinstance(data, dict):
            self.data = Data(**data)
        else:
            self.data = data

    def mark_bar(self):
        self.mark = BarChart(self.data, title=self.title)
        return self.mark

    def mark_point(self):
        self.mark = ScatterChart(self.data, title=self.title)
        return self.mark

    def mark_line(self):
        self.mark = LineChart(self.data, title=self.title)
        return self.mark

class Mark:

    def __init__(self, data, title=None):
        self.data = data
        self.title = title
        self.json = {}
        self.json["$schema"] = "https://vega.github.io/schema/vega-lite/v2.json"
        self.json['data'] = {}
        if self.title:
            self.json["title"] = self.title

        # Now convert the data into a json format
        self.json['data'] = {"values": data.vals}

    def encode(self, x='', y='', color='', size=''):
        self.encoding = {}
        if x:
            if isinstance(x,Axis): 
                self.encoding['x'] = x.toJson()
            else:
                self.encoding['x'] = Axis(x).toJson()
        if y:
            if isinstance(y, Axis):
                self.encoding['y'] = y.toJson()
            else:
                self.encoding['y'] = Axis(y).toJson()

        # "color": {"type": "nominal", "field": "species"}
        if color:
            field, tp = _get_name_type(color)
            self.encoding['color'] = dict(type=tp, field=field)

        # "size": {"type": "quantitative", "field": "Acceleration"}
        if size:
            field, tp = _get_name_type(size)
            self.encoding['size'] = dict(type=tp, field=field)
            
        self.json['encoding'] = self.encoding
        return self

    def display(self):
        render_graph(self.json)

class BarChart(Mark):
    def __init__(self, data, title=None):
        # we will assume that the data is structured like you would make a dataframe.
        # The keys are the name of the columns and the values are lists

        Mark.__init__(self, data, title=title)        
        self.json['mark'] = 'bar'

class ScatterChart(Mark):

    def __init__(self, data, title=None):
        Mark.__init__(self, data, title=title)
        self.json['mark'] = 'point'


class LineChart(Mark):

    def __init__(self, data, title=None):
        Mark.__init__(self, data, title=title)
        self.json['mark'] = 'line'


# TODO:  add a rect mark type for a heat map

def _get_name_type(name):
    typed = {'Q': 'quantitative', 'O': 'ordinal', 'N': 'nominal', 'T':'temporal'}
    nt = name.split(':')
    tstring= 'quantitative'
    if len(nt) == 2:
        tstring = typed[nt[1]]
    return nt[0], tstring

class Axis:



    def __init__(self, name, bin=False):
        self.aggregate = None
        self.name, self.type = _get_name_type(name)
        if  '()' in self.name: # aggregate function
            self.aggregate = self.name.replace('()','')
            self.name = None
        self.bin = bin

    def toJson(self):
        json = {}
        if self.name:
            json['field'] = self.name
        if self.type:
            json['type'] = self.type
        if self.bin:
            json['bin'] = True
        if self.aggregate:
            json['aggregate'] = self.aggregate

        return json


class X(Axis):
    pass

class Y(Axis):
    pass

class Data:
    def __init__(self, **kwargs):
        """
        input can be the form of a series of keyword args where 
        the keyword is the column name, or a single keyword data 
        that is a list of json style records as rows.
        could also accept a csv file? or keywords columns and rows
        This accepts a lot more options that "real altair" to make it easier
        to work with non-DataFrame data sets.  Internally:
        self.keys contains the list of column names
        self.vals is a list of dictionaries of the form [{col1:val1, col2:val2, ... coln:valn},
                                                         {col1:val3, col2:val4, ... coln:valn},
                                                         {col1:val5, col2:val6, ... coln:valn}]                                                         
        """
        # todo: accept a URL as the argument to read a CSV or JSON file
        if len(kwargs) == 1 and 'data' in kwargs:
            self.data = kwargs['data']
            self.keys = self.data[0].keys()
            self.vals = self.data
        elif len(kwargs) == 2 and ('columns' in kwargs) and ('rows' in kwargs):
            self.keys = kwargs['columns']
            self.vals = []
            for r in kwargs['rows']:
                self.vals.append(dict(zip(self.keys, r)))
        else:
            keys = kwargs.keys()
            vals = []
            primary_key = keys[0]
            for ix in range(len(kwargs[primary_key])):
                d = {}
                for key in keys:
                    d[key] = kwargs[key][ix]
                vals.append(d)
            self.vals = vals
            self.keys = keys

    def __str__(self):
        #header = "\t".join(self.keys) + "\n"
        header = ""
        for key in self.keys:
            header += key.center(10) + " "
        header += "\n"
        template = ""
        for key in self.keys:
            template += "{" + key + ": <10} "
        template += "\n"
        res = ""
        for row in self.vals:
            res += template.format(**row)
        
        return header + res
        



if __name__ == '__main__':
    d = Data(a=[3,4,5], b=[1,2,3], c=['r','g','b'])
    print(d)
    Chart({'a':list("abc"), 'b':[1,2,3]}).mark_bar().encode(x='a:N',y='b')
    Chart(Data(a=[3,4,5], b=[1,2,3], c=['r','g','b'])).mark_point().encode(x='b',y='a',color='c:O')
    Chart(Data(a=[1,2,3,2,2,4,5,5,6,7,8,8,8,8,8,9,0,0])).mark_bar().encode(Axis('a:Q', bin=True),y='count()')


# todo: see if I can work with the repr of an object to get the behavior that altair gets in notebooks
# todo: implement a Bin object to specifiy maxbins
