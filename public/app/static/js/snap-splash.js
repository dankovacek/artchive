var set_bg_image = function() {
    var self = this;
    var s = new Snap("#splashLogo");
    var g = s.group();

    var logo = Snap.load('/static/images/artchivelogo_frontpage.svg', function(f) {
        var logo_svg = f.select("#layer1");
        g.append(logo_svg);
        var logo_dims = logo_svg.getBBox();
        var svg_canvas = document.getElementById("logo-container");
        var cvs_h = svg_canvas.offsetHeight;
        var cvs_w = svg_canvas.offsetWidth;

        // initial vertical % difference between logo and canvas
        var initial_vscale_diff = cvs_h / g.getBBox().height;

        // scaling factor, as % of actual height difference
        // between logo and canvas
        var sf = 0.8 * initial_vscale_diff;

        // scale string for initial scale transform
        //var s_str = 's' + sf.toString();
        //g.transform(s_str);

        // get updated logo dimensions after transform
        logo_w = g.getBBox().width;
        logo_h = g.getBBox().height;

        //console.log(logo_w, logo_h, 'new sizes');

        // set initial placement in middle of canvas
        var xi = ((cvs_w - logo_w * sf) / 2.0);
        var yi = ((cvs_h - logo_h * sf) / 2.0);

        //  Define a transform matrix
        var logoMatrix = new Snap.Matrix();

        logoMatrix.translate(xi, yi);
        logoMatrix.scale(sf);
        g.transform(logoMatrix);
        //console.log('xi, yi', xi, yi);
        //t_string = s_str + ' t' + xi.toString() + ' ' + yi.toString();
        //g.transform(t_string);
        // g.transform('S5 ' + t_string);
        // var sf = (canvas_width - 100) / logo_dims.width;
        // var transform_str = 's' + sf.toString();
        // console.log(init_x, init_y);
        // transform_str += ' t' + init_x + ' ' + init_y;
        // g.animate({
        //     transform: transform_str
        // }, 1000, mina.elastic);
    });
};
