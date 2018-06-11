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
        vegaEmbed("#foo", Sk.ffi.remapToJs(vegaspec), {actions: true})
    });

    return mod;
}