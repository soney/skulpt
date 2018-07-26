// The specs for Vega are here:
// https://vega.github.io/vega-lite/docs/
//
// https://github.com/vega/vega-embed

var $builtinmodule = function (name) {
    var mod = {};

    mod.__file__ = "/src/lib/vega_caller.js";

    mod.__package__ = Sk.builtin.none.none$;

    mod.render_graph = new Sk.builtin.func(function (vegaspec) {
        Sk.builtin.pyCheckArgs("render_graph", arguments, 1, 1);
        // set actions to false to remove links to editor etc.
        let divid = '#' + Sk.divid + '_graphics'
        try {
            vegaEmbed(divid, Sk.ffi.remapToJs(vegaspec), {actions: true})
    } catch(e) {
        throw new Sk.builtin.Exception("Error in graph specification unable to render the graph\n" + e.message);
    }
    });

    return mod;
}