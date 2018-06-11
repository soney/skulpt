try:
    from vega_caller import render_graph
except:
    print("Mock render")
    def render_graph(js):
        print(js)

class Chart:

    def __init__(self, data):
        self.data = data

    def mark_bar(self):
        self.mark = BarChart(self.data)
        return self.mark

    def mark_point(self):
        self.mark = ScatterChart(self.data)
        return self.mark

class Mark:

    def __init__(self, data):
        self.data = data
        self.keys = data.keys()
        self.json = {}
        self.json["$schema"] = "https://vega.github.io/schema/vega-lite/v2.json"
        self.json['data'] = {}
        # Now convert the data into a json format
        vals = []
        primary_key = self.keys[0]
        for ix in range(len(self.data[primary_key])):
            d = {}
            for key in self.keys:
                d[key] = self.data[key][ix]
            vals.append(d)
        self.json['data'] = {"values": vals}


    def encode(self, x='', y=''):
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

        self.json['encoding'] = self.encoding

        render_graph(self.json)

class BarChart(Mark):
    def __init__(self, data):
        # we will assume that the data is structured like you would make a dataframe.
        # The keys are the name of the columns and the values are lists

        Mark.__init__(self, data)        
        self.json['mark'] = 'bar'

class ScatterChart(Mark):

    def __init__(self, data):
        Mark.__init__(self, data)
        self.json['mark'] = 'point'


class Axis:

    def _get_name_type(self, name):
        typed = {'Q': 'quantitative', 'O': 'ordinal', 'N': 'nominal', 'T':'temporal'}
        nt = name.split(':')
        tstring= 'quantitative'
        if len(nt) == 2:
            tstring = typed[nt[1]]
        return nt[0], tstring


    def __init__(self, name, bin=False):
        self.aggregate = None
        self.name, self.type = self._get_name_type(name)
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


if __name__ == '__main__':
    #Chart({'a':list("abc"), 'b':[1,2,3]}).mark_bar().encode(x='a:N',y='b')
    #Chart({'a':[3,4,5], 'b':[1,2,3]}).mark_point().encode(x='b',y='a')
    Chart({'a':[1,2,3,2,2,4,5,5,6,7,8,8,8,8,8,9,0,0]}).mark_bar().encode(Axis('a:Q', bin=True),y='count()')
