var $builtinmodule = function (name) {
    var elementClass;
    var mod = {};

    mod.getElementById = new Sk.builtin.func(function (id) {
        var result = document.getElementById(id.v);
        if (result) {
            return Sk.misceval.callsimArray(mod.Element, [result]);
        }
        return Sk.builtin.none.none$;
    });

    mod.createElement = new Sk.builtin.func(function (eName) {
        var r = document.createElement(eName.v);
        if (r) {
            return Sk.misceval.callsimArray(mod.Element, [r]);
        }
    });


    mod.getElementsByTagName = new Sk.builtin.func(function (tag) {
        var r = document.getElementsByTagName(tag.v)
        var reslist = [];
        for (var i = r.length - 1; i >= 0; i--) {
            reslist.push(Sk.misceval.callsimArray(mod.Element, [r[i]]))
        }
        return new Sk.builtin.list(reslist)
    });

    mod.getElementsByClassName = new Sk.builtin.func(function (cname) {
        var r = document.getElementsByClassName(cname.v);
        var reslist = [];
        for (var i = 0; i < r.length; i++) {
            reslist.push(Sk.misceval.callsimArray(mod.Element, [r[i]]));
        }
        ;
        return new Sk.builtin.list(reslist);
    });

    mod.getElementsByName = new Sk.builtin.func(function (cname) {
        var r = document.getElementsByName(cname.v);
        var reslist = [];
        for (var i = 0; i < r.length; i++) {
            reslist.push(Sk.misceval.callsimArray(mod.Element, [r[i]]));
        }
        ;
        return new Sk.builtin.list(reslist);
    });

    mod.querySelector = new Sk.builtin.func(function (cname) {
        var r = document.querySelector(cname.v);
        if (r) {
            return Sk.misceval.callsimArray(mod.Element, [r]);
        }
        return Sk.builtin.none.none$;
    });

    mod.querySelectorAll = new Sk.builtin.func(function (cname) {
        var r = document.querySelectorAll(cname.v);
        var reslist = [];
        for (var i = 0; i < r.length; i++) {
            reslist.push(Sk.misceval.callsimArray(mod.Element, [r[i]]));
        }
        ;
        return new Sk.builtin.list(reslist);
    });

    mod.getCurrentEditorValue = new Sk.builtin.func(function () {
        if (Sk.divid !== undefined && window.edList !== undefined) {
            if (Sk.gradeContainer != Sk.divid) {
                var edKey = Sk.gradeContainer + ' ' + Sk.divid;
                return new Sk.builtin.str(window.edList[edKey].editor.getValue())
            }
            return new Sk.builtin.str(window.edList[Sk.divid].editor.getValue())
        }
        else {
            throw new Sk.builtin.AttributeError("Can't find editor for this div");
        }
    })

    mod.currentDiv = new Sk.builtin.func(function () {
        if (Sk.divid !== undefined) {
            return new Sk.builtin.str(Sk.divid)
        }
        else {
            throw new Sk.builtin.AttributeError("There is no value set for divid");
        }
    })

    mod.currentCourse = new Sk.builtin.func(function () {
        if (eBookConfig !== undefined) {
            return new Sk.builtin.str(eBookConfig.course)
        }
        else {
            throw new Sk.builtin.AttributeError("There is no course");
        }
    })

    mod.currentGradingContainer = new Sk.builtin.func(function () {
        if (Sk.gradeContainer !== undefined) {
            return new Sk.builtin.str(Sk.gradeContainer)
        }
        else {
            if (Sk.divid != undefined) {
                return new Sk.builtin.str(Sk.divid)
            }
            throw new Sk.builtin.AttributeError("There is no value set for grading");
        }
    })


    elementClass = function ($gbl, $loc) {
        /*
         Notes:  self['$d'] is the dictionary used by the GenericGetAttr mechanism for an object.
         for various reasons  if you create a class in Javascript and have self.xxxx instance
         variables, you cannot say instance.xxx and get the value of the instance variable unless
         it is stored in the self['$d'] object.  This seems like a duplication of storage to me
         but that is how it works right now  (5/2013)

         Writing your own __getattr__ is also an option but this gets very tricky when an attr is
         a method...
         */
        $loc.__init__ = new Sk.builtin.func(function (self, elem) {
            self.v = elem
            self.innerHTML = elem.innerHTML
            self.innerText = elem.innerText
            if (elem.value !== undefined) {
                self.value = elem.value
                Sk.abstr.objectSetItem(self['$d'], new Sk.builtin.str('value'), new Sk.builtin.str(self.value))
            }

            if (elem.checked !== undefined) {
                self.checked = elem.checked
                Sk.abstr.objectSetItem(self['$d'], new Sk.builtin.str('checked'), new Sk.builtin.str(self.checked))
            }

            Sk.abstr.objectSetItem(self['$d'], new Sk.builtin.str('innerHTML'), new Sk.builtin.str(self.innerHTML))
            Sk.abstr.objectSetItem(self['$d'], new Sk.builtin.str('innerText'), new Sk.builtin.str(self.innerText))

        })

        $loc._internalGenericGetAttr = Sk.builtin.object.prototype.GenericGetAttr;
        $loc.__getattr__ = new Sk.builtin.func(function (self, name) {
            if (name != null && (Sk.builtin.checkString(name) || typeof name === "string")) {
                var _name = name;

                // get javascript string
                if (Sk.builtin.checkString(name)) {
                    _name = Sk.ffi.remapToJs(name);
                }

                var res = self.v[_name];
                if (res != undefined) {
                    return Sk.misceval.callsimArray(mod.Element, [res]);
                }
            }

            return $loc._internalGenericGetAttr(name);
        });

        $loc.__setattr__ = new Sk.builtin.func(function (self, key, value) {
            key = Sk.ffi.remapToJs(key);
            if (key === 'innerHTML') {
                self.innerHTML = value
                self.v.innerHTML = value.v
                Sk.abstr.objectSetItem(self['$d'], new Sk.builtin.str('innerHTML'), value)
            }
            if (key === 'innerText') {
                self.innerText = value
                self.v.innerText = value.v
                Sk.abstr.objectSetItem(self['$d'], new Sk.builtin.str('innerText'), value)
            }
        });


        $loc.appendChild = new Sk.builtin.func(function (self, ch) {
            self.v.appendChild(ch.v);
        });

        $loc.removeChild = new Sk.builtin.func(function (self, node) {
            self.v.removeChild(node.v)
        })

        $loc.closest = new Sk.builtin.func(function (self, ch) {
            var res = self.v.closest(ch.v);
            if (res) {
                return Sk.misceval.callsimArray(mod.Element, [res]);
            }
            return Sk.builtin.none.none$;
        });

        // getCSS

        $loc.getCSS = new Sk.builtin.func(function (self, key) {
            return new Sk.builtin.str(self.v.style[key.v]);
        });


        $loc.setCSS = new Sk.builtin.func(function (self, attr, value) {
            self.v.style[attr.v] = value.v

        })

        $loc.getAttribute = new Sk.builtin.func(function (self, key) {
            var res = self.v.getAttribute(key.v)
            if (res) {
                return new Sk.builtin.str(res)
            } else {
                return Sk.builtin.none.none$;
            }
        });

        $loc.setAttribute = new Sk.builtin.func(function (self, attr, value) {
            self.v.setAttribute(attr.v, value.v)
        });

        $loc.getProperty = new Sk.builtin.func(function (self, key) {
            var res = self.v[key.v]
            if (res) {
                return new Sk.builtin.str(res)
            } else {
                return Sk.builtin.none.none$;
            }
        });

        $loc.__str__ = new Sk.builtin.func(function (self) {
            console.log(self.v.tagName);
            return new Sk.builtin.str(self.v.tagName)
        })

        $loc.__repr__ = new Sk.builtin.func(function (self) {
            return new Sk.builtin.str('[DOM Element]')
        })


    };

    mod.Element = Sk.misceval.buildClass(mod, elementClass, 'Element', []);

    return mod;

}
